# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Submitted version doesn't provide a reproducible paper and operator source snapshot

### System Info

Review type: Release reproducibility review
OGX: 1.0.2
OGX commit: 9424b4d9e5eca99bfc79a6e0004e28adf5f58704
Paper source inspected: current main branch
Operator repository: https://github.com/ogx-ai/ogx-k8s-operator
JOSS review: https://github.com/openjournals/joss-reviews/issues/11234

### Information

- [ ] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

The v1.0.2 tag does not contain a paper directory or paper source:

```bash
git checkout v1.0.2
git ls-tree -r --name-only HEAD | grep paper
```

### Error logs

The current main branch contains paper/ogx.tex, while the JOSS submission metadata refers to paper.md on the default branch and this makes it unclear which manuscript source corresponds to the generated proof.

### Kubernetes Operator
The paper dedicates a full section to the OGX Kubernetes Operator:

https://github.com/ogx-ai/ogx-k8s-operator

The operator is maintained in a separate repository and currently has no Git tags. Therefore, the exact operator revision evaluated by the paper is not identified by the submitted OGX v1.0.2 tag.

### Expected behavior

### Expected result

The submission has to identify an immutable and reproducible source snapshot for:

```text
The OGX v1.0.2 software
The exact paper source used to generate the proof
The Kubernetes Operator revision described in the paper
```

Please pin or tag the required repositories and clarify which manuscript and operator revisions are part of the JOSS submission.

JOSS review reference: openjournals/joss-reviews#11234
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `b1a400d7964601b99659a39e6d8390737ae5dc12`.  There
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
{"case_id": "ogx_ai_ogx__6484__b1a400d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
