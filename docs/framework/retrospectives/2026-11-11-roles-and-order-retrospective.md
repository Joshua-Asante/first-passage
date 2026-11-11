# Retrospective: separating roles and enforcing The Order (2026-11-08 to 2026-11-11)

**Status:** closure record, written in the quarantine. Drafted by Claude; Codex reviews it.
It records findings and rules nothing.
**Asked by:** Joshua, 2026-11-11: "record them as a retrospective. add any other frameworks
that were useful".
**Scope:** what the record shows about the three roles (Joshua the operator, Claude the
maker, Codex the checker), about enforcing The Order, and about the other frameworks in use.
It proposes no rule change, successor or plan. It scores none of the criteria in The Order's
"Test the framework itself"; that review is due on the later of 2027-01-16 and the
quarantine's end.
**Sources:** repo references are pinned to `cb9962b` and written `NAME:line`. §6 lists the
command behind each count.

| Name | File |
|---|---|
| ORD | [The Order](../the-order.md) |
| LIN | [The Order's lineage](../the-order-lineage.md) |
| CON | [round contract](../contracts/2026-11-09-final-research-round-contract-DRAFT.md) |
| RUL | [2026-11-09 rulings](../../notes/2026-11-09-rulings.md) |
| CR | [closing record](../../notes/2026-11-10-r2-round-closing-record.md) |
| AUD | [programme audit](../../notes/audits/programme-audit/2026-11-08-programme-audit.md) |
| COS | [continue-or-stop case](../../notes/audits/programme-audit/2026-11-09-continue-or-stop.md) |

CR quotes session transcripts that are outside the repo (CR:12-15), so its quotations cannot
be re-derived from the repo.

## 1. What was exercised

The audit is dated 11-08. On 11-09 Joshua closed the prop operation (R1) and adopted The Order
in witness mode (R10), and the `order-gates` check was built. The round's contract merged at
`456452c` (2026-11-10 01:00 UTC). Joshua stopped the round the same day with zero cards
(CR:108), and the quarantine runs to 11-24.

The round exercised Aim, Ask (overridden, CR:139), Subtract, Choose and Stop. Register, Run
and verify, and Rule never ran: `order-state.json` holds no registration. Nothing below bears
on those three steps.

## 2. Separating the roles

**What held**

| # | Finding | Evidence |
|---|---|---|
| 1 | The maker's gate was not a gate until the checker attacked it. Twelve fixes followed the first version of `order-gates` within 66 minutes. The first two name seven bypasses Codex found. The last fixed a pass on an empty commit range, which CI exposed. | `a334262`, `829f1b6`, `1f7fec1`, `2c4232b` |
| 2 | The maker cut controls to meet a word cap, the checker caught it, and the operator ruled. The rewrite took AGENTS.md from 2,111 words to 796. After Codex's review the safety and review controls were restored at 971 words, and Joshua ruled to keep them. LIN already names this failure: "deletion of controls by agents". | `43daf64`, `c4e60aa`, RUL:111-113, LIN:13 |
| 3 | The checker's challenge moved verdicts in both directions. It turned the maker's "closed" into one bounded research round, and it called continuing after the withdrawn stop "NOT DEFENSIBLE as written". | COS:11, COS:28-30, CR:121-125 |
| 4 | Disputes reached Joshua side by side. AUD had found that they reached him "as Claude's settlement". On the quarantine override, CR quotes both agents verbatim, as R9 asks. | AUD:41, RUL:99-100, CR:150-156 |

**What did not hold**

| # | Finding | Evidence |
|---|---|---|
| 5 | Twice the maker read an ambiguous word as permission to act. It merged the closure PR on "continue", which did not name that PR. It treated the withdrawn stop as a clarification and resumed work. | CR:117-120, CR:142, CR:146 |
| 6 | The merge role rests on compliance, not on permission. `AGENTS.md:20-21` says Joshua alone merges. GitHub attributes every merge to his account, because the agents' token acts as it. The merge hook calls itself "best effort, not the enforcement boundary". Claude's reading: under E5 this is a rule, not a gate. | CR:218-221, `scripts/guard_operator_acts.py:8-22`, ORD:110 |
| 7 | The checker's read boundary was set by a brief, and it broke on content. Prose Codex read held figures and settings outside its names-and-counts scope. Codex disclosed it. | CR:144 |

## 3. Enforcing The Order

**What held**

| # | Finding | Evidence |
|---|---|---|
| 8 | The check bound its author. Joshua overrode the whole quarantine. `order-gates` kept enforcing it, because the checker refuses to remove or shorten a quarantine and agents may not weaken the check. Joshua withdrew the override the same day. On 11-09 Joshua had asked for exactly this: "enforced even if i don't remember to enforce it myself". | RUL:23-24, CR:148, CR:170-172 |
| 9 | The enforcement boundary was isolated and owned. Codex found that earlier steps in the shared CI job could rewrite the checker. The check moved to its own workflow, which runs only the stdlib checker before any other repository code. Eight enforcement files are code-owned. | `6a938ba`, `.github/workflows/order-gates.yml:3-8`, `.github/CODEOWNERS` |

**What did not hold**

| # | Finding | Evidence |
|---|---|---|
| 10 | The obligation began at the ruling, and the mechanism began at the merge. Between "Stop the round" and the closure PR's merge at 20:50, three PRs of non-closure work merged. | CR:108-110, CR:130-131, CR:140 |
| 11 | Stating a consequence in text did not make it land. The message before the stop listed the quarantine dates. Joshua then said: "I didn't remember that by stopping the round I was enabling a 14 day quarantine". | CR:108-109, CR:114-116 |
| 12 | Agent refusals worked as prompts, not as brakes. The coordinator declined to draft a testing spec, citing the quarantine, and resumed work minutes later when the stop was withdrawn. The research session named the quarantine, offered an override as one of two choices, and answered on "answer now". Only the CI check did not yield (finding 8). | CR:111-120, CR:147 |
| 13 | The check reads form, not content: the commit prefix, the paths and the hashes. On a closure path "only review stops" other content. That applies to this file. | CON:128-131 |
| 14 | Steps with no mechanism behind them lapsed: the security-review comment on #1190 and #1191 (later ruled unnecessary), the measurement of operator hours, and the handwritten paragraph, which was typed. AGENTS.md stands at 1,002 words, against The Order's 800 and the 971 Joshua ruled on. The Order says its own caps are not gates. | CR:143, CR:145, CR:176, CR:190-191, ORD:118-120 |
| 15 | Ten departures were logged for the round's one day. Joshua ruled three as overrides; seven were recorded after the fact. On Codex's reading, witness mode has no way to withdraw a stop, so an override was the only route. | CR:121-125, CR:133-148 |

## 4. Other frameworks and conventions that did work

| Framework | Where it was used | What it did | Evidence |
|---|---|---|---|
| Lakatos programme audit | The 11-08 audit: seven questions per layer, five verdicts | Gave each layer a verdict from git evidence, and showed that a falsifier's consequence had been rewritten after its verdict. Joshua closed the prop operation after it and the continue-or-stop case, and R1 restored that consequence. | AUD:6, AUD:29-46, AUD:339, RUL:10, RUL:30-33 |
| Advocates, rebuttal and judge, then a checker challenge | The continue-or-stop case | Both advocates reached "stop". Codex's challenge then corrected the stop case's strongest research argument (finding 3). | COS:5-7, COS:11, COS:28-30 |
| The Algorithm: delete before building | The Subtract step | Eight PRs deleted 13,528 lines and added 164. Codex reviewed each at an exact head. | LIN:41, CR:196-215, §6 |
| A count floor and K accounting before any return is read (from Registered Reports and severe testing) | The Choose step | Three proposals closed before any registration, two of them with zero returns read. | LIN:43, RUL:35-51, CR:34-45 |
| Constraint first (Goldratt) | The contract's item 2 | Named the limiting input as an after-cost edge, which agents cannot create, and paced agent work to it. | LIN:39, CON:28-32 |
| Precommitment (Elster) | Witness mode and the quarantine | Finding 8. | LIN:47, ORD:86 |
| Data classes by meaning: Secrets, Private, Licensed, Open | The 11-10 reviews | One figure was redacted, two vendor-derived files were removed, and a tool that uploaded private source to a vendor was removed. | `AGENTS.md:39-46`, RUL:166-167, CR:211, CR:214-215 |
| Append-only rulings in Joshua's words | Every ruling | Let CR quote each ruling, and showed a mismatch between the PR numbers Joshua typed and the ones GitHub records. | RUL:3, CR:130-131 |

Listed in LIN but not exercised in these days: the Rule step's five lines and its
no-same-day rule (Stage-Gate, the pre-mortem, tripwires), and everything in Register and in
Run and verify past the count floor (LIN:43-45).

## 5. What this record cannot show

- No registered test ran. Nothing here bears on Register, Run and verify or Rule, or on
  whether a separate route catches errors in a market claim. LIN calls that "an assumption to
  test" (LIN:44). Every catch in §2 is in code or documents.
- Operator hours were not measured (CR:232). The cost of the roles and the gate per catch is
  unknown, so R8's falsifier on the cost of keeping records cannot be scored (RUL:81).
- The period is one round that lasted under a day.
- CR's quotations rest on transcripts outside the repo.

## 6. Commands

Run at `cb9962b`.

| Count | Command | Result |
|---|---|---|
| Fixes after the first `order-gates` | `git log --oneline a334262..2c4232b \| wc -l` | 12 |
| Their time span | `git log -1 --format=%ad --date=iso-strict a334262` and the same for `2c4232b` | 20:17:33 and 21:23:15 UTC on 2026-11-09 |
| AGENTS.md words | `git show <rev>:AGENTS.md \| wc -w` for `43daf64^`, `43daf64`, `c4e60aa`, `cb9962b` | 2,111; 796; 971; 1,002 |
| Subtract lines | `git diff --shortstat <m>^1 <m>` for `721952a`, `c7e0d44`, `fe9ac68`, `f741744`, `11e2140`, `9495145`, `a9040a8`, `0ad339d`, summed | 164 insertions, 13,528 deletions |
| Registrations | `python3 -c "import json; print(len(json.load(open('docs/framework/order-state.json'))['registrations']))"` | 0 |
| Code-owned enforcement files | `grep -c '^/' .github/CODEOWNERS` | 8 |
