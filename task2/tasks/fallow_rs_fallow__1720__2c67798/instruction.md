# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Make deep CSS audit the default with opt-out controls

## Problem

`fallow audit` now has CSS styling findings, but deep CSS context is still gated behind `--css-deep`. That keeps default audit cheap, but it also means audit can miss the higher-value styling findings that need project context: unused theme tokens, unreferenced classes, undefined keyframes, near-duplicate theme tokens, and changed-anchor filtering from a project-wide CSS scan.

If styling should feel as first-class as TypeScript and JavaScript in audit, deep CSS probably needs to become the default audit behavior once we have the right controls.

## Proposed direction

Make deep CSS audit the default, with explicit opt-out controls:

- CLI: keep `--css-deep` as a compatibility alias during transition, add a clear opt-out such as `--no-css-deep` or `--css-scope changed`.
- Config: add an audit-level setting so teams can choose `off`, `changed`, or `deep`.
- MCP: keep `css_deep` accepted, but align default behavior with CLI audit.
- Output: keep audit output narrowed to changed anchors so default deep mode does not become a whole-project cleanup dump.
- Performance: add a timing guard or documented fallback for very large repos.

## Acceptance criteria

- `fallow audit` runs deep CSS by default when CSS analysis is enabled.
- Users can opt out from CLI and config.
- JSON, human, SARIF, CodeClimate, markdown, and MCP behavior stay consistent.
- The changed-file audit output remains scoped and does not report unrelated whole-project styling cleanup by default.
- Existing `--css-deep` users are not broken.
- Add a real-project smoke covering a large Tailwind/design-system repo and a fixture-heavy compiler/tooling repo.

## Notes

This is probably the right long-term default, but it should land after opt-out/config/perf controls exist, not as a blind default flip.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2c67798f2629db09e82117ce345130c1c822bf6d`.  There
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
{"case_id": "fallow_rs_fallow__1720__2c67798",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
