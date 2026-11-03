# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Combined-mode JSON envelope drops analysis-stage workspace diagnostics

`fallow dead-code --format json`, `fallow check --format json`, and `fallow health --format json` carry analysis-stage workspace diagnostics, but the bare combined run (`fallow --format json`, check plus dupes plus health) does not. The stderr warning still prints once, so the JSON consumer is the only one left in the dark.

Affected kinds: `malformed-pnpm-workspace-yaml` and `bun-lockb-override-resolution-skipped` (added in #2362).

## Reproduction

`package.json` with `"overrides": { "ws": "^8.21.0" }`, a `bun.lockb` next to it, no other lockfile, and a `src/index.ts`.

- `fallow dead-code --format json --quiet`: `workspace_diagnostics[0].kind == "bun-lockb-override-resolution-skipped"`; `check` and `health --format json` carry it too.
- `fallow --format json --quiet`: no `workspace_diagnostics` key at the top level and none under `check`; stderr still prints the warning once.

A malformed `pnpm-workspace.yaml` behaves the same way.

## Causes (both pre-existing)

1. `serialize_combined_check_json` in `crates/api/src/combined_output.rs` passes `workspace_diagnostics: Vec::new()` unconditionally to `serialize_check_json_payload`, and the combined dupes and health serializers never read the diagnostics registry. A diagnostic that survives in the registry never reaches the combined envelope.
2. Every per-analysis config reload calls `stash_workspace_diagnostics` (`crates/config/src/workspace/diagnostics.rs`), which replaces the registry set and preserves only `is_source_discovery()` kinds, so diagnostics recorded by the analyze stage through `record_workspace_diagnostics` are wiped between sections. Fixing (2) alone is not enough because of (1).

Related: long-lived engine sessions (LSP, MCP) keep a stale analysis-stage entry until a config reload, because `clear_source_discovery_diagnostics` only clears source-discovery kinds at walk start.

## Proposed shape

- Add an analysis-stage classification on `WorkspaceDiagnosticKind` for both kinds above and preserve it in `stash_workspace_diagnostics` the way source-discovery kinds are preserved.
- Clear stale analysis-stage entries at the start of each analyze pass (mirror of `clear_source_discovery_diagnostics`) so watch-mode and engine reruns drop the diagnostic once the YAML is fixed or a text `bun.lock` exists.
- Have the combined check section read the registry instead of passing an empty vector.
- Tests for combined mode, watch mode, and an engine session.

Surfaced while reviewing #2362 (the fix for #2358).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `969689e6de5675acebfdffd6e0538bc9e56372eb`.  There
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
{"case_id": "fallow_rs_fallow__2366__969689e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
