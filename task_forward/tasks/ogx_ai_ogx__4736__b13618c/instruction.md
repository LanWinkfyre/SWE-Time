# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Conformance mark down caused some error for documentation

### System Info

NA

### Information

- [x] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

```
✖ Client
  Compiled with some errors in 3.83s

✖ Server


<w> [webpack.cache.PackFileCacheStrategy] Skipped not serializable cache item 'Compilation/modules|/Users/gualiu/go/src/github.com/llamastack/llama-stack/docs/node_modules/@docusaurus/mdx-loader/lib/index.js??ruleSet[1].rules[8].use[0]!/Users/gualiu/go/src/github.com/llamastack/llama-stack/docs/docs/api-openai/conformance.mdx': No serializer registered for VFileMessage
<w> while serializing webpack/lib/cache/PackFileCacheStrategy.PackContentItems -> webpack/lib/NormalModule -> webpack/lib/ModuleBuildError -> Error -> VFileMessage
[ERROR] Client bundle compiled with errors therefore further build is impossible.
Error: MDX compilation failed for file "/Users/gualiu/go/src/github.com/llamastack/llama-stack/docs/docs/api-openai/conformance.mdx"
Cause: Expected a closing tag for `<details>` (183:1-183:10) before the end of `paragraph`
Details:
{
  "column": 1,
  "file": "",
  "message": "Expected a closing tag for `<details>` (183:1-183:10) before the end of `paragraph`",
  "line": 183,
  "name": "183:1-183:52",
  "place": {
    "start": {
      "_bufferIndex": 0,
      "_index": 0,
      "line": 183,
      "column": 1,
      "offset": 5178
    },
    "end": {
      "_bufferIndex": -1,
      "_index": 1,
      "line": 183,
      "column": 52,
      "offset": 5229
    }
  },
  "reason": "Expected a closing tag for `<details>` (183:1-183:10) before the end of `paragraph`",
  "ruleId": "end-tag-mismatch",
  "source": "mdast-util-mdx-jsx"
}

> docusaurus-template-openapi-docs@4.3.7 serve
> docusaurus serve

```
### Error logs

See above

### Expected behavior

no error when run https://llamastack.github.io/ locally
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b13618ca4f051d8c8bae608b71e39a5853a8763c`.  There
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
{"case_id": "ogx_ai_ogx__4736__b13618c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
