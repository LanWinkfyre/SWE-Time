# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
[ui] React Router params are decoded twice, breaking percent-containing names

### Summary

React Router decodes matched path segments before exposing them through `useParams()`, but several React UI pages call `decodeURIComponent()` on those values again.

For a valid model name such as `rate%model`, navigating to `/app/backend-logs/rate%25model` produces the route parameter `rate%model`; decoding it again throws `URIError: URI malformed` and the page falls into the router error boundary.

Names containing a literal escape-like substring fail more quietly. For example, `model%20name` is encoded as `model%2520name`, correctly returned by `useParams()` as `model%20name`, then incorrectly changed to `model name` by the second decode. The UI can display or request the wrong resource.

### Affected pages

- Backend logs
- Per-node backend logs
- Model editor
- Skill editor

### Reproduction

1. Create or rename a model to `rate%model` (model names reject path separators, but `%` is allowed).
2. Open `/app/backend-logs/rate%25model` or `/app/model-editor/rate%25model`.
3. Observe the `URIError` / router error boundary instead of the requested model page.

A minimal route probe against the currently pinned React Router also demonstrates the behavior:

```text
name:  rate%model
path:  rate%25model
param: rate%model
extra decodeURIComponent(param): URIError: URI malformed
```

### Expected behavior

Pages should use `useParams()` values directly and encode them only when constructing a new URL or API path. Literal percent signs and escape-like substrings should be preserved exactly.

### Suggested fix

Remove the second decode at each affected page and add Playwright coverage for percent-containing parameters. The model editor API path must encode the already-decoded model name when constructing its request URL.

---

_This report and its reproduction were prepared with Codex assistance._
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bcf196da3e042640868d528335b25b3cd936df51`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__11882__bcf196d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
