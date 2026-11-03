# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
health: per-function threshold overrides (configurable ceilings instead of binary suppression)

## Problem

`health` thresholds (`maxCyclomatic` / `maxCognitive` / `maxCrap`) are global. Some functions are legitimately above the standard thresholds (e.g. a linear module-assembly entry point), but the only escape hatches today are binary:

- `// fallow-ignore-next-line complexity` hides the finding forever — if the function later grows from cognitive 18 to 35, no signal fires;
- `health.ignore` globs drop whole files;
- health baselines store per-file finding *counts*, so a baselined function that gets worse stays invisible;
- `overrides[].rules` only adjusts severities of dead-code-family rules, not thresholds.

For agent-driven workflows this matters a lot: we want a deterministic verdict ("blocked / not blocked") so the agent never has to re-judge whether a finding is "real". A sanctioned exception should be a *number*, not an off switch — if the function exceeds its agreed ceiling, the gate must fire again.

In #119 configurable severity thresholds were explicitly "deferred to a follow-up based on user demand" — consider this that demand, one level deeper (per-function).

## Proposal

Per-function/per-path threshold overrides in config, e.g.:

```jsonc
{
  "health": {
    "maxCognitive": 15,
    "overrides": [
      {
        "files": ["components/auth/src/index.ts"],
        "functions": ["createAuthModule"],   // optional; omit = whole file
        "maxCognitive": 25,
        "reason": "linear module assembly; agreed 2026-06"
      }
    ]
  }
}
```

Desired semantics:

- a finding matching an override is gated against the override's thresholds instead of the global ones;
- an override whose function no longer exceeds the *global* thresholds is reported as stale (same spirit as `stale-suppressions`), so the table can't rot;
- `audit` respects the overrides in its health sub-analysis.

## Workaround we use today

A ~150-line wrapper script that runs `fallow audit` + `fallow health --format json` and applies a `path#functionName -> ceilings` table, including the stale check. It works, but it re-implements gating that conceptually belongs in fallow, and drifts from fallow's own file classification.

Happy to provide more detail or test a prototype.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9618e15c326f4202aa00b43e78a8c418c43edf84`.  There
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
{"case_id": "fallow_rs_fallow__1206__9618e15",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
