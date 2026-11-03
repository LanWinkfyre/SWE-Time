# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Route session export and onboarding downloads through the transfer adapter

## Outcome

Migrate the remaining session-export and onboarding-token downloads to the typed asynchronous OpenShell transfer boundary introduced by #11496. Preserve existing contents, validation, permissions, failure results, and cleanup.

## Accepted scope

Decision: Accept, carrying forward capability slice 2 from the accepted #9810 plan. These consumers are explicitly outside #11496 under #9802's partial-delivery rule. Accountable maintainer and implementation owner: @rsliter.

The reason is completion of the existing transfer adapter migration. Transport construction and process handling belong in `src/lib/adapters/openshell/`; export formats, config parsing, private artifacts, and recovery decisions stay with their current owners. No new integration, transport, credential model, or public guarantee is introduced.

## Consumers and acceptance evidence

- All three download paths in `src/lib/actions/sandbox/sessions/export.ts`: directory, tar, and JSONL. Preserve session identifier validation, archive construction, contents, destination handling, private permissions, manifests, artifact verification, and cleanup warnings.
- `fetchGatewayAuthTokenFromSandbox` in `src/lib/onboard/dashboard.ts` and its asynchronous callers. Keep the downloaded config in the existing private temporary directory and the token in caller memory. Failed transfer, missing file, or invalid config retains the existing failure result. Preserve the documented best-effort cleanup limitation.
- Await complete work before releasing lifecycle locks or owned resources. Use typed consumer fakes for decisions and real filesystem tests for private artifact custody and cleanup after partial failure. Run focused checks, CLI type checking, local review, and PR validation.
- Preserve each consumer's existing output policy. Never include credential values or downloaded payloads in typed results or adapter-generated diagnostics. Do not add mutation retries, rollback, universal size limits, or transfer deadlines.

## Dependencies and completion

Depends on #11496's user-transfer boundary. Refresh the production consumer inventory at implementation time. Link the implementation PR and evidence here and record final consumer disposition in #9813. #9810 remains the originating capability issue; this follow-on owns the implementation listed above.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5310ad0a5c25d49f06910525456ea2529506b3ae`.  There
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
{"case_id": "NVIDIA_NemoClaw__11497__5310ad0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
