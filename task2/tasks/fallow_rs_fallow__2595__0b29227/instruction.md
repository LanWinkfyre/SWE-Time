# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
license refresh: fall back to FALLOW_API_KEY when the stored JWT is stale

`fallow license refresh` only ever sends the locally stored JWT as the bearer token (`refresh_active_license` in `crates/cli/src/license/mod.rs`). The cloud refuses a token that is more than 45 days past expiry with `token_stale`, and `fallow license activate --trial` returns 409 for an organisation that is already on a paid tier. A paying user who has not run the CLI for 45 days therefore has no way back in from the CLI: the only recovery is to call `POST /v1/auth/license/refresh` by hand with a full-access API key as the bearer, which the server already accepts.

### What to do

1. In `refresh_active_license`, when the stored JWT is missing or the server answers `token_stale`, retry with `FALLOW_API_KEY` (or `--api-key`) as the bearer if one is set. The response shape is the same.
2. When neither works, print the actual recovery path instead of the trial hint: "set FALLOW_API_KEY to a full-access key and run `fallow license refresh` again".
3. Unit-test the fallback order (stored JWT first, API key second) and the error text.

### Acceptance

- With an expired JWT and a valid `FALLOW_API_KEY`, `fallow license refresh` succeeds and stores the new JWT.
- Without either, the error names the API-key route rather than the trial flow.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0b2922747231a43c269b2e555e0f366f6025e294`.  There
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
{"case_id": "fallow_rs_fallow__2595__0b29227",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
