# CI resilience — fail-closed, self-healing, no blind spots

The repo's teeth (`tools/validate.py`, `verify_mount_strategy.py`, `verify_deploy_*`, the pytest
suites) already exit non-zero on any violation. This document is about making that enforcement
**unbypassable and self-maintaining**, not advisory.

## The three gaps this closes

1. **Stacked-PR blind spot.** `on.pull_request.branches: [main]` only validated PRs whose *base*
   was `main`. A stacked PR (base = another feature branch) merged into its base with **zero repo
   CI**, and was only ever validated once it happened to reach `main`. Fixed: `pull_request` now
   fires for **any** base branch, plus `merge_group` (merge queue) and a daily `schedule`.
2. **Advisory, not required.** `main` had no branch protection — the teeth ran but nothing forced
   them green before a merge. Fixed by requiring the **`CI gate (fail-closed aggregate)`** status
   check on `main`.
3. **No re-assertion.** Nothing re-checked `main` after it was green once (a transitive dependency
   or an out-of-band push could rot it silently). Fixed by the scheduled plumb-line + self-heal.

## Fail-closed aggregate gate

`ci-gate` `needs: [selftest]`, runs `if: always()`, and **explicitly asserts** every required job
`== success`. A skipped, cancelled, or failed teeth job fails the gate — you cannot merge on a
check that merely "didn't run red". Branch protection requires this one context, so adding a new
teeth job in future only widens enforcement (wire it into `ci-gate.needs`); it can never silently
narrow it.

## Self-healing drift loop (scheduled plumb-line)

The teeth re-run daily against `main`. Two guarded jobs make the outcome self-maintaining:

- `drift-autofile` — on a scheduled **failure**, opens (or updates) a single tracking issue.
- `drift-resolve` — on a scheduled **success**, auto-closes that issue.

This is **detection + notification + auto-recovery of the tracking state** — deliberately *not* a
blind auto-mutation of `main`. Auto-"fixing" a red trunk is the daemon that dies; the control that
cannot fail is the required gate. The loop guarantees drift is *surfaced within a day and cleared
automatically once real*, never left to rot unseen.

## Least privilege

Top-level `permissions: contents: read`. Only the two self-heal jobs elevate to `issues: write`,
and only they need it. Superseded PR runs are cancelled by `concurrency`; trunk pushes and the
scheduled plumb-line are never cancelled.

## Branch protection (the enforcement)

`main` requires the `CI gate (fail-closed aggregate)` status check, strict up-to-date branches
(a PR must be current with `main` before merge, so it cannot land stale and break the trunk), and
linear history. Force-push and deletion of `main` are blocked.
