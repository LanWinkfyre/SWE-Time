# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-dependencies: binary after `varlock run -- <bin>` in package.json scripts is not credited

### What happened?

`fallow dead-code` reports a devDependency as unused when its binary is only invoked behind `varlock run ... -- <bin>` in a package.json script. Other `--` passthrough wrappers are handled: the same binary behind `dotenv -- <bin>` is credited, and the same binary at command position is credited.

[varlock](https://varlock.dev) (`varlock run [options] -- <command>`) is an env loader that follows the usual "options, then `--`, then the real command" wrapper convention, like `dotenv-cli`, `cross-env` and `env-cmd`, so it should credit the command that follows `--`.

```
● Unused devDependencies (1)
  is-ci
  Listed in devDependencies but never imported or referenced — https://docs.fallow.tools/explanations/dead-code#unused-dependencies
```

### Reproduction

1. `package.json`:

   ```json
   {
     "name": "fallow-repro",
     "private": true,
     "type": "module",
     "scripts": {
       "ci": "varlock run -- is-ci"
     },
     "devDependencies": {
       "dotenv-cli": "^8.0.0",
       "is-ci": "^4.1.0",
       "varlock": "^1.18.0"
     }
   }
   ```

2. `pnpm install`
3. `fallow dead-code` → `is-ci` is reported as an unused devDependency.

Control cases, changing only the `ci` script:

| script | result |
| --- | --- |
| `is-ci` | credited, no issues |
| `dotenv -- is-ci` | credited, no issues |
| `varlock run -- is-ci` | **`is-ci` reported unused** |
| `varlock run -p ./env/ -p ./env/.env.schema -- is-ci` | **`is-ci` reported unused** |

`varlock` itself is credited in every case, so the wrapper is recognised as a binary; it is the command after `--` that is dropped.

### Expected behavior

A binary that appears after `varlock run [options] --` in a script is credited the same way it is after `dotenv --`, or at command position. More generally, `<declared-bin> [options] -- <command>` could be treated as a passthrough for any declared binary, which would cover this and similar env-loading wrappers without a per-tool list.

### Fallow version

3.22.0

### Operating system

macOS

### Configuration

No `fallow.toml` or `.fallowrc.json` in the reproduction (defaults). The same result occurs in a pnpm workspace with a `.fallowrc.json` that only sets `rules` severities.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3f062cf9f5b08c2747aff0bd73f4a3c458e0bb98`.  There
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
{"case_id": "fallow_rs_fallow__2551__3f062cf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
