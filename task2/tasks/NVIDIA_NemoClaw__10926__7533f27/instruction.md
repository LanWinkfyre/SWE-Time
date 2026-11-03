# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
perf(cli): reduce Hermes forward recovery subprocess and settlement overhead

## Outcome
Preserve the original scope of #10822 as a dedicated capability: reduce two-port Hermes forward restoration by replacing subprocess-heavy reachability and serial settlement with bounded shared observations.

## Parent
Subissue of #10822.

## Scope
- Additive forward list/parse/currentness/reachability/mutation/settlement/rollback timing.
- Bounded in-process localhost probes; TCP remains liveness only.
- Sequential fenced mutations and joint settlement of touched ports.
- Strict ownership parsing, healthy-port invariants, and reverse-order rollback.

## Acceptance
Use the detailed validation, compatibility, and security contract preserved in the parent issue history. PR #10828 provides the observability slice and should be reconciled with current main before later slices.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7533f279edeb9cd6d71117e8e65c364ef15cacab`.  There
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
{"case_id": "NVIDIA_NemoClaw__10926__7533f27",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
