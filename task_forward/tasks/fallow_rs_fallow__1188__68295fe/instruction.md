# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Generate agent-facing docs (SKILL.md tables, llms.txt) from the fallow schema capability manifest

Since #1186, `fallow schema` emits a complete machine-readable capability manifest (`manifest_version: "1"`): all commands and flags (clap-derived), one `issue_types` row per registered rule across every analysis (with filter flags, fixability, parse-verified suppression comments, and free/freemium markings), an `mcp_tools` block backed by the shared manifest in `fallow-types` (drift-tested against the live tool router), a live-derived `plugins` block, and the user-facing environment variables.

The hand-maintained agent docs that describe the same surface can now be generated from it instead of drifting independently:

- The commands table, issue-types table, and MCP tools section in the bundled agent skill (`npm/fallow/skills/fallow/SKILL.md`, source of truth in the fallow-skills repo).
- The flags tables in the skills `references/cli-reference.md`.
- An `llms.txt` (and optionally `llms-full.txt`) for docs.fallow.tools, which currently has none.

Proposed shape:

1. A small generator (script or `cargo xtask`-style bin) that reads `fallow schema` output and renders the generated table sections between marker comments (`<!-- generated:issue-types:start/end -->`), so hand-written prose around them stays hand-written.
2. Wire it into the release flow where the npm skills copy is already refreshed, so generation happens at the same moment as vendoring.
3. A drift check that fails when the committed generated sections no longer match the manifest (regenerate-and-diff, same pattern as the existing codegen checks), so the tables cannot silently rot between releases.

Size: M. The manifest already carries everything the tables need; the work is the renderer, the markers in the existing docs, and the release-flow wiring.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `68295fee174c9c64bcdb371aeeb37076fd44631f`.  There
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
{"case_id": "fallow_rs_fallow__1188__68295fe",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
