# How a SIG_DFL SIGUSR1 kills a Docker PID-1 CPython — mechanism note

Read-only research, 2026-09-20. Sources were fetched raw (kernel v6.8, runc v1.2.6 / v1.1.15,
glibc 2.36, Go 1.23, CPython 3.12.6, OpenBLAS 0.3.28, moby v28.0.0, containerd v2.0.0) and
grepped; line numbers below are from those tags. Repo facts are from the worktree at
`ops/c1_rail/qualification/execution/` and `deploy/qualification/bootstrap.py`.

## 0. Summary

The kernel's "container-init drops SIG_DFL signals" guarantee is enforced at **two** points,
and both are per-thread-mask dependent:

1. at send time, `sig_ignored()` → `sig_task_ignored()` — but `sig_ignored()` returns
   "not ignored" **before** reaching the SIGNAL_UNKILLABLE test whenever the *target task's*
   (`kill(pid)` ⇒ the thread-group leader's) mask has the signal **blocked**;
2. at dequeue time in `get_signal()` — which only runs if the signal is *delivered to a thread*.

Between those two points sits `complete_signal()`, which since Linux 4.15 (commit
426915796cca, Oleg Nesterov, 2017-11-17) **no longer checks SIGNAL_UNKILLABLE**. If the leader
has the signal blocked but *another thread in the group does not*, `complete_signal()` picks
that thread, sees `sig_fatal()` (handler == SIG_DFL), and starts a **group exit with
`group_exit_code = SIGUSR1`** directly — `get_signal()`'s init check is never consulted, and
`signal->flags = SIGNAL_GROUP_EXIT` even overwrites the SIGNAL_UNKILLABLE bit.

The probe process is exactly in that state during `import numpy`: OpenBLAS's load-time
constructor creates its thread pool with `pthread_create()`, and glibc's `pthread_create()`
**blocks all signals in the creating thread (the leader) around `clone()`**, while the worker
threads it already created run with SIGUSR1 unblocked (inherited mask). `import numpy` is
reached by `bootstrap.py campaign_probe` *before* `block_resume_signal()` runs
(`worker.py` → `compute.py` → `core/mc/simulation.py` → `import numpy`). The two observed deaths
(0.115 s and 0.18 s CPU consumed, exit 138, non-zero threads, no OOM) are consistent with a
`docker kill --signal=SIGUSR1` landing inside one of those windows, which a 33 % CPU quota
stretches from microseconds to milliseconds.

The same path is also open inside `block_resume_signal()` itself, between
`pthread_sigmask(SIG_BLOCK)` and `signal.signal(SIGUSR1, handler)` (leader blocked, OpenBLAS
threads unblocked, disposition still SIG_DFL).

Corollary for the earlier record (G3 packet, run 35494972519): the stated cause ("Go runtime
handles SIGUSR1 as fatal, `_SigNotify+_SigKill` → `dieFromSignal`") is **wrong on the Go
source**: Go 1.23's Linux sigtable has SIGUSR1 as `_SigNotify` only; an un-Notify'd SIGUSR1 is
caught and dropped ("Other signals will be caught but no action will be taken", os/signal docs).
And in the pre-Go nsexec phase the disposition is SIG_DFL on an unkillable single-threaded init
→ dropped by `sig_task_ignored()`. Neither `runc:[2:INIT]` phase can die of SIGUSR1. That run's
death (0.115 s CPU, 320 ms after the first send) fits the *same* numpy-import mechanism, with
the guardian not yet recording `comm`. The comm gate added by G3 therefore did not remove the
race; it moved the first send later.

## 1. Mechanism, with the establishing source lines

### 1.1 Kernel path for `kill(pid, SIGUSR1)` from the host

`kill(2)` → `kill_something_info()` (kernel/signal.c:1599-1604, pid > 0) → `kill_proc_info()`
→ `kill_pid_info()` (1481-1491): `p = pid_task(pid, PIDTYPE_PID)` (the **leader**), then
`group_send_sig_info(sig, info, p, PIDTYPE_TGID)` → `do_send_sig_info()` →
`send_signal_locked()` (1214-1248): sender is in an ancestor pidns so `force = true`
(1241-1245) — but `force` only matters for `sig_kernel_only()` = SIGKILL/SIGSTOP
(include/linux/signal.h:419-420, 445).

`__send_signal_locked()` (≈1075-1185): first `prepare_signal(sig, t, force)` (line 1084) →
`sig_ignored(t, sig, force)`:

```c
// kernel/signal.c v6.8
81  static bool sig_task_ignored(struct task_struct *t, int sig, bool force)
...
91  	if (unlikely(t->signal->flags & SIGNAL_UNKILLABLE) &&
92  	    handler == SIG_DFL && !(force && sig_kernel_only(sig)))
93  		return true;

103 static bool sig_ignored(struct task_struct *t, int sig, bool force)
104 {
105 	/*
106 	 * Blocked signals are never ignored, since the
107 	 * signal handler may change by the time it is
108 	 * unblocked.
109 	 */
110 	if (sigismember(&t->blocked, sig) || sigismember(&t->real_blocked, sig))
111 		return false;
...
118 	if (t->ptrace && sig != SIGKILL)
119 		return false;
120
121 	return sig_task_ignored(t, sig, force);
```

`t` here is the **leader** (from `kill_pid_info`). If the leader's `blocked` contains SIGUSR1,
the SIGNAL_UNKILLABLE test at line 91 is never reached; the signal is queued in
`signal->shared_pending` and `complete_signal(sig, t, type)` runs (line 1184):

```c
994  static void complete_signal(int sig, struct task_struct *p, enum pid_type type)
...
1004 	if (wants_signal(sig, p))            // leader: blocked → false (wants_signal:979-980)
1005 		t = p;
1006 	else if ((type == PIDTYPE_PID) || thread_group_empty(p))
1011 		return;                          // SINGLE-THREADED: safe, signal stays pending
1012 	else {
1016 		t = signal->curr_target;
1017 		while (!wants_signal(sig, t)) {  // find a sibling thread with SIGUSR1 unblocked
1018 			t = next_thread(t);
...
1034 	if (sig_fatal(p, sig) &&             // SIG_DFL and not ignore/stop default → true
1035 	    (signal->core_state || !(signal->flags & SIGNAL_GROUP_EXIT)) &&
1036 	    !sigismember(&t->real_blocked, sig) &&
1037 	    (sig == SIGKILL || !p->ptrace)) {
1041 		if (!sig_kernel_coredump(sig)) {
1048 			signal->flags = SIGNAL_GROUP_EXIT;   // overwrites SIGNAL_UNKILLABLE too
1049 			signal->group_exit_code = sig;       // = 10
1050 			signal->group_stop_count = 0;
1051 			__for_each_thread(signal, t) {
1053 				sigaddset(&t->pending.signal, SIGKILL);
1054 				signal_wake_up(t, 1);
```

`sig_fatal` (include/linux/signal.h:451-453) tests only the shared `sighand->action[]`
disposition, never SIGNAL_UNKILLABLE. Every thread then takes `get_signal()`'s
"already marked for death" branch (2727-2736: `signr = SIGKILL; goto fatal`) →
`do_group_exit(SIGKILL)` (2893) → `exit_code = sig->group_exit_code` (kernel/exit.c:999-1000)
→ `do_exit(10)` → `wait4` reports **WIFSIGNALED, WTERMSIG = 10** → containerd-shim
`128 + 10 = 138` → `docker inspect .State.ExitCode == 138`. Note the process dies with
"signal 10" although no thread ever *dequeued* SIGUSR1; the `get_signal()` drop at 2819-2821
("Container-init gets no signals it doesn't want") is bypassed because delivery never happens.

History: the 2009 design (commit b3bfa0cba867, "signals: protect cinit from blocked fatal
signals") explicitly relied on `complete_signal()` *and* `get_signal_to_deliver()` to cover
"a signal blocked when posted"; commit 426915796cca (v4.15) removed the
`SIGNAL_UNKILLABLE` term from `complete_signal()` on the argument that
"`sig_fatal(sig) && SIGNAL_UNKILLABLE` can only be true if … sig == SIGKILL OR it is traced"
— which overlooks the blocked-leader/unblocked-sibling case, since `sig_ignored()` only looks at
the leader's mask. Ubuntu 24.04's 6.8 kernel carries the v6.8 code shown above. I found no
public report of this exact race (unverified: a search, not a survey).

### 1.2 SIGNAL_UNKILLABLE is set on this task and survives execve (so the flag is not the gap)

- Set in `copy_process()` for the first pid of a new pidns: kernel/fork.c:2677-2679
  (`if (is_child_reaper(pid)) { ns_of_pid(pid)->child_reaper = p; p->signal->flags |= SIGNAL_UNKILLABLE; }`),
  `is_child_reaper` = `pid->numbers[pid->level].nr == 1` (include/linux/pid.h:157-160).
- runc: stage-1 `unshare(CLONE_NEWPID…)` then `clone_parent(&env, STAGE_INIT)`
  (nsexec.c:937, 962); stage-2 is "the only process that will actually return to the Go
  runtime" (nsexec.c:1000-1003, `prctl(PR_SET_NAME,"runc:[2:INIT]")` at 1026). Go side:
  `libcontainer.Init()` does `runtime.GOMAXPROCS(1); runtime.LockOSThread()`
  (init_linux.go:78-80) and the same thread ends in `system.Exec(name, args, env)`
  (standard_init_linux.go:290 → `unix.Exec`, system/linux.go:35-37). The entrypoint is therefore
  exec'd **by the PID-1 task itself**; the observed host pid is `docker inspect .State.Pid`
  (campaign_supervisor.py:1160), which is that task.
- execve keeps `signal_struct`: `begin_new_exec()` (fs/exec.c) calls `de_thread()` (1278),
  `unshare_sighand()` (1331), `__set_task_comm()` (1380) and `flush_signal_handlers()` (1385);
  the only `signal->flags` reference in exec.c is a read (1071). `de_thread` sets
  `group_exec_task`/`notify_count` only. Pending signals also survive exec (only
  `flush_itimer_signals()` at 1325 flushes anything).
- So on the observed run the flag *was* set; it was **bypassed**, not absent.

### 1.3 Why the probe is multithreaded with a blocked leader at 0.1–0.2 s CPU

- `bootstrap.py` (`deploy/qualification/bootstrap.py`) maps role `campaign_probe` → module
  `worker` and imports `c1_rail.qualification.execution.worker` **before** calling
  `campaign_probe_main`. `worker.py:9` `from .compute import run_n1_compute`; `compute.py:2`
  `from mc.simulation import EvaluationState`; `core/mc/simulation.py:9` `import numpy as np`.
  `requirements-ops.lock`: `numpy==2.4.6` (bundles a pthreads OpenBLAS). `block_resume_signal()`
  (campaign_probe.py) runs only afterwards, inside `main()`.
- OpenBLAS creates its pool at **library load**, not first use: `gotoblas_init` is a
  `CONSTRUCTOR` (driver/others/memory.c:1508) and calls `blas_thread_init()` (memory.c ≈1550,
  also 3359/3421); `blas_thread_init()` loops `for(i = 0; i < blas_num_threads - 1; i++)
  pthread_create(...)` (blas_server.c:579-591). No `sigmask` handling anywhere in
  blas_server.c/memory.c (grep). On a 4-vCPU runner this is 3 sequential `pthread_create`s from
  the main thread (Docker's CPU quota does not shrink the affinity mask that OpenBLAS counts).
- glibc 2.36 (`python:3.12-slim-bookworm`) `nptl/pthread_create.c`:

  ```c
  769   /* Block all signals, so that the new thread starts out with
  770      signals disabled.  This avoids race conditions in the thread
  771      startup.  */
  772   internal_sigset_t original_sigmask;
  773   internal_signal_block_all (&original_sigmask);      // rt_sigprocmask(SIG_BLOCK, all)
  ...
  786       pd->sigmask = original_sigmask;                  // child inherits the *unblocked* mask
  ...
  834   /* Return to the previous signal mask, after creating the new
  835      thread.  */
  836   internal_signal_restore_set (&original_sigmask);
  ```
  and the child restores `pd->sigmask` early in `start_thread` (line 426). So during creation
  of worker #2 and #3 the **leader has every signal blocked while worker #1 (…#2) has SIGUSR1
  unblocked and the disposition is SIG_DFL** — precisely the `complete_signal()` condition.
- Window length: a few µs of CPU, but under `cpu.max` = 33 % with four runnable threads
  (three new OpenBLAS servers allocating their buffers) the cgroup exhausts its quota in a few
  ms of wall time and is throttled for the remainder of the 100 ms period; a throttle inside the
  window stretches it to tens of ms. Sends every ~200 ms then hit it at the observed
  order-of-one-in-fifteen rate. (The stretch argument is reasoning, not measured.)
- Timing fit: Python 3.12 startup ≈ 25 ms CPU; the stdlib imports in `contract.py` etc.
  ≈ 50 ms; numpy 2.x import ≈ 80-150 ms CPU, with the OpenBLAS constructor early in it. Deaths
  at 0.115 s and 0.18 s CPU bracket that; the "~2.0 s wall ≈ 0.66 s CPU to reach the block" is
  well after it.
- A second identical window exists in `block_resume_signal()` itself:
  `signal.pthread_sigmask(SIG_BLOCK, {SIGUSR1})` (leader now blocked; OpenBLAS threads still
  unblocked) **then** `signal.signal(SIGUSR1, handler)` — until the second call returns the
  disposition is SIG_DFL and a send is fatal by the same path. Python bytecode between two
  syscalls, again stretchable by throttling.

### 1.4 Things checked and excluded

- Docker/containerd/runc signal path adds nothing: dockerd `task.Kill(ctx, stopSignal)` with no
  KillAll (moby v28 daemon/kill.go:109; libcontainerd/remote/client.go:313-315) →
  shim `Init.kill` → `runc kill` with `KillOpts{All: false}`
  (containerd cmd/containerd-shim-runc-v2/process/init.go:355-360) → runc `Container.Signal`
  (container_linux.go:376-406; the `signalAllProcesses` branch is SIGKILL-and-shared-pidns only)
  → `initProcess.signal` = `unix.Kill(p.pid(), s)` (process_linux.go:840-846). runc 1.1.15 is
  the same for a non-`--all` kill. No pidfd/cgroup.kill; plain `kill(2)`, positive pid.
  runc's `signals.go` handler is `runc run` foreground forwarding, not used under containerd.
- Container config (`probe_container_body`, campaign_supervisor.py:1004-1015): `PidMode=''`
  (private pidns), no `Init`, exec-form entrypoint `/opt/ops/bin/python` which is a
  `venv --copies` real binary (image.py:35) — no shell, no tini, no re-exec; comm `python` ⇒ the
  interpreter task is the pidns init.
- CPython 3.12 installs no SIGUSR1 handler at startup (`signal_install_handlers`: SIGPIPE,
  SIGXFSZ → SIG_IGN, SIGINT → default_int_handler; signalmodule.c:1910-1920), never touches the
  process mask at startup (no `sigprocmask`/`pthread_sigmask` in pylifecycle.c; the only mask
  call is `signal.pthread_sigmask` itself, signalmodule.c:973, and faulthandler's watchdog
  thread, faulthandler.c:564, which only runs for `dump_traceback_later`). The mask inherited
  across execve is runc init's; nsexec.c has no `sigprocmask` (grep of v1.2.6 and v1.1.15), and
  Go leaves SIGUSR1 blockable (`blockableSig`, signal_unix.go:1361-1373; sigtable entry
  `/* 10 */ {_SigNotify, ...}`, sigtab_linux_generic.go:20) so `runc init` simply inherits
  whatever mask containerd-shim's `os/exec` restored (normally empty). The observed deaths
  themselves imply SIGUSR1 was **unblocked** in the inherited mask (otherwise every thread would
  block it and the signal would just sit pending).
- `force_sig_info_to_task()` (signal.c:1314-1358) is the only place that *clears*
  SIGNAL_UNKILLABLE, for kernel-forced SIG_DFL signals; not involved (no SIGSEGV/SIGSYS:
  Docker's seccomp profile returns errno, not SIGSYS).
- ptrace: `sig_ignored` line 118 also skips the drop for traced tasks, but `complete_signal`
  line 1037 then refuses the group exit; nothing traces the container.
- OOM / pids limit / RLIMIT: excluded by the artifact (no OOM event, 0.18 s CPU).

## 2. Evidence that would confirm it in a future run artifact

Retain, on every guardian poll of the init pid (all world-readable, no ptrace needed):

- `/proc/<pid>/status` fields `Threads:`, `SigBlk:` (this file shows the **leader** thread's
  mask), `ShdPnd:`, `SigCgt:`, `NSpid:` (fs/proc/array.c:212, 291, 297-300). Prediction for
  the poll immediately preceding a fatal send: `Threads:` ≥ 2, `SigCgt` bit 9 (mask `0x200`)
  clear, and either (a) leader `SigBlk` = `fffffffffffffeff`/`ffffffffffffffff`-style all-ones
  (glibc `sigall_set`, internal-signals-linux.h:64-66) — the `pthread_create` window — or
  (b) `SigBlk` = `0000000000000200` with `SigCgt` bit 9 still clear — the
  `block_resume_signal()` window. `NSpid: <hostpid> 1` proves it is the pidns init (so the
  "not really PID 1" alternative is ruled out in-band).
- Per-thread masks: `/proc/<pid>/task/<tid>/status` `SigBlk` for every tid; the mechanism needs
  at least one tid with bit 9 clear while the leader has it set.
- The final `PAYLOAD_EXIT` with `exit_code == 138` and `oom_killed == false`; the shim maps a
  signalled wait status to 128+sig (containerd `sys/reaper`, unverified quote).
- Kernel-side proof (host tooling, if the runner allows): `perf trace -e signal:signal_generate
  -e signal:signal_deliver` or bpftrace on those tracepoints filtered to the pid: a
  `signal_generate` with `sig=10 group=1 result=0` (delivered/queued, not
  `TRACE_SIGNAL_IGNORED`) followed by `signal_deliver sig=9` to every tid and
  `sched_process_exit`, with **no** `signal_deliver sig=10`. Dropped sends show
  `result=1` (TRACE_SIGNAL_IGNORED) instead.
- `auditd -S kill` only proves the sends, not the outcome; low value.
- Cheapest offline confirmation/falsification (one Linux host, no CI): run the worker image
  with `--cpus 0.33`, entrypoint `python -c "import numpy, time; time.sleep(60)"`, and loop
  `docker kill -s USR1` every 5 ms during the first second. Expect occasional exit 138. Repeat
  with `-e OPENBLAS_NUM_THREADS=1` (no thread pool) → never dies; repeat with a handler installed
  before the import → never dies. Death with `Threads: 1` in the last poll would falsify this
  note.
- `docker inspect -f '{{.HostConfig.PidMode}} {{.HostConfig.Init}} {{.HostConfig.Runtime}}'`
  and `docker info` (Default Runtime, Init Binary) to pin the configuration assumed here.

## 3. Does a `/proc/self/comm` readiness token close the race?

Yes, for the fatal path, regardless of which window is hit — with the token written **after**
the handler is installed, and provided the guardian gates *every* send on the token, not only
the first.

- Ordering argument: the only way `complete_signal()` starts a group exit is
  `sig_fatal(p, sig)` = disposition SIG_DFL (signal.h:451-453). Once `signal.signal(SIGUSR1,
  handler)` has returned, the shared `sighand->action[9]` is a handler and `sig_fatal` is false
  for every later send, whatever the per-thread masks are. `/proc/<pid>/comm` write →
  `comm_write` → `set_task_comm(p)` under `task_lock` (fs/proc/base.c:1660-1685;
  `__set_task_comm` fs/exec.c:1245-1252); the guardian's read of the token is therefore
  ordered after the handler install. So a gated send can be queued (all threads block it),
  delivered to the no-op handler on some thread, or consumed by `sigtimedwait` — never fatal.
- Kernel facts for the marker: `REG("comm", S_IRUGO|S_IWUSR, …)` (base.c:3271) — readable by
  any uid, including a guardian running as a different uid (the repo already relies on this,
  `_process_image`, campaign_supervisor.py:1062-1076). Writes are accepted only from the same
  thread group (`same_thread_group`, base.c:1677-1682) and truncated to `TASK_COMM_LEN - 1 =
  15` bytes (base.c:1667-1670; `TASK_COMM_LEN = 16`, include/linux/sched.h:301). The write
  targets the task the directory names: `/proc/self/comm` is the **tgid** entry, so it renames
  the leader even if written from another thread; `prctl(PR_SET_NAME)` renames the *calling*
  thread only — call it from the main thread or use the `/proc/self/comm` write. Do not write
  a trailing newline (it becomes part of the name; `comm_show` appends its own). Keep the token
  ASCII, ≤ 15 bytes, and distinct from `python` and `runc:[` so `_interpreter_image` /
  `_pre_exec_init` stay unambiguous.
- Caveats: (a) comm is not an identity — any process can name itself the token; the existing
  uid/start_ticks/cgroup binding (`_process_identity`) must stay the identity, the token is only
  a readiness bit. (b) `hidepid` on /proc would hide it from a foreign-uid guardian; the
  guardian already reads `/proc/<pid>/stat|status`, so this is no new dependency. (c) The token
  survives `fork()` into children (they are not PID 1 and are killable by SIGUSR1, but the
  guardian signals only `State.Pid`). (d) It does **not** survive a later `execve` (comm is
  reset to the new basename, handlers reset to SIG_DFL) — so an S3 entrypoint that re-execs
  must redo the handshake; the guardian must keep re-evaluating the gate every turn, which the
  current loop does (`_interpreter_image(*init_image)` per turn, line 1220-1221).
- It does not by itself guarantee the resume is *received by `sigtimedwait`*: if any thread has
  SIGUSR1 unblocked (the OpenBLAS pool created before the block), `complete_signal()` prefers
  the leader only while the leader is inside `sigtimedwait` (`wants_signal(p)` true because
  `do_sigtimedwait` temporarily removes the set from `blocked`, signal.c:3635-3636); a send
  landing between the token write and the wait can be consumed by an OpenBLAS thread's no-op
  handler. The bounded re-send window (`RESUME_SIGNAL_SENDS`) covers that today; blocking
  before any thread exists (below) removes it.

## 4. Implications for the real S3 worker entrypoint

1. **Block and install before any thread exists — i.e. in `bootstrap.py`, before
   `importlib.import_module(...)`**, not in the role module. Threads inherit the mask at
   creation (glibc line 786), so a block done first is process-wide; a block done after
   `import numpy` covers only the main thread and leaves the fatal window and the
   handler-steal window open. `campaign_probe.block_resume_signal()`'s docstring claim ("a
   container init holds a blocked signal pending regardless of disposition") is true only for
   a process whose *every* thread blocks it.
2. **Install the handler first, then block** (`signal.signal` before `pthread_sigmask`). With
   the handler installed, no send can be fatal even if the process is already multithreaded;
   the only cost of the reversed order is a possibly handler-consumed send, which the re-send
   window already tolerates. The current order has the two states reversed for the length of a
   Python call under a 33 % quota.
3. Never rely on "PID 1 ignores SIG_DFL signals" for any process that may become
   multithreaded. The kernel guarantee is: a SIG_DFL signal is dropped **iff the leader has it
   unblocked at send time**; if the leader blocks it and any sibling does not, it is fatal.
   This applies to SIGTERM/SIGINT too: a SIG_DFL SIGTERM from `docker stop` can kill a
   multithreaded PID-1 worker during any `pthread_create` (or any other leader-side
   block-all window, e.g. glibc `fork()`/`posix_spawn` internals) instead of being ignored —
   acceptable, but the worker's exit-code semantics must not assume "SIGTERM is dropped until
   the handler is installed".
4. Gate every resume on the readiness token (comm), not on `comm == python`; the guardian's
   send-eligibility should require both the retained identity and the token, re-read each turn.
5. Retain `Threads`, leader `SigBlk`, `SigCgt` in `PROCESS`/`RESUMED` events; with them the
   next 138 is attributable from the artifact alone (§2), and the fix is verifiable: after the
   change, every `RESUMED` must show `SigCgt` bit 9 set.
6. Numpy/OpenBLAS thread pools are pure overhead in a 0.33-CPU payload; setting
   `OPENBLAS_NUM_THREADS=1` in the container env also removes the only thread creator on the
   startup path — a belt to the braces in items 1-2, not a substitute (any future C extension
   or `threading` use reopens the window without the mask fix).

## 5. Unverified / not established

- No runtime capture of `Threads`/`SigBlk` exists for either run; §1.3 is inferred from source
  reads plus the CPU-time and exit-code fit. §2 lists what turns it into evidence.
- The OpenBLAS thread count on the runner (assumed 4 vCPU → 3 pool threads) and whether numpy
  2.4.6's bundled OpenBLAS is built with `SMP_SERVER` (pthreads) — both standard, not checked
  on the image.
- The throttling-stretches-the-window argument is qualitative; no measurement.
- No prior public report of this exact `complete_signal()` blocked-leader gap was located.
- containerd's 128+signal mapping is quoted from memory.

## Sources

- kernel v6.8: https://raw.githubusercontent.com/torvalds/linux/v6.8/kernel/signal.c ·
  https://raw.githubusercontent.com/torvalds/linux/v6.8/kernel/fork.c ·
  https://raw.githubusercontent.com/torvalds/linux/v6.8/fs/exec.c ·
  https://raw.githubusercontent.com/torvalds/linux/v6.8/kernel/exit.c ·
  https://raw.githubusercontent.com/torvalds/linux/v6.8/include/linux/signal.h ·
  https://raw.githubusercontent.com/torvalds/linux/v6.8/include/linux/pid.h ·
  https://raw.githubusercontent.com/torvalds/linux/v6.8/fs/proc/base.c ·
  https://raw.githubusercontent.com/torvalds/linux/v6.8/fs/proc/array.c
- kernel history: https://github.com/torvalds/linux/commit/426915796ccaf9c2bd9bb06dc5702225957bc2e5
  (remove SIGNAL_UNKILLABLE check in complete_signal, v4.15) ·
  https://github.com/torvalds/linux/commit/ac25385089f673560867eb5179228a44ade0cfc1 ·
  https://github.com/torvalds/linux/commit/b3bfa0cba867f23365b81658b47efd906830879b
  (2009 "protect cinit from blocked fatal signals") ·
  https://lore.kernel.org/patchwork/patch/870783/
- glibc 2.36: https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=nptl/pthread_create.c;hb=refs/tags/glibc-2.36 ·
  https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=sysdeps/unix/sysv/linux/internal-signals.h;hb=refs/tags/glibc-2.36
- OpenBLAS 0.3.28: https://raw.githubusercontent.com/OpenMathLib/OpenBLAS/v0.3.28/driver/others/blas_server.c ·
  https://raw.githubusercontent.com/OpenMathLib/OpenBLAS/v0.3.28/driver/others/memory.c
- runc: https://raw.githubusercontent.com/opencontainers/runc/v1.2.6/libcontainer/nsenter/nsexec.c ·
  https://raw.githubusercontent.com/opencontainers/runc/v1.2.6/libcontainer/init_linux.go ·
  https://raw.githubusercontent.com/opencontainers/runc/v1.2.6/libcontainer/standard_init_linux.go ·
  https://raw.githubusercontent.com/opencontainers/runc/v1.2.6/libcontainer/container_linux.go ·
  https://raw.githubusercontent.com/opencontainers/runc/v1.2.6/libcontainer/process_linux.go ·
  https://raw.githubusercontent.com/opencontainers/runc/v1.2.6/kill.go (and the v1.1.15 twins)
- Go 1.23: https://raw.githubusercontent.com/golang/go/go1.23.0/src/runtime/signal_unix.go ·
  https://raw.githubusercontent.com/golang/go/go1.23.0/src/runtime/sigtab_linux_generic.go ·
  https://raw.githubusercontent.com/golang/go/go1.23.0/src/runtime/sigqueue.go ·
  https://pkg.go.dev/os/signal
- CPython 3.12.6: https://raw.githubusercontent.com/python/cpython/v3.12.6/Modules/signalmodule.c ·
  https://raw.githubusercontent.com/python/cpython/v3.12.6/Python/pylifecycle.c ·
  https://raw.githubusercontent.com/python/cpython/v3.12.6/Modules/faulthandler.c
- moby v28.0.0: https://raw.githubusercontent.com/moby/moby/v28.0.0/daemon/kill.go ·
  https://raw.githubusercontent.com/moby/moby/v28.0.0/libcontainerd/remote/client.go
- containerd v2.0.0: https://raw.githubusercontent.com/containerd/containerd/v2.0.0/cmd/containerd-shim-runc-v2/process/init.go
- repo (worktree): `deploy/qualification/bootstrap.py`,
  `ops/c1_rail/qualification/execution/{campaign_probe,worker,compute,campaign_supervisor,image}.py`,
  `core/mc/simulation.py`, `requirements-ops.lock`,
  `docs/briefs/handoffs/2026-09-20-full-e1-s2-g3-resume-before-exec.md`

## Addendum 2026-09-21 — the healthy-send prediction, corrected by run 35552151992

The prediction "before a healthy send: leader `SigBlk` bit 9 set and `SigCgt` bit 9 set" is half right. On the first integrated run with the send-time masks retained (run 35552151992, merged head `deacbb4`), every payload's **first** send showed `SigBlk=0x0000000000000000` with `SigCgt=0x0000000000000202` and `Threads=1`, and every later re-send showed `SigBlk=0x0000000000000200`. Mechanism: `do_sigtimedwait` (kernel/signal.c) temporarily clears the awaited set from `tsk->blocked` while the task sleeps, keeping the original in `tsk->real_blocked` (which `sig_ignored()` also honours), so the arrival wakes the waiter; `/proc/<pid>/status` `SigBlk` reports `tsk->blocked`, i.e. the temporary mask. The first send is by construction the one that lands during the wait. The invariant that closes the fatal path is therefore `SigCgt` bit 9 on every send (handler installed → `sig_fatal()` false → `complete_signal()` never takes the group-exit branch); `SigBlk` bit 9 is expected only on sends after the wake. `Threads=1` on every send confirms the thread-limit environment kept OpenBLAS single-threaded at send time. The Linux `resumed_image` assertion was over-strict and is corrected accordingly; no production change.
