# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
sglang backend: enable_thinking=false is dropped, and reasoning_content stays empty for <think>-prefilled templates

### LocalAI version

master (`backend/python/sglang/backend.py`, 592 lines as of this writing), sglang backend image built from the `latest` gallery entry (sglang 0.5.17).

### Environment, CPU architecture, OS, and Version

arm64 (NVIDIA Jetson-class / L4T, CUDA 13), sglang backend, a Qwen3-style MoE model with the stock Qwen3 chat template.

### Describe the bug

Two independent gaps in the sglang gRPC backend. Both have an already-merged upstream counterpart on the Go/llama.cpp side, so the fix direction is settled — the Python backend simply isn't wired into it.

---

#### 1. `enable_thinking: false` is silently dropped — thinking can only be switched *on*, never *off*

`core/backend/options.go` explicitly forwards both states:

```go
if c.ReasoningConfig.DisableReasoning != nil {
    if *c.ReasoningConfig.DisableReasoning {
        metadata["enable_thinking"] = "false"
    } else {
        metadata["enable_thinking"] = "true"
    }
}
```

and the comment a few lines down states that these standalone string keys reach every backend because "Python backends read them directly".

The sglang backend reads only one of the two values (`backend.py:366`):

```python
if request.Metadata.get("enable_thinking", "").lower() == "true":
    template_kwargs["enable_thinking"] = True
```

There is no `else`. `"false"` takes the same path as "key absent": `enable_thinking` is never passed to `apply_chat_template`, so the **chat template's own default decides**. For the Qwen3 family that default is thinking **on**, which makes thinking-off unreachable through every documented lever — the model YAML (`chat_template_kwargs:` / `reasoning.disable`, both introduced by #10359 and #8973) as well as per-request `metadata`. The only workaround left is editing the template file itself, which defeats the purpose of a per-request switch.

`backend/python/vllm/backend.py:591` carries the identical line, so this is not sglang-specific.

The generic `metadata["chat_template_kwargs"]` JSON blob built by `ResolveChatTemplateKwargs` is also not read by either Python backend — the code comment scopes it to llama.cpp, so that may well be intentional, but it means any template variable other than `enable_thinking` is unreachable there too.

**Suggested fix** — coerce both directions, the way the Go side already coerces them:

```python
_thinking = request.Metadata.get("enable_thinking", "").lower()
if _thinking in ("true", "false"):
    template_kwargs["enable_thinking"] = (_thinking == "true")
```

Happy to send a PR for sglang + vllm if the direction is agreeable. Whether the `chat_template_kwargs` blob should also be merged into `template_kwargs` in the Python backends is a separate call I'd rather leave to a maintainer.

---

#### 2. `reasoning_content` stays empty for templates that prefill the opening `<think>`

With `reasoning_parser: qwen3` configured, `reasoning_content` is always empty and the entire thinking block lands in `content`.

Cause: the Qwen3 chat template puts the **opening** `<think>` into the *prompt*. The model therefore emits only the reasoning text plus the **closing** `</think>` — the output never contains the start tag. sglang's `ReasoningParser` looks for it, doesn't find it, and returns everything as content. It is constructed without `force_reasoning` in both places (`backend.py:393` streaming, `backend.py:505` non-streaming).

Measured against sglang 0.5.17, same prompt, thinking on:

```
ReasoningParser("qwen3", stream_reasoning=False)                       -> reasoning   0 chars
ReasoningParser("qwen3", stream_reasoning=False, force_reasoning=True) -> reasoning 746 chars
                                                                          content    28 chars
```

**A blanket `force_reasoning=True` would be wrong**, and it fails in a way this project already knows well. With thinking *off*, the response contains no `</think>` at all, and forcing the prefill assumption swallows the whole answer:

```
19-char answer, no </think> in the output
  without force : reasoning   0    content  19   "2,3,5,7,11,13,17,19"
  with    force : reasoning  19    content   0   ""      <- answer gone
```

That is exactly the failure mode #10225 fixed for the Go/peg-native path (`reasoning.ExtractReasoningComplete`: honour a prefilled start token **only** when the matching closing tag is actually present). The same rule applied here would be the natural fix — in the non-streaming path (`final_reasoning_parser`, around line 502) the check is trivial, since the full text is available: set `force_reasoning` iff the closing tag occurs in `generated_text`. The streaming path is harder because the closing tag arrives late, and I don't have a good proposal for it.

Keying it off the request instead (`request.Metadata["enable_thinking"] == "true"`) is not sufficient: `reasoning_effort` also enables thinking and travels through a different key.

### To Reproduce

1. Serve a Qwen3-family model through the sglang backend, `use_tokenizer_template: true`, stock Qwen3 chat template, `reasoning_parser: qwen3`.
2. **Issue 1:** send a request with `"metadata": {"enable_thinking": "false"}` (or set `reasoning.disable` / `chat_template_kwargs: {enable_thinking: false}` in the model YAML). The model still emits a thinking block — the value never reaches `apply_chat_template`.
3. **Issue 2:** with thinking on, the response has a populated `content` containing the thinking text and an empty/absent `reasoning_content`.

### Expected behavior

1. `enable_thinking: false` reaches the chat template and turns thinking off, symmetrically with `true`.
2. Reasoning text is returned in `reasoning_content` and not in `content`, without breaking short, tag-less answers.

### Additional context

Both findings come from running this backend in production against a Qwen3-style MoE model; the numbers above are measured, not inferred. Fix #1 is a small, contained change I'm glad to contribute; #2 looks like a design call that should be made by someone with the streaming path in view, which is why it's an issue and not a PR.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `964be3bceb4c15f09505a82abdb1695692fb4660`.  There
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
{"case_id": "mudler_LocalAI__11674__964be3b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
