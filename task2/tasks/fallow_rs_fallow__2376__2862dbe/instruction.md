# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
MDX prose line starting with import is classified as a statement and drops every import of the file

`is_statement_start` in `crates/extract/src/mdx.rs` treats any trimmed line that starts with `import ` or `export ` as JavaScript. A prose sentence that begins with the word "import" is sent to the statement parser, the parse fails, and the file loses all of its imports, so the imported modules become unused files and nothing in the body is credited.

## Reproduction

Astro project with `src/pages/index.astro` rendering this MDX file:

```mdx
import * as NS from '../components/ns'

<NS.Star />

import the thing and render <NS.Moon /> here.
```

`src/components/ns.ts` exports `Star`, `Moon`, `Unused`. `fallow dead-code --no-cache --format json` reports `src/components/ns.ts` as an unused file (and therefore no unused export for `Unused`). Expected: `ns.ts` is used and only `Unused` reports. Reproduces identically on the pre-#2355 binary, so this is pre-existing.

## Direction

Require the candidate statement line to look like a real import or export (a source clause `from '...'`, a `{`, a `*`, a default specifier followed by `from`, or `export` followed by a declaration keyword) before classifying it, or parse the line and fall back to prose when it does not parse.

Surfaced while reviewing #2360 (the fix for #2355).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2862dbe4f96a2e801a576b63028da97c73b8f6b9`.  There
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
{"case_id": "fallow_rs_fallow__2376__2862dbe",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
