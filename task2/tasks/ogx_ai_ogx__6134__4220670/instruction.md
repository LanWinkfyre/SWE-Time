# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
feat(skills): inject skill instructions into Responses API system prompt

## Summary

When skills are attached to a Responses API call, their SKILL.md instructions should be injected into the model's system prompt. This is the foundational integration layer — every skill needs its instructions surfaced to the model regardless of execution model.

This is Tier 1 of the Skills–Responses integration (see #5891 for the Skills CRUD API, now complete).

## Motivation

The Skills API (#5891) provides CRUD for versioned skill bundles, but skills are inert without integration into the inference path. The most immediate value is making the model aware of skill instructions so it can follow them when using existing tools (`code_interpreter`, `file_search`, function calls).

Example: a "code-review" skill with SKILL.md instructions like "Always check for SQL injection, XSS, and auth bypass" would guide the model's behavior during a Responses API call without requiring any new tool type or container.

## Proposed Design

Add a `skills` parameter to the Responses API create endpoint:

```python
response = client.responses.create(
    model="gpt-4o",
    input="Review this code for security issues",
    skills=["skill-abc123"],  # skill IDs
)
```

When `skills` is provided:

1. The Responses provider resolves each skill ID via the Skills API
2. For each skill, reads the SKILL.md manifest (name, description, instructions)
3. Prepends the skill instructions to the system prompt, formatted as:

```
## Skill: {name}
{description}

### Instructions
{instructions}
```

4. The model generates its response with the skill context available

## Tasks

- [ ] 1. Add `skills` parameter (list of skill IDs) to the Responses API create request model
- [ ] 2. Add `Api.skills` as an optional dependency for the Responses provider
- [ ] 3. In the builtin Responses provider, resolve skill IDs and read SKILL.md instructions
- [ ] 4. Inject skill instructions into the system prompt before the inference call
- [ ] 5. Add unit tests for skill instruction injection
- [ ] 6. Add integration test: create skill → create response with skill → verify instructions influence output
- [ ] 7. Update OpenAPI spec and provider docs

## Dependencies

- Skills CRUD API (#5891) — **merged**

## Non-goals (handled by separate issues)

- Skill tool type for structured invocation (see companion issue)
- Container execution for skill code (see #5892)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `422067080ba05a603e718d5a39c2417b77d4b037`.  There
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
{"case_id": "ogx_ai_ogx__6134__4220670",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
