# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
GGUF thinking probe overrides explicit reasoning.disable config

## LocalAI version
- reproduced on current `master` as of 2026-04-21

## Environment
- GGUF model
- `llama-cpp` backend
- `template.use_tokenizer_template: true`
- reasoning-capable model where backend `ModelMetadata.SupportsThinking=true`

## Describe the bug
`reasoning.disable` and `reasoning.disable_reasoning_tag_prefill` are documented LocalAI model config options, but explicit YAML values are not respected on the GGUF tokenizer-template path.

After model load, `DetectThinkingSupportFromBackend(...)` overwrites explicit reasoning config using backend metadata, so a model config such as:

```yaml
template:
  use_tokenizer_template: true
reasoning:
  disable: true
  disable_reasoning_tag_prefill: true
```

can end up at runtime as:
- `reasoning.disable: false`
- `reasoning.disable_reasoning_tag_prefill: false`

This is visible through `/api/models/config-json/<model>` even though `/api/models/edit/<model>` still shows the original YAML.

There is a second related problem in the same path: the runtime only probes backend thinking metadata when *both* reasoning fields are nil. That means partial explicit config (for example only `reasoning.disable: true`) cannot preserve the explicit field and still infer the missing sibling default.

## Related context
These are related but not duplicates:
- #7944 tracks prior thinking-model handling issues
- #8036 tracks reasoning-content / OpenAI compatibility issues
- #8595 improved thinking-model support around tokenizer-template paths

This issue is narrower: it is specifically about **reasoning config precedence and probe gating** on the GGUF tokenizer-template path.

## To reproduce
1. Configure a GGUF model with `backend: llama-cpp` and `template.use_tokenizer_template: true`.
2. Set explicit reasoning config in YAML:

```yaml
reasoning:
  disable: true
  disable_reasoning_tag_prefill: true
```

3. Load the model.
4. Compare:
   - `/api/models/edit/<model>`
   - `/api/models/config-json/<model>`
5. Observe that runtime config flips the explicit reasoning values back based on backend metadata.

## Expected behavior
Explicit YAML reasoning settings should win.
Backend thinking probe should only fill defaults for fields that are still unset.

## What I verified
- The feature is officially documented in LocalAI model configuration docs (`reasoning.disable` plus request-level metadata override).
- The code path exists today in:
  - `pkg/reasoning/config.go`
  - `core/backend/options.go`
  - `core/config/gguf.go`
  - `core/backend/llm.go`
- I reproduced the bug in a live distributed deployment and confirmed that runtime `config-json` changed from explicit `disable: true` to `disable: false` before the fix.
- After patching:
  - explicit runtime config is preserved
  - package tests pass
  - minimal runtime diagnostics improve materially

## Proposed fix
1. In `core/config/gguf.go`, only write inferred reasoning values when the target field is `nil`.
2. In `core/backend/llm.go`, run the thinking probe when tokenizer templates are enabled and **either** reasoning field is unset, not only when both are unset.

## Validation
I prepared a fix with targeted tests for:
- respecting fully explicit reasoning config
- filling defaults when unset
- supporting partial explicit / partial inferred behavior on the real runtime gate
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `47efaf5b435fc90e24ca0a4dd8587d386d67e566`.  There
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
{"case_id": "mudler_LocalAI__9462__47efaf5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
