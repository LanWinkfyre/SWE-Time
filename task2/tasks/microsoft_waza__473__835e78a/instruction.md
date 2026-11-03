# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
ci: validate site builds on pull requests

## Summary

Add PR-time validation for the documentation site so changes under `site/**` cannot merge with all required checks green while the Pages build is untested until after merge.

## Why

During PR cleanup, site dependency PRs (#446, #462, #468) showed that the required PR checks validate Go and the dashboard, but not the Starlight docs site. The Pages workflow does run `npm ci` and `npm run build`, but only on `push` to `main`, which means a broken site dependency update would be detected after merge.

## Suggested approach

- Add a `site` build job to an always-reporting PR workflow, or use a path-filter setup with a skip-shim job so required checks do not deadlock on PRs that do not touch `site/**`.
- Mirror the existing `/web` validation pattern where possible.
- Run at least `cd site && npm ci && npm run build`; consider adding the existing site Playwright e2e tests as a follow-up or optional job.

## Acceptance criteria

- PRs touching `site/**`, `package-lock.json`, or site workflow/config files validate the docs site before merge.
- Non-site PRs still report a successful/skipped site check if the check is required.
- Dependabot site PRs get the same signal before merge that Pages currently provides only after merge.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `835e78a7a94967399178bcfcab935f52ce45935e`.  There
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
{"case_id": "microsoft_waza__473__835e78a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
