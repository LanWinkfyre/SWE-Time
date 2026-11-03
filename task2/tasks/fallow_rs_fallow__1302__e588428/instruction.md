# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Support (and optionally enforce) a reason on `fallow-ignore-*` suppressions (a la Biome)

### Problem

Fallow has `stale-suppressions` (flags a suppression that no longer matches an active issue), but no way to record or require *why* a suppression exists. Biome requires a reason on its suppressions — `// biome-ignore lint/rule: <reason>` is a parse error without the `: <reason>`, and the suppression doesn't apply. We'd like parity for `fallow-ignore-*`.

### Proposed solution

1. A documented inline-reason syntax for `fallow-ignore-next-line` / `fallow-ignore-file` / `@expected-unused` — e.g. `// fallow-ignore-next-line <rule> -- <reason>` or trailing free text after the rule name — that fallow records and surfaces.
2. An optional rule (e.g. `require-suppression-reason`) that fails when a suppression carries no reason, mirroring Biome's mandatory-reason behavior.

### Alternatives considered

A repo-local lint script (`scripts/lint-fallow-ignore-justification.ts`, wired into lefthook + CI) requires a rationale comment directly above each `fallow-ignore-*` directive. Native support would let us drop the workaround.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e588428bc570a98397ea182e069e72b07bd52811`.  There
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
{"case_id": "fallow_rs_fallow__1302__e588428",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
