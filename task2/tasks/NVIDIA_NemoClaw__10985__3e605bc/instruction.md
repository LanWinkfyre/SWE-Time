# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Generic catch in gateway readiness checks swallows the real error behind "could not be collected safely"

## Summary

`src/lib/readiness/gateway.ts` wraps `observeManagedGateway()` (and a similar externally-supervised attachment probe) in a bare `try { ... } catch { return { ..., failure: "...could not be collected safely" } }`. Any underlying exception — a missing binary, a permission error, an actual bug — collapses to the same generic, unhelpful message, with no indication of what command or error actually failed.

This made a real bug (filed separately as #10984) very hard to diagnose: onboarding reported three failed capabilities with a one-line summary that gave no signal it was actually a `docker: command not found` failure underneath. Finding the cause required reading source, not anything onboarding itself surfaced.

## Suggestion

Preserve at least the caught error's message (or a redacted form of it) as evidence attached to the finding, instead of discarding it. This doesn't need to expose raw stack traces to end users — even the failing command name or error code (e.g. `ENOENT`) would have made this diagnosable without reading source.

## Where

`src/lib/readiness/gateway.ts` — the `try/catch` around `observeManagedGateway(owner)`, and the similar attachment-probe catch above it.

## Related

Surfaced while investigating #10891/#10900 and the bug reported in #10984.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3e605bc55b4a660b03bf1e132bdd9725078e346c`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "NVIDIA_NemoClaw__10985__3e605bc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
