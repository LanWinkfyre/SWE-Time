# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
mcp/cli: unified target inspection (inspect_target) returning one evidence bundle per symbol/file

## Motivation

To act on a symbol safely (delete, rewrite, extract, harden), an agent today makes several separate calls: `trace_export`, `trace_file`, `trace_dependency`, `find_dupes` / `trace_clone`, `check_health`, `security_candidates`. There is no single "tell me everything about this target" entry point. The data already exists across these surfaces; what is missing is one composition.

## Proposed

A new read-only MCP tool `inspect_target` (and, later, a `fallow inspect` CLI verb) that takes a target and returns a compact evidence bundle composed from existing analysis:

- identity + source span, entry reachability, is-entry-point
- callers (graph reverse-deps) and callees / imports-from / imported-by
- exports declared; dependency / package / workspace context
- duplicate siblings touching the target (clone fingerprints)
- complexity + CRAP for the enclosing function
- runtime hot/cold state for the enclosing function when coverage is available
- security-candidate overlap on the same span
- safest action hints + relevant suppressions

## Addressing

- Symbol-keyed first: `file + export_name` and `file`. This matches the existing trace plumbing, which is symbol/file keyed, not line keyed (`trace_export` / `trace_file` / `trace_dependency` in `crates/mcp/src/server/mod.rs` take `file` + `export_name` / `file` / `package_name`, never `file:line`).
- `file:line` addressing is a follow-up. It needs a line-to-enclosing-symbol mapping; the complexity visitor already records function spans to build on.

## Scope notes

- MCP-first. A new top-level CLI command overlaps `--trace` / `--trace-file`; add the CLI verb only after the MCP tool proves the shape.
- v1 composes existing systems only (no new analysis pass). Richer proof objects (blocking effects, pure regions) come once the function-local relation layer (#1142) lands.

## Acceptance

- `inspect_target` returns a typed JSON bundle for a symbol target and a file target, composed from existing analysis.
- Listed in the MCP tool surface; telemetry tool-name allowlist updated.
- No new analysis pass in v1.

Relates to: #1142 (substrate for later proof objects).

Size: M.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e2d2dae4bc670c88a458b836f6946f53cb888ff8`.  There
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
{"case_id": "fallow_rs_fallow__1144__e2d2dae",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
