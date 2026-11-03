# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
Docs: Getting Started eval.yaml example is missing required `executor` property

## Summary
The Getting Started docs include an `eval.yaml` example that omits the required `executor` property. Running the example command fails with:

```pwsh
waza-test azd waza run -v
unknown engine type:
```

## Affected docs
- https://microsoft.github.io/waza/getting-started/
- Section shown in screenshot: **Step 6: Configure Your Evaluation**

## Problem details
The YAML snippet in the docs currently shows fields like `name`, `description`, `skill`, `version`, and `config`, but does not include `executor`.
Without `executor`, the runtime cannot determine the engine and returns `unknown engine type:`.

## Expected behavior
The Getting Started example should include a valid `executor` value so the sample runs successfully as written.

## Suggested fix
- Update the Step 6 `eval.yaml` sample to include the required `executor` property.
- Optionally add a short note that `executor` is required and what values are supported.
- Verify the exact command in the guide (`waza-test azd waza run -v`) succeeds after following the documented steps.

## Repro steps
1. Follow https://microsoft.github.io/waza/getting-started/.
2. Use the `evals/code-explainer/eval.yaml` snippet shown in Step 6.
3. Run:
   ```pwsh
   waza-test azd waza run -v
   ```
4. Observe error:
   ```
   unknown engine type:
   ```

![Getting Started screenshot highlighting missing executor in eval.yaml example](https://github.com/user-attachments/assets/6afe1381-9e1b-47f1-a567-473bbe707fff)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8486619e48a4ed308e24ac5709d323c2c2928d6a`.  There
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
{"case_id": "microsoft_waza__436__8486619",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
