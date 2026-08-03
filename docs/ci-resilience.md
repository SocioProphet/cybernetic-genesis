# CI resilience — fail-closed, declaratively enforced, no blind spots

The repo's teeth (`tools/validate.py`, `verify_mount_strategy.py`, `verify_deploy_*`, the pytest
suites) already exit non-zero on any violation. This document is about making that enforcement
**unbypassable and reproducible**, not advisory — and about doing red-main *detection* where it
can actually be watched (the estate plane), not in a per-repo blind spot.

## The gaps this closes

1. **Stacked-PR blind spot.** `on.pull_request.branches: [main]` only validated PRs whose *base*
   was `main`. A stacked PR (base = another feature branch) merged into its base with **zero repo
   CI**, and was only ever validated once it happened to reach `main`. Fixed: `pull_request` now
   fires for **any** base branch, plus `merge_group` (merge queue) and `workflow_dispatch`.
2. **Advisory, not required.** `main` had no branch protection — the teeth ran but nothing forced
   them green before a merge. Fixed by requiring the **`CI gate (fail-closed aggregate)`** status
   check on `main`.
3. **Protection was imperative, not IaC.** It was first applied with a one-shot `gh api PUT` —
   invisible, undriftable, unreproducible. Fixed by committing the spec and reconciling it from the
   estate plane (below).

## Fail-closed aggregate gate

`ci-gate` `needs: [selftest]`, runs `if: always()`, and **explicitly asserts** every required job
`== success`. A skipped, cancelled, or failed teeth job fails the gate — you cannot merge on a
check that merely "didn't run red". Branch protection requires this one context, so adding a new
teeth job in future only widens enforcement (wire it into `ci-gate.needs`); it can never silently
narrow it. Top-level `permissions: contents: read`; superseded PR runs are cancelled by
`concurrency`, trunk pushes never are.

> **The required-check name is a frozen contract.** Branch protection requires the context string
> `CI gate (fail-closed aggregate)`. Renaming the `ci-gate` job's `name:` silently un-gates `main`
> (or wedges it). Do not rename it without updating `.github/branch-protection.main.json` in the
> same change.

## Branch protection is declarative (IaC), reconciled org-wide

`.github/branch-protection.main.json` is the **source of truth** for `main`'s protection (the exact
classic-protection API body). It is not applied by a bespoke per-repo workflow — privileged
GitHub-settings changes are an **estate-wide** operation run from `git-ops-standards` with a minted
GitHub App token (never a PAT — control `ci-secrets-minted-never-static-pat`), the same pattern as
`estate-ci-health`:

- the estate **`estate-branch-protection`** workflow (in `git-ops-standards`) reads each repo's
  committed spec, **detects drift** against live protection (control `main-branch-protection-enforced`),
  and **reconciles** on a deliberate `workflow_dispatch` (never a blind scheduled auto-mutation).

To apply by hand as an admin (e.g. bootstrapping, or after break-glass):

```bash
gh api -X PUT repos/SocioProphet/cybernetic-genesis/branches/main/protection \
  --input .github/branch-protection.main.json
```

The org is **not** on GitHub Team, so org/repo *rulesets* are unavailable; classic protection is
codified here. Migrate the spec to a ruleset if the tier changes.

## Red-main detection is estate-wide, not a per-repo watcher

An earlier revision added a per-repo scheduled plumb-line + auto-filed drift issue. It was
**removed**: the estate already scans every first-party repo's default-branch CI conclusion
org-wide from `git-ops-standards` (`estate-ci-health`, control `github-ci-health-current`), and that
scan — hosted in an actively-maintained repo — keeps watching this repo **even when it goes
dormant**. A per-repo `schedule` would be disabled by GitHub after 60 days of inactivity, i.e.
exactly when its rot-detection would matter; while active, the org-wide scan already sees this
repo's fresh PR/push runs. A per-repo watcher was therefore redundant when active and dead when
dormant, and re-created the very anti-pattern of incident `2026-08-02-silent-ci-failures`.

## Break-glass (the fail-closed gate must not wedge)

Protection sets `enforce_admins: true` — even admins need a green gate and an up-to-date branch,
and cannot force-push `main`. If the required check can never report (a GitHub Actions outage, or an
accidental `ci-gate` rename) `main` can become unmergeable, including for the fix that restores CI.
To break glass (admin only, minimal window):

```bash
# temporarily let admins bypass, land the fix, then RE-ASSERT from the committed spec:
gh api -X DELETE repos/SocioProphet/cybernetic-genesis/branches/main/protection/enforce_admins
# ... merge the restoring change ...
gh api -X PUT repos/SocioProphet/cybernetic-genesis/branches/main/protection \
  --input .github/branch-protection.main.json
```

Leaving protection relaxed is itself drift — `estate-branch-protection` will flag it until the spec
is re-applied.
