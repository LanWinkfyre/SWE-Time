# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Self-quantized models get a chat template that breaks the agent path (Jinja raise_exception)

### Summary

A model quantized through LocalAI's own `/app/quantize` carries the upstream chat template that `convert_hf_to_gguf.py` embeds. For the Qwen3.x family that template raises on message orders the agent path produces, so the model chats fine but cannot be used as an agent — with nothing pointing at the cause.

### Symptom

Every agent task fails. The server log shows:

```
Error: Jinja Exception: System message must be at the beginning.
WARN [decisionWithStreaming] schema fallback after aborted forced stream failed
     tool="pick_tool" error=rpc error: code = InvalidArgument
ERROR Job execution failed error=failed to execute tools: failed to select tool:
     failed to pick tool: failed to pick tool via intention: ...
```

The same model answers ordinary chat completions correctly, including with a system message, so it looks healthy from every other angle.

### Cause

The stock Qwen3.6 template only handles `messages[0].role == 'system'` and raises otherwise. The agent path legitimately produces other orders (and more than one system/developer message).

Quants published by others do not hit this because their templates are patched. Comparing the template our conversion embedded (7764 chars) against the one in a published APEX quant of the same base model (8057 chars), the published one:

- merges up to two leading system/developer messages into one (`merged_system`), instead of looking only at `messages[0]`
- drops the `raise_exception` calls (`System message must be at the beginning.`, `No user query found in messages.`)

So the difference between "works as an agent" and "does not" is entirely in the embedded template, and self-quantizing silently lands on the wrong side.

### Workaround

Transplant a working template into the produced GGUF:

```
gguf-py/gguf/scripts/gguf_new_metadata.py --chat-template-file <working>.jinja in.gguf out.gguf
```

After that the same model passes agent tasks. (Note for anyone doing this with a non-stock quantization format: the bundled `gguf-py` aborts with `... is not a valid GGMLQuantizationType`; the writer needs to know the tensor types.)

### Suggestion

Not obvious what the right fix is, so treating this as a report rather than a proposal:

- the quantization backend could warn when the embedded template contains `raise_exception`, since that is the reliable marker; or
- `/app/quantize` could offer a chat-template override, mirroring `llama-server --chat-template-file`; or
- at minimum, document it — the failure mode is invisible until someone points an agent at the model.

### Impact

This is the one that costs the most time, because everything else about the model looks correct. Chat works, deterministic coding tasks pass unchanged, only the agent path fails, and the log line names Jinja rather than the model.

---

*Disclosure: this report was prepared with AI assistance (Claude); the runs, the template diff and the workaround were carried out on a real host (LocalAI v4.9.0-305-g8351db5de, ROCm 7.x / gfx1151).*
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e8546965c7c2e2da9dcf2d2a2c25b7ea43fad3bf`.  There
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
{"case_id": "mudler_LocalAI__11876__e854696",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
