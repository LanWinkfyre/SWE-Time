# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Mismatched tags on gallery models

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
<!-- Container Image or LocalAI tag/commit -->
Container image

**Environment, CPU architecture, OS, and Version:**
<!-- Provide the output from "uname -a", HW specs, if it's a VM  -->
N/A

**Describe the bug**
<!-- A clear and concise description of what the bug is. -->
I have noticed some inconsistent tagging on models in the default gallery, which affects filtering. Specifically "embedding" vs "embeddings", but may be happening with other tags.

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->
1. Go to "Install Models"
2. Filter by "Embedding", note that only 5 models appear
3. Remove filter, search for a well known embedding model, e.g. "nomic-embed"
4. Open its details and note that it is tagged as "embeddings"


**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->
Tagging should be consistent on the gallery or more fuzzily searched

**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

**Additional context**
<!-- Add any other context about the problem here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fbe4f0a99b9d4d3405b2c9efadb9bf06eafd2216`.  There
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
{"case_id": "mudler_LocalAI__9247__fbe4f0a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
