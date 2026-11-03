# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] IncrementalTokenizer builds the wrong tokens.full NestedKey on step

## Describe the bug

On `_step`, `IncrementalTokenizer` reuses `tokens.full` as the next prompt. The lookup is:

```python
tokens_full_key = (
    (self.tokens_key[0], "full")
    if isinstance(self.tokens_key, tuple)
    else "tokens_full"
)
```

- `tokens_key="tokens"` looks for `"tokens_full"`, not `("tokens", "full")` (what the wrappers write).
- `tokens_key=("obs", "tokens", "prompt")` looks for `("obs", "full")`, not `("obs", "tokens", "full")`.

Existing `test_custom_keys` only covers reset, not this reuse path.

## Expected behavior

`tokens_full_key` should replace the last component of `tokens_key` with `"full"`, for both string and NestedKey inputs. `_step` should copy that tensor onto `tokens_key` without re-tokenizing when it is present.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the documentation (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `46c5daee9e28e47560a6adfa839a5ce0d9176e25`.  There
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
{"case_id": "pytorch_rl__4344__46c5dae",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
