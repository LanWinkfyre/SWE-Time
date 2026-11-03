# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Multi-turn conversation evaluation

## Problem

Waza already supports multi-turn flows via `inputs.follow_up_prompts` and the responder model. The real gap is that **per-turn assertions** aren't first class:

- Graders run once at the end of the conversation.
- There's no way to express "after turn 2, the agent should have called tool X" or "before turn 3, no PII should have been emitted."
- Failures in early turns get masked by later recovery; conversely, a correct final answer can hide a broken middle step.

So authors can compose multi-turn inputs, but can't grade *the conversation* — only its terminal state.

## Proposal

Add **per-turn checkpoints** layered on top of the existing multi-turn model. No breaking change to `inputs.prompt` or `inputs.follow_up_prompts`.

```yaml
inputs:
  prompt: "..."
  follow_up_prompts: ["..."]
checkpoints:
  - after_turn: 1
    graders:
      - type: tool_calls
        must_include: ["search_docs"]
  - after_turn: 2
    graders:
      - type: behavior
        forbidden: ["leaked credentials"]
```

- Each checkpoint runs the listed graders against the state *at that turn boundary*.
- Existing top-level `graders:` continues to run against the final state.
- `results.json` records per-turn outcomes (pass/fail per checkpoint).

## Why this matters for agentic-first

Agentic skills make decisions over time. A skill that gets the right answer the wrong way (wrong tool, wrong order, wrong intermediate state) is still buggy. Per-turn checkpoints let authors lock down *how* the agent got there.

## Acceptance criteria

- [ ] `checkpoints:` field added to task schema; backward compatible (existing tasks with only top-level `graders` keep working).
- [ ] Per-turn checkpoint results surfaced in `results.json` and dashboard.
- [ ] Reuses existing grader implementations (no new grader types required).
- [ ] Tests cover: checkpoint failure short-circuit vs. continue, mixed checkpoint + final graders, schema validation.
- [ ] Docs updated in `site/` with an example.

## Non-goals (filed separately)

- Cross-engine session/event normalization — depends on #10.
- Scripted assistant replies for deterministic dialog testing — see #367 (snapshot/replay).

## Related

- Existing: `inputs.follow_up_prompts`, responder model
- Roadmap: #66
- Engine event normalization: #10
- Snapshot/replay for deterministic dialogs: #367
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3458ced5ce3d83fd88925097de5b93516644e1a9`.  There
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
{"case_id": "microsoft_waza__358__3458ced",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
