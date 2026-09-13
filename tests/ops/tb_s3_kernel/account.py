"""Account orchestration over the durable primitive kernel; offline candidate."""
from dataclasses import dataclass, field
from datetime import datetime

from book_policy import TakeoverPlan
from book_policy import leg as leg_spec
from book_protocol import OrderIntent

from .broker import STALENESS_WINDOW
from .broker import Outcome
from .control import ConfigOwner
from .effects import planned_command
from .kernel import Decision, Kernel, KernelRefusal, Operation, OWNED_SYMBOLS


@dataclass
class AccountKernel(Kernel):
    """Account commands publish primitive owners and account effects in one snapshot."""

    last_control_read: datetime | None = None
    feed_episodes: dict = field(default_factory=dict)
    source_reports: dict = field(default_factory=dict)
    report_history: dict = field(default_factory=dict)
    source_highwater: dict = field(default_factory=dict)
    account_runs: dict = field(default_factory=dict)
    daemon_episode: str | None = None
    daemon_control: str = "not_reached"
    SCHEMA = 7
    PERSISTED = Kernel.PERSISTED + ("last_control_read", "feed_episodes", "source_reports",
                                   "account_runs", "daemon_episode", "daemon_control", "report_history",
                                   "source_highwater")

    def __post_init__(self):
        if self.broker.control_owner is None:
            self.broker.control_owner = ConfigOwner()

    def disarm_effect(self, effect):
        return self.broker.control_owner.disarm(effect.effect_id)

    def _effect_ready(self, effect):
        if effect.kind == "disarm":
            return (effect.status == "planned"
                    and effect.owner == self.account_runs.get("kill", {}).get("id")
                    and self.flatten_complete("kill", self.clock.now))
        return super()._effect_ready(effect)

    @planned_command
    def acknowledge_daemon_control(self, kill_id: str, command_id: str, now: datetime) -> bool:
        """Verify the separate config command's heartbeat; persist acknowledgment explicitly."""
        run = self.account_runs.get("kill")
        heartbeat = self.broker.control_owner.daemon_heartbeats.get(command_id)
        if (run is None or run["id"] != kill_id or heartbeat is None
                or heartbeat.get("emit_enabled") is not False
                or not 0 <= (now - heartbeat["at"]).total_seconds() <= STALENESS_WINDOW.total_seconds()):
            return False
        self.daemon_control = "acknowledged"
        run["daemon_command"] = command_id
        return True

    def completion_actions(self, now: datetime) -> None:
        """Automatically plan disarm during the completing event transition."""
        for reason in list(self.account_runs):
            run = self.account_runs[reason]
            if run.get("retire_when_complete") and self.flatten_complete(reason, now):
                run["active"] = False
            if run.get("active", True):
                self._expand_run(reason, now)
        self._maybe_disarm(now)

    def _account_symbols(self):
        return set(OWNED_SYMBOLS) | set(self.evidence) | {
            sym for ev in self.evidence.values() for sym in (ev.order_symbols or {}).values()}

    def _expand_run(self, reason, now):
        run = self.account_runs[reason]
        for sym in sorted(self._account_symbols() - set(run["scopes"])):
            op_id = f"{run['id']}:{sym}"
            run["scopes"][sym] = op_id
            self.close("sym", sym, now, reason, op_id=op_id)

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
        del daemon_reachable
        run = self.account_runs.get("kill", {})
        acknowledged = self.dry_run and any(e.kind == "disarm" and e.owner == run.get("id")
                                           and e.outcome == "accepted" for e in self.effects.values())
        return {"complete": acknowledged and self.flatten_complete("kill", now), "disarmed": acknowledged,
                "daemon_control": self.daemon_control}


    @planned_command
    def eod(self, now: datetime) -> list[Operation]:
        """S7 (1)–(3): block, cancel resting risk-adds, prepare a close for every owned symbol."""
        self.block("eod", now.isoformat())
        return self._flatten_all(now, "eod_flatten")


    @planned_command
    def kill(self, now: datetime) -> list[Operation]:
        """S8: the listener block first, then the S7 steps."""
        if "kill" not in self.blocks:
            self.account_runs.pop("kill", None)
            self.daemon_control = "not_reached"
        self.block("kill", now.isoformat())
        return self._flatten_all(now, "kill")


    def _flatten_all(self, now: datetime, reason: str) -> list[Operation]:
        # The whole request and every required effect exist durably before the first send.
        self._in_evidence = True
        if (reason not in self.account_runs or not self.account_runs[reason].get("active", True)
                or self.account_runs[reason].get("retire_when_complete")):
            self.account_runs[reason] = {"id": self._next("account"), "scopes": {}, "active": True}
        self._expand_run(reason, now)
        ops = [self.operations[i] for i in self.account_runs[reason]["scopes"].values()]
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
        run = self.account_runs.get(reason)
        if run is None or not self._account_symbols() <= set(run["scopes"]):
            return False
        ops = [self.operations[i] for i in run["scopes"].values()]
        if self.unresolved_requests or any(o.status != "complete" for o in ops):
            return False
        for sym in run["scopes"]:
            if (self.restarted_at is not None and not self.evidence_after(
                    sym, self.restarted_at, self.restart_seq)):
                return False
            relevant = [o for o in ops if o.sym == sym]
            if not all(self.evidence_after(sym, o.sent_at or o.prepared_at,
                                           max(o.prepared_seq, o.sent_seq)) for o in relevant):
                return False
            if not self.quiescent(sym, self.clock.now):
                return False
        return True


    def _maybe_disarm(self, now: datetime) -> None:
        """S8 (6): the disarm is part of the kill-completion transition itself."""
        if not any(o.reason == "kill" for o in self.operations.values()):
            return
        if self.flatten_complete("kill", now):
            run = self.account_runs["kill"]
            effect = next((e for e in self.effects.values()
                           if e.kind == "disarm" and e.owner == run["id"]), None)
            if effect is None:
                self._effect("disarm", run["id"], {})
            elif effect.status == "recorded" and effect.outcome != "accepted":
                if self.broker.control_owner.confirms(effect.effect_id):
                    self._effect_outcome(effect, Outcome("accepted"))
                else:
                    effect.status = "planned"  # idempotent config write with same identity
                self.persist()


    @planned_command
    def on_flat_intent(self, op_id: str, leg_id: str, now: datetime) -> Operation:
        """The daemon's feed-loss flat; idempotent by operation identity. A resting risk-add
        of the leg is cancelled too — it must not trigger after its source has failed."""
        self.block("feed", op_id)
        op = self.close("leg", leg_id, now, "feed_loss_flat", op_id=op_id)
        return op


    def record_control_read(self, now: datetime) -> None:
        """R-N: the listener persists the time of every control read."""
        if isinstance(self.last_control_read, datetime) and now < self.last_control_read:
            return
        self.last_control_read = now
        if self.daemon_episode is not None:
            self._retire_run("daemon_loss_flat")
        self.daemon_episode = None
        self.persist()


    @planned_command
    def daemon_loss_check(self, now: datetime) -> list[Operation]:
        """S6 daemon-loss flat: absent timestamp counts as expired."""
        expired = (not isinstance(self.last_control_read, datetime)
                   or now - self.last_control_read > STALENESS_WINDOW)
        if not expired:
            return []
        if self.daemon_episode is None:
            self.daemon_episode = self._next("daemon-loss")
            self.account_runs["daemon_loss_flat"] = {"id": self.daemon_episode, "scopes": {}}
        self.block("feed", self.daemon_episode)
        return self._flatten_all(now, "daemon_loss_flat")


    @planned_command
    def session_open(self) -> None:
        """R-1: the ``feed`` block clears only at the next session open; ``eod`` likewise."""
        self.unblock("feed")
        self.unblock("eod")
        if "eod_flatten" in self.account_runs:
            self._retire_run("eod_flatten")
        for op_id, episode in self.feed_episodes.items():
            if episode["active"]:
                self.block("feed", op_id)
        self._latch_stale_sources()
        if self.daemon_episode is not None:
            self.block("feed", self.daemon_episode)

    def _latch_stale_sources(self):
        for leg_id, report in self.source_reports.items():
            if self.clock.now - report["source_at"] > STALENESS_WINDOW:
                self.block("feed", f"stale-source:{leg_id}")

    def _retire_run(self, reason):
        run = self.account_runs[reason]
        run["retire_when_complete"] = True
        run["active"] = not self.flatten_complete(reason, self.clock.now)

    def _sweep_timeouts(self, now):
        super()._sweep_timeouts(now)
        self._latch_stale_sources()

    @planned_command
    def source_report(self, report: dict) -> bool:
        """Ordered, acknowledged episode commands; GET liveness is not source recovery."""
        leg_id, seq = report["leg_id"], report["seq"]
        leg_spec(leg_id)
        if type(seq) is not int or seq < 1:
            raise KernelRefusal("invalid source report sequence")
        self.source_highwater[leg_id] = max(seq, self.source_highwater.get(leg_id, 0))
        previous = self.source_reports.get(leg_id)
        if previous and seq <= previous["seq"]:
            if self.report_history.get((leg_id, seq)) == report:
                return True
            self.block("unknown_order", f"report-conflict:{leg_id}:{seq}")
            return False
        if seq != (previous["seq"] + 1 if previous else 1):
            self.block("unknown_order", f"report-gap:{leg_id}")
            return False
        if report["kind"] == "open":
            op_id = report["episode"]
            if (op_id in self.feed_episodes or report["at"] > self.clock.now
                    or report["at"] - report["source_at"] <= STALENESS_WINDOW
                    or previous and (previous["kind"] not in ("recovery", "health")
                                     or report["source_at"] < previous["at"])):
                self.block("unknown_order", f"invalid-episode:{op_id}")
                return False
            self.feed_episodes[op_id] = {"leg_id": leg_id, "active": True,
                                         "boundary": report["at"]}
            self.on_flat_intent(op_id, leg_id, report["at"])
        elif report["kind"] == "recovery":
            episode = self.feed_episodes.get(report["episode"])
            if (episode is None or episode["leg_id"] != leg_id
                    or not episode["active"] or previous is None
                    or previous["kind"] != "open" or previous["episode"] != report["episode"]
                    or report["source_at"] < episode["boundary"]
                    or report["source_at"] > report["at"] or report["at"] > self.clock.now
                    or report["at"] - report["source_at"] > STALENESS_WINDOW):
                return False
            episode["active"] = False
        elif report["kind"] == "health":
            if (report["source_at"] > report["at"] or report["at"] > self.clock.now
                    or report["at"] - report["source_at"] > STALENESS_WINDOW
                    or previous and report["source_at"] < previous["source_at"]
                    or any(e["leg_id"] == leg_id and e["active"]
                           for e in self.feed_episodes.values())):
                return False
        else:
            return False
        self.source_reports[leg_id] = dict(report)
        self.report_history[leg_id, seq] = dict(report)
        self._latch_stale_sources()
        if seq >= self.source_highwater[leg_id]:
            self.unblock("unknown_order", f"report-gap:{leg_id}")
        return True
