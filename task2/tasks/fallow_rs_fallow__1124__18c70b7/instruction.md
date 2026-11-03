# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Give a Score for How Well a Project Is Defined for AI Agents

### Problem


Since many people already use this tool to review AI-generated code changes, it could be useful to also have a feature that evaluates how AI-friendly a project is.

The tool could analyze the repository and provide an **AI Agent Readiness Score** along with a few suggestions for improvement.

Some possible factors:

* README quality
* Documentation coverage
* Project structure
* Setup instructions
* Tests
* AI/agent-specific guidance files

This could help maintainers understand how easily an AI agent can navigate and contribute to their project.


### Proposed solution

Add a check that analyzes a repository and generates an AI Agent Readiness Score. The score could be based on documentation, project structure, tests, and other factors that help AI agents understand and work with the codebase. The tool could also provide suggestions for improvement.


### Alternatives considered

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `18c70b766e28138e5795dff81ad82c7432d980c9`.  There
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
{"case_id": "fallow_rs_fallow__1124__18c70b7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
