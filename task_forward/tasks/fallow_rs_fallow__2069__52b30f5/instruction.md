# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Unused dependency override not reported for npm

### What happened?

It seems fallow assumed only pnpm has dependency overrides. Npm does too. We have an unused dependency override in our package.json which is not reported by Fallow, while i did spot pnpm_overrides.rs as part of Fallow which does seem to do what could also be done for npm.

### Reproduction

- Check package.json in opensource repo: https://github.com/openfrontio/OpenFrontIO
- Notice it currently contains this override which was for use with lit-markdown in the past (we don't use lit-markdown anymore but the override for its subdependency was left in so far): ```"overrides": {
    "sanitize-html": ">=2.17.4"
  },```
- Run Fallow on the repo and notice it won't report an unused dependency override. I think Fallow would have reported it when we would have used PNPM instead of NPM.

### Expected behavior

Report the dependency override for 'sanitize-html' as unused

### Fallow version

3.10.0

### Operating system

Windows

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `52b30f51ec5639ccbefec3bb9a130f5a8afd436a`.  There
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
{"case_id": "fallow_rs_fallow__2069__52b30f5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
