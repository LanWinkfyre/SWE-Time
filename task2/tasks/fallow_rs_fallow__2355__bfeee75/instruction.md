# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Astro and MDX templates do not record JSX member-expression tag usage

#2348 fixed JSX member-expression tags (`<SC.Wrapper />`) for TS/JS/TSX extraction, but two template pipelines still miss them:

- **Astro**: `collect_astro_template_used_names` in `crates/extract/src/astro.rs` records only the tag root for component tags in `.astro` markup, so `<SC.Card />` credits `SC` as a bare name and the member access is never recorded. An entry-point `.astro` file with a namespace import keeps the pre-#2348 false positive shape.
- **MDX**: `crates/extract/src/mdx.rs` deliberately extracts only `import` and `export` lines, so JSX member tags in the MDX body are invisible to usage crediting entirely.

Both should record member accesses the way the JSX visitor now does, so namespace-imported exports rendered only in Astro or MDX markup are credited (and unused siblings can narrow instead of mark-all, matching #2348 semantics).

Surfaced during the review of #2352.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bfeee75e2d04e637a1bab843241eb988ebbe1f42`.  There
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
{"case_id": "fallow_rs_fallow__2355__bfeee75",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
