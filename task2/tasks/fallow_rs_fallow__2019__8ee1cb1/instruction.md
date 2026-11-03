# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Extend CLI flag-value dependency crediting with an explicit convention table

#2006 credits packages named as eslint `--format` values. Other CLIs follow the same pattern, where a flag value names an npm package that has no other reference in the project.

Recommended rows, each with its own fixture, added one at a time:

- eslint `--plugin` (prefix `eslint-plugin-`, no built-ins, safest of the set)
- jest `--testEnvironment`, `--runner`, `--reporters`, `--preset` (jest-resolve tries the prefixed name then the plain one, so credit both candidates; built-ins `node`, and `default` / `github-actions` for reporters)
- node / tsx / ts-node `-r`, `--require`, `--loader`, `--experimental-loader`, `--import` (verbatim; skip values starting with `.` or `/` and `node:` built-ins)
- mocha `--reporter` / `-R` and `--require` / `-r`
- prettier `--plugin` (verbatim; prettier does not auto-prefix)
- stylelint `--custom-syntax`
- postcss `--use`

Explicitly out of scope:

- eslint `--rulesdir` and `--resolve-plugins-relative-to` (directory paths, not packages)
- stylelint `--formatter` (no `stylelint-formatter-*` naming convention exists)
- nyc / c8 `--reporter` (the istanbul-reports built-in set changes over time)
- semantic-release and commitlint `--extends` (file-configured and already parsed)

And never a generic "any bare token matching a declared dependency" rule. A wrong credit produces no signal anywhere, it just makes a real finding vanish, and values like `--platform node`, `--target html` and `--env production` collide with real package names.

Blocked on #2016. Most projects invoke these through `npm run <script> -- --flag`, which is dropped before flag scanning even starts. That package-manager indirection is the part of #2016 that is still open, and it has to land first or this table reaches almost no real project.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8ee1cb14f4702b78c8102c2742a42f0e7ffc849a`.  There
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
{"case_id": "fallow_rs_fallow__2019__8ee1cb1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
