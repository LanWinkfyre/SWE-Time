# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
ogx landing page still displays old starter command and content

https://ogx-ai.github.io/

### 🐛 Describe the bug

<img width="527" height="360" alt="Image" src="https://github.com/user-attachments/assets/fb015469-c729-4efc-bbcd-6fbb44c9509c" />

I'm no expert on ogx at all, and I'm also new to all the renaming changes, but it feels like this landing page section might need to be updated as well to reflect the new naming

I think the obvious one is the `uvx --from 'ogx[starter]' llama stack run starter` that should be `uvx --from 'ogx[starter]' ogx run starter` instead if I'm not mistaken

Also after reading the [blog](https://ogx-ai.github.io/blog/from-llama-stack-to-ogx#why-the-rename), the messaging of "we're not a stack" sort of juxtaposes weirdly with the 'we're the full stack" that we see here...

### Expected behavior

Different content on "hero" section of landing page to reflect new naming
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `64e81241816b96bd5e2f3723a8768889dfa309f4`.  There
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
{"case_id": "ogx_ai_ogx__5650__64e8124",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
