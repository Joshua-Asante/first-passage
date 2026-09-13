"""Account orchestration over the durable primitive kernel; offline candidate."""
from dataclasses import dataclass
from datetime import datetime

from book_policy import TakeoverPlan
from book_policy import leg as leg_spec
from book_protocol import OrderIntent

from .broker import STALENESS_WINDOW
from .effects import planned_command
from .kernel import Decision, Kernel, KernelRefusal, Operation, OWNED_SYMBOLS


@dataclass
class AccountKernel(Kernel):
    """Account commands publish primitive owners and account effects in one snapshot."""

    last_control_read: datetime | None = None
    SCHEMA = 5
    PERSISTED = Kernel.PERSISTED + ("last_control_read",)

    def completion_actions(self, now: datetime) -> None:
        """Automatically plan disarm during the completing event transition."""
        self._maybe_disarm(now)

    @planned_command
    def takeover(self, plan: TakeoverPlan, now: datetime) -> list[Operation]:
        """Cancel every displaced resting or partially filled risk-add, then ``CLOSE`` each
        displaced symbol; cancellation counts only when evidence confirms it (settle)."""
        if self.risk_add_blocked:
            raise KernelRefusal("takeover under a block")
        self.ledger.begin_takeover(plan)
        self.persist()
        self._in_evidence = True
        ops = []
        for leg_id in plan.displaced:
            sym = leg_spec(leg_id).symbol
            resting = [o for o in self.pending.values() if o.leg_id == leg_id
                       and o.status in ("accepted", "sent", "unknown", "partial")]
            op = self.close("sym", sym, now, "capacity_takeover")
            op.payload["cancel_refs"] = [o.ref for o in resting]
            ops.append(op)
        self.persist()
        self._in_evidence = False
        self._drain_effects()
        return ops


    def settle_takeover(self, intent: OrderIntent, now: datetime) -> Decision:
        """Admit the requester only when every displaced cancel is confirmed by evidence and
        every displaced symbol is flat on postdating evidence."""
        takeover = self.ledger._takeover  # pylint: disable=protected-access
        if takeover is None:
            raise KernelRefusal("no takeover pending")
        if takeover.state == "refused":
            self.ledger.settle_takeover()
            self.persist()
            return Decision(False, "takeover_refused")
        for leg_id in takeover.plan.displaced:
            sym = leg_spec(leg_id).symbol
            ops = [o for o in self.operations.values()
                   if o.reason == "capacity_takeover" and o.sym == sym]
            if not ops:
                takeover.fail(leg_id, "no close operation")
                break
            op = ops[-1]
            unconfirmed = [r for r in op.payload.get("cancel_refs", [])
                           if self.pending[r].status not in ("cancelled", "filled", "rejected")]
            if unconfirmed:
                takeover.fail(leg_id, f"cancel not confirmed for {unconfirmed}")
                break
            takeover.ack_cancel(leg_id)
            if op.status != "complete":
                takeover.fail(leg_id, f"close not confirmed ({op.status})")
                break
            if not self.quiescent(sym, now):
                takeover.fail(leg_id, "displaced scope no longer confirmed quiescent")
                break
            takeover.confirm_close(leg_id, self.p_ev[sym][0])
        if takeover.state == "pending":
            refusal = self._entry_refusal(intent, now)
            if (refusal or intent.leg_id != takeover.plan.requester
                    or self.size(intent.leg_id, intent.qty) != takeover.plan.contracts):
                takeover.fail(takeover.plan.requester,
                              refusal.reason if refusal else "request differs from takeover plan")
        decision = self.ledger.settle_takeover()
        if not decision.admitted:
            self._emit("capacity_takeover_refused", reason=decision.reason)
            self.persist()
            return Decision(False, "takeover_refused")
        return self._place(intent, takeover.plan.contracts, now)


    def kill_status(self, daemon_reachable: bool, now: datetime) -> dict:
        """S8 (7): completion reported beside the daemon-app acknowledgement."""
        return {"complete": self.dry_run and self.flatten_complete("kill", now), "disarmed": self.dry_run,
                "daemon_control": "acknowledged" if daemon_reachable else "not_reached"}


    @planned_command
    def eod(self, now: datetime) -> list[Operation]:
        """S7 (1)–(3): block, cancel resting risk-adds, prepare a close for every owned symbol."""
        self.block("eod", now.isoformat())
        return self._flatten_all(now, "eod_flatten")


    @planned_command
    def kill(self, now: datetime) -> list[Operation]:
        """S8: the listener block first, then the S7 steps."""
        self.block("kill", now.isoformat())
        return self._flatten_all(now, "kill")


    def _flatten_all(self, now: datetime, reason: str) -> list[Operation]:
        # The whole request and every required effect exist durably before the first send.
        self._in_evidence = True
        ops = [self.close("sym", sym, now, reason) for sym in OWNED_SYMBOLS]
        self.persist()
        self._in_evidence = False
        self._drain_effects()
        self._maybe_disarm(now)
        self.persist()
        return ops


    def flatten_complete(self, reason: str, now: datetime) -> bool:
        """S7 (4)–(5) / S8 completion: every owned symbol flat with no working order,
        on evidence that postdates its close operation (pure; no side effect)."""
        del now
        ops = [o for o in self.operations.values() if o.reason == reason]
        if len(ops) < len(OWNED_SYMBOLS) or any(o.status != "complete" for o in ops):
            return False
        for sym in OWNED_SYMBOLS:
            relevant = [o for o in ops if o.sym == sym]
            if not all(self.evidence_after(sym, o.sent_at or o.prepared_at,
                                           max(o.prepared_seq, o.sent_seq)) for o in relevant):
                return False
            if not self.quiescent(sym, self.clock.now):
                return False
        return True


    def _maybe_disarm(self, now: datetime) -> None:
        """S8 (6): the disarm is part of the kill-completion transition itself."""
        if self.dry_run or not any(o.reason == "kill" for o in self.operations.values()):
            return
        if self.flatten_complete("kill", now):
            if not any(e.kind == "disarm" for e in self.effects.values()):
                self._effect("disarm", "kill", {})


    @planned_command
    def on_flat_intent(self, op_id: str, leg_id: str, now: datetime) -> Operation:
        """The daemon's feed-loss flat; idempotent by operation identity. A resting risk-add
        of the leg is cancelled too — it must not trigger after its source has failed."""
        self.block("feed", op_id)
        op = self.close("leg", leg_id, now, "feed_loss_flat", op_id=op_id)
        return op


    def record_control_read(self, now: datetime) -> None:
        """R-N: the listener persists the time of every control read."""
        self.last_control_read = now
        self.persist()


    @planned_command
    def daemon_loss_check(self, now: datetime) -> list[Operation]:
        """S6 daemon-loss flat: absent timestamp counts as expired."""
        expired = self.last_control_read is None or now - self.last_control_read > STALENESS_WINDOW
        if not expired:
            return []
        ops = []
        for sym in OWNED_SYMBOLS:
            if self.quiescent(sym, now):
                continue
            self.block("feed", "daemon_loss")
            ops.append(self.close("sym", sym, now, "daemon_loss_flat"))
        if ops:
            self.block("feed", "daemon_loss")
        return ops


    def session_open(self) -> None:
        """R-1: the ``feed`` block clears only at the next session open; ``eod`` likewise."""
        self.unblock("feed")
        self.unblock("eod")
