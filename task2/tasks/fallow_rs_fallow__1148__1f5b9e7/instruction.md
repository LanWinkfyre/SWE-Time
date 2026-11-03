# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
config: declarative custom rule packs (banned calls/imports, effect rules) without project-code execution

## Motivation

External plugins are intentionally declarative (entry points, always-used files, tooling deps, used exports, class members). There is no way for a team to encode a project-specific semantic policy that is too specific for an upstream plugin: ban this call from this area, require this wrapper around that call, forbid this effect in that zone.

## Hard constraint: no project-code execution

fallow must never execute the analyzed project's code. `fallow-core` / `extract` / `graph` ban `Command::new` via clippy, and the `safe_analysis` integration test enforces it. Any custom-check mechanism must preserve this: no loading or running project config, and no running arbitrary project JS/TS, in the default analyzer.

## Proposed phasing

- Phase 1: declarative JSON/JSONC rule packs (banned calls, banned imports, required wrappers, effect rules) with schema autocomplete. Matchers reuse the segment-aware callee patterns and, where relevant, the internal effect classification (#1143).
- Phase 2: optional out-of-process or WASM checks behind an explicit trust opt-in, never default-on. A frozen JSON IR is the boundary the guest sees.

This composes with boundary v2 (#1147): the boundary `calls` / `effects` sections are the project-architecture-scoped form of the same matchers; rule packs are the general per-rule form.

## Acceptance

- Phase-1 declarative rule pack format defined and schema'd, evaluated over existing extraction data (no project-code execution).
- At least banned-calls and banned-imports working end to end, with suppression and actions wired.
- A clear, documented trust boundary for any future Phase-2 executable checks.

Relates to: #1143 (effect rules), #1147 (boundary calls/effects share the matchers).

Size: L.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1f5b9e799c7e0cbee4556b6b5e33b6fab844212d`.  There
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
{"case_id": "fallow_rs_fallow__1148__1f5b9e7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
