# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
trace: ambiguous star-collision exports are indistinguishable from a missing symbol

Tracing a name that a barrel exposes through two colliding `export *` sources reports it as if the barrel never exported it. The output is byte-identical to tracing a name that genuinely does not exist, so a consumer cannot tell "this export is ambiguous and therefore unusable" from "you typed the wrong name".

**Reproduction**

```ts
// src/left.ts
export const Widget = 1;
// src/right.ts
export const Widget = 2;
// src/barrel.ts
export * from "./left";
export * from "./right";
// src/main.ts
import { Widget } from "./barrel";
```

```
$ fallow trace src/barrel.ts:Widget --format json --quiet
{"symbol_found":false, ...,"reason":"symbol not found as an export of this file; chains are file-scoped best-effort and may be empty",
 "callers":[{"file":"src/main.ts","imported_as":"Widget",...}]}

$ fallow trace src/barrel.ts:DoesNotExist --format json --quiet
{"symbol_found":false, ...,"reason":"symbol not found as an export of this file; chains are file-scoped best-effort and may be empty"}
```

Same verdict, same reason string. The ambiguous case is arguably the more interesting one: it still lists `src/main.ts` as a caller, so the trace simultaneously says the symbol is not an export and that something imports it.

**Why it matters**

Ambiguity is a real, actionable state. Per the spec a name supplied by two different star sources does not exist as an export, which is exactly the kind of subtle breakage a trace should surface loudly. Reporting it as an unknown symbol sends the user looking for a typo instead of at the colliding barrel.

**Suggested shape**

Distinguish the resolution states in the trace output rather than collapsing both to `symbol_found: false`: keep `symbol_found` for the unknown-name case and add an explicit ambiguity signal naming the colliding origins, so consumers can branch on it. The effective export index already models this as `EffectiveExportResolution::Ambiguous`; the information is available at the point where the trace gives up.

Found while reviewing #2210, which introduced the ambiguity distinction in the graph layer.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8b32aa4f6a285d1ae6897986f99dde834ecb7579`.  There
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
{"case_id": "fallow_rs_fallow__2262__8b32aa4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
