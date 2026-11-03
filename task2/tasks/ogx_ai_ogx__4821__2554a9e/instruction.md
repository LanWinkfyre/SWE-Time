# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
local render failed for docs

### System Info

NA

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

```[ERROR] Client bundle compiled with errors therefore further build is impossible.
Error: MDX compilation failed for file "/Users/gualiu/go/src/github.com/llamastack/llama-stack/docs/docs/providers/agents/inline_meta-reference.mdx"
Cause: Unexpected character `|` (U+007C) before name, expected a character that can start a name, such as a letter, `$`, or `_`
Details:
{
  "column": 260,
  "file": "",
  "message": "Unexpected character `|` (U+007C) before name, expected a character that can start a name, such as a letter, `$`, or `_`",
  "line": 54,
  "name": "54:260",
  "place": {
    "_bufferIndex": 259,
    "_index": 32,
    "line": 54,
    "column": 260,
    "offset": 5158
  },
  "reason": "Unexpected character `|` (U+007C) before name, expected a character that can start a name, such as a letter, `$`, or `_`",
  "ruleId": "unexpected-character",
  "source": "micromark-extension-mdx-jsx",
  "url": "https://github.com/micromark/micromark-extension-mdx-jsx#unexpected-character-at-expected-expect"
}

--------------------------

Error: MDX compilation failed for file "/Users/gualiu/go/src/github.com/llamastack/llama-stack/docs/docs/providers/tool_runtime/inline_rag-runtime.mdx"
Cause: Unexpected character `|` (U+007C) before name, expected a character that can start a name, such as a letter, `$`, or `_`
Details:
{
  "column": 260,
  "file": "",
  "message": "Unexpected character `|` (U+007C) before name, expected a character that can start a name, such as a letter, `$`, or `_`",
  "line": 45,
  "name": "45:260",
  "place": {
    "_bufferIndex": 259,
    "_index": 32,
    "line": 45,
    "column": 260,
    "offset": 5767
  },
  "reason": "Unexpected character `|` (U+007C) before name, expected a character that can start a name, such as a letter, `$`, or `_`",
  "ruleId": "unexpected-character",
  "source": "micromark-extension-mdx-jsx",
  "url": "https://github.com/micromark/micromark-extension-mdx-jsx#unexpected-character-at-expected-expect"
}
```

### Error logs

NA

### Expected behavior

local render should works
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2554a9ef1f03124ee0c4a87ed0594ec62b73769b`.  There
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
{"case_id": "ogx_ai_ogx__4821__2554a9e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
