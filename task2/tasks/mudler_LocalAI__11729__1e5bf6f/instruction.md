# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Benchmarking a la 'llama-bench': LLMs, Backends, ..

<!-- Thanks for helping us to improve LocalAI! We welcome all feature requests. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**Is your feature request related to a problem? Please describe.**
No

**Describe the solution you'd like**
Create a native LocalAI benchmarking solution that enables users to execute various performance benchmarks across various LLMs and Backends. 
A.o. this would enable users to find their most performant LLM/Backend combo, to quickly check performance after changes/updates, etc. 

**Describe alternatives you've considered**
<!-- A clear and concise description of any alternative solutions or features you've considered.  -->

**Additional context**
Consider the existing 'llama-bench' as a starting point.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1e5bf6ffb0b63575ae3539d7a9098280daf19794`.  There
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
{"case_id": "mudler_LocalAI__11729__1e5bf6f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
