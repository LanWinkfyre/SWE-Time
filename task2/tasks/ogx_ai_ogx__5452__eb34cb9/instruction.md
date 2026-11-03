# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Wire up service_tier parameter in vertexai inference provider

### 🚀 Describe the new functionality needed

The vertexai inference provider currently ignores the `service_tier` parameter with a warning. As of google-genai v1.69.0, the Gemini API supports service tier configuration (`FLEX`, `STANDARD`, `PRIORITY`) through `GenerateContentConfig.service_tier`. The lockfile already pins google-genai at v1.70.0, so no dependency change is needed.

The provider should map OpenAI `service_tier` values to Gemini equivalents and pass them through to the SDK instead of dropping them.

### 💡 Why is this needed? What if we don't build it?

Without this, users cannot select Gemini's FLEX tier (lower cost, higher latency) or PRIORITY tier (lower latency) when using the vertexai backend. The `service_tier` parameter is silently ignored, which is surprising when other providers honor it. FLEX in particular is useful for batch-like workloads where cost matters more than latency.

### Other thoughts

Mapping: `auto` is omitted (let the API decide), `default` maps to Gemini's `standard`, `flex` and `priority` pass through directly. Gemini does not echo the tier back in responses, so the response-level `service_tier` field will remain `None` (the Responses layer already defaults this to `"default"`).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `eb34cb947c21aa40d1c5adf8a0dcf94ba63f01c7`.  There
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
{"case_id": "ogx_ai_ogx__5452__eb34cb9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
