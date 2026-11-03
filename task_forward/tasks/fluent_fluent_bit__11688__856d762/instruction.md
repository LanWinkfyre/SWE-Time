# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
TCP, UDP and probably more inputs should allow parsers

**Is your feature request related to a problem? Please describe.**
I tried to replace a Tail input with a setup utilizing the UDP input (#11687) and found that this input does not allow to set a parser (contrary to the documentation which suggests that all inputs may involve a parser).

**Describe the solution you'd like**
Allow parsers on all inputs, at least all which take free-form input like TCP, UDP, Blob(?), Head.

**Describe alternatives you've considered**
A Regex parser can be replaced by a Content modifier processor but that is less powerful, see #11689.

**Additional context**
As it stands now, it is not possible to simply replace an input which reads a file (Tail) with one which reads from a socket (TCP/UDP) without redesigning the whole pipeline.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `856d762ca2a6edccef2182231e0f56d66667e471`.  There
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
{"case_id": "fluent_fluent_bit__11688__856d762",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
