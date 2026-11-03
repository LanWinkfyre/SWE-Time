# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Agent-docs generator v2: generate cli-reference.md flags tables (needs a column-mapping spec)

Follow-up to #1188. v1 (scripts/generate-agent-docs.mjs) generates the SKILL.md commands, issue-types, and MCP-tools tables from the `fallow schema` manifest with merge semantics. The per-command flags tables in the skills `references/cli-reference.md` were deliberately deferred because a mechanical splice from `schema.commands[].flags` would produce structurally wrong tables:

- The curated `dead-code` section splits its 20 issue-type filter flags into a separate `### Issue Type Filters` sub-table, while the schema carries them inline on the command.
- The curated tables list relevant GLOBAL flags (`--format`, `--workspace`, `--changed-since`, `--production`, `--max-file-size`) inline per command; the schema keeps them in `global_flags`.
- The curated `dead-code` table documents combined-mode-only overrides (`--dupes-mode`, `--dupes-threshold`) that are not on the schema's dead-code command at all.
- Several curated flag descriptions are richer than the clap help text the schema carries; replacing them wholesale loses curation (the v1 merge-semantics answer: identity columns generated, description cells hand-owned, applies here too).

Scope for v2:

1. Write an explicit per-command column-mapping spec first: which schema flags land in which marker (`generated:flags:<command>`, `generated:flags:global`, a separate `generated:flags:dead-code-filters`), how global flags are referenced (link to the global table rather than duplicating), and what happens to combined-mode override rows.
2. Extend the generator with the flags-table renderers using the same merge semantics (Flag | Type | Default identity columns regenerated; Description hand-owned, seeded from clap help).
3. Once the tables generate, consolidate the release flow's step-10c flag-coverage grep into the generator's --check (one authoritative gate instead of two that can disagree).

Size: M.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4e35d2b50c84318d3bda4b1f634fc61695fe6beb`.  There
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
{"case_id": "fallow_rs_fallow__1189__4e35d2b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
