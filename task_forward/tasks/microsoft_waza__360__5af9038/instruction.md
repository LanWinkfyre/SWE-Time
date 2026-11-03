# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: First-class LLM-as-judge grader with reusable rubrics

## Problem

Waza already has a `prompt` grader (LLM-as-judge) in `internal/graders/prompt_grader.go`. What's missing is a **rubric library** so authors don't hand-write the same rubric prompts across every skill:

- Every author re-invents "helpfulness," "groundedness," "instruction-following," "refusal-correctness" from scratch.
- Rubrics in the wild are inconsistent in scale (1–5 vs. pass/fail vs. 0–1), wording, and bias.
- No way to reference a rubric by name (`rubric: groundedness`) the way you reference a grader type.

## Proposal

Ship a **rubric preset library** that the existing `prompt` grader can resolve by name:

```yaml
graders:
  - type: prompt
    rubric: groundedness   # resolves to a versioned rubric file
  - type: prompt
    rubric: ./rubrics/my-custom.md   # local file
```

- Rubrics live as plain markdown/YAML files with a defined frontmatter shape (scale, scoring guide, examples).
- Ship a starter set: `groundedness`, `helpfulness`, `instruction-following`, `refusal-correctness`, `tool-use-appropriateness`.
- Rubrics are versioned (semver in frontmatter).
- Each rubric has golden examples bundled so the rubric *itself* can be unit-tested.

## Why this matters for agentic-first

Agentic skills need to be judged on *behavior* (did it refuse correctly? did it ground its answer in the right source?), not just output text. A shared rubric vocabulary makes evals comparable across skills and across teams.

## Acceptance criteria

- [ ] Rubric file schema defined and validated (frontmatter + body).
- [ ] `prompt` grader resolves `rubric:` by name (built-in) or path (local).
- [ ] Starter set of 5 rubrics shipped under `internal/graders/data/rubrics/` with golden examples.
- [ ] Each shipped rubric has a test that runs it against goldens and asserts expected scores.
- [ ] No breaking change to existing `prompt` grader usage (inline `criteria` still works).
- [ ] Docs in `site/` listing rubrics with usage examples.

## Non-goals (filed separately)

- Judge calibration / inter-judge variance reporting — separate concern, file as follow-up if needed.
- Multi-judge aggregation — defer until there's a concrete user workflow.
- Safety/adversarial rubrics — see #365.

## Related

- Existing: `internal/graders/prompt_grader.go`
- Roadmap: #66
- Safety rubrics: #365
- Registry-addressable rubrics: #17
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5af9038ba478c9bca700a4f71a847db85a85a7b9`.  There
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
{"case_id": "microsoft_waza__360__5af9038",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
