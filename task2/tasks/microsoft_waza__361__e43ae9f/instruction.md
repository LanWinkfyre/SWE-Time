# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Natural-language requirements → executable evals (spec-to-test)

## Problem

A SKILL.md is the contract — it tells the model when to invoke (`USE FOR`), when not to (`DO NOT USE FOR`), and what parameters mean. But there's no automated check that an `eval.yaml` actually *covers* those promises. Drift between SKILL.md claims and what's tested is invisible until users hit it.

## Proposal

Add `waza spec verify` (verification first; generation is out of scope here):

- Parses SKILL.md deterministically: `description`, `USE FOR` triggers, `DO NOT USE FOR` triggers, parameter list. Emits machine-readable requirement IDs (`req-use-001`, `req-dont-001`, etc.) with source spans.
- Loads `eval.yaml` and computes coverage: which requirement IDs are exercised by which tasks.
- Optional semantic matching (LLM-assisted) gated by a flag — deterministic parser runs first; LLM only fills gaps.
- Reports uncovered requirements. CI gate supports `--warn` (exit 0 with warnings) and `--fail` (non-zero exit).

```
$ waza spec verify
✓ req-use-001  "summarize a PR diff"          → covered by tasks: [pr-summary-basic, pr-summary-large]
✗ req-dont-002 "code review of security PRs"  → no task exercises this
```

## Why this matters for agentic-first

Agentic skills succeed or fail on *when* they engage. The router uses SKILL.md to make that decision, but evals usually only test the happy path. This issue makes negative-trigger coverage visible and gateable.

## Acceptance criteria

- [ ] `waza spec verify` command emits requirement IDs with source spans (file:line ranges).
- [ ] Deterministic parser handles `USE FOR` / `DO NOT USE FOR` / parameter blocks; tested against the existing skills corpus.
- [ ] Semantic matching is opt-in via `--semantic` flag and uses the configured judge model.
- [ ] CI modes: `--warn` (exit 0), `--fail` (exit 1 when uncovered ≥ threshold).
- [ ] Output formats: human, JSON, GitHub Actions annotations.
- [ ] Docs in `site/` with worked example and a CI snippet.

## Non-goals (filed separately)

- Generating cases to close coverage gaps — see #357.
- LLM-judged "did the agent follow the spirit of the spec" rubric — see #360.

## Related

- Roadmap: #66
- Test generation: #357
- Rubrics: #360
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e43ae9f84beaa8eaad87c26dfa922fdc981d939e`.  There
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
{"case_id": "microsoft_waza__361__e43ae9f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
