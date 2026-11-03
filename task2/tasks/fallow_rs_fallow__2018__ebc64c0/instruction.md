# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Conditional dependency crediting for style preprocessors

The table half of this issue shipped in #2059: `(plugin, config key path, config value) -> credited packages` now lives in a data file next to `crates/core/data/tooling.toml`, and the three hardcoded arms (jsdom/canvas, edge-runtime, lightningcss) were migrated onto it behaviour-neutrally. The squash commit carried a closing keyword and closed this issue early; what follows is the part that is still open.

### The harder case: style preprocessors

`less`, `stylus` and `sugarss` are reported unused in a Vite project that imports `src/app.less`, and `fallow fix` will delete them, breaking the build. The obvious fix, adding them to `tooling.toml` next to `sass`, is a regression rather than a fix: a project declaring `sass` with zero stylesheets reports nothing today, so those catalogue rows already hide genuinely unused deps.

The right shape is conditional crediting keyed on what the module graph actually contains: credit `less` when a `.less` file is reachable, `stylus` on `.styl`/`.stylus`, `sugarss` on `.sss`. A plugin-level filesystem probe is simpler but over-credits on a stray unimported file; a post-graph credit hook keyed on extensions present in the resolved graph is correct but new machinery.

Two decisions to make before implementing:

- probe versus post-graph hook, given the over-crediting risk of the first and the new machinery of the second
- whether the unconditional `sass` and `sass-embedded` rows migrate to the conditional mechanism as well, which would newly flag projects that declare sass and have zero stylesheets

### Explicitly not a general rule

"An installed optional peer of a used package is credited" removes these false positives but would hide genuinely unused code on a large scale: `vite` alone declares twelve optional peers (`@types/node`, `esbuild`, `jiti`, `less`, `lightningcss`, `sass`, `sass-embedded`, `stylus`, `sugarss`, `terser`, `tsx`, `yaml`), so every Vite project would silently exempt all twelve. It would also require deleting `optional_peer_dependency_of_used_package_is_still_flagged_when_unused`, which is precisely the invariant keeping this conservative.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ebc64c0c5a600e97d712fd369859b1a05c9a0c60`.  There
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
{"case_id": "fallow_rs_fallow__2018__ebc64c0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
