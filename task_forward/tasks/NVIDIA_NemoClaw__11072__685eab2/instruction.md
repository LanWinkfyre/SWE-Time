# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Hermes rebuild can use a local fallback after stale resolution metadata fails

## Outcome

A Hermes rebuild with stale or invalid base-image resolution metadata must not treat that metadata as local-build authority. If the release-pinned image cannot be resolved or validated, NemoClaw must stop before sandbox mutation.

## Current behavior

The rebuild path disables local fallback only when Hermes has no explicit override and no resolution hint. A stale or invalid hint can therefore fall through to the release-pinned image and then to a provenance-bound local image when the pinned image fails. Forced refresh skips hint reuse but retains the same fallback.

## Scope

- Apply this rule only to Hermes rebuild target selection.
- Preserve an explicit, provenance-bound local override or other accepted local-build authority.
- Preserve current resolver behavior for other agents and operations.
- Keep source-sandbox ownership checks unchanged.
- Do not weaken repository, digest, platform, OpenShell ABI, MCP/ACP, or security-inventory validation.

## Acceptance criteria

- [ ] A Hermes rebuild with stale or invalid resolution metadata and no explicit local-build authority disables local fallback.
- [ ] The same rule applies when forced refresh is requested.
- [ ] If the release-pinned image cannot be pulled or validated, rebuild stops before backup, deletion, or recreation.
- [ ] NemoClaw does not inspect, select, or build a local candidate on the denied path.
- [ ] An explicit, provenance-bound local override retains its current behavior.
- [ ] Other agents and operations retain their current fallback behavior.
- [ ] Focused tests cover stale metadata, invalid metadata, forced refresh, pinned-image failure, the pre-mutation stop, and explicit local authority.

## Validation

Use focused preflight and resolver tests. A new live E2E target is not required unless implementation changes a Docker or OpenShell boundary that deterministic tests cannot observe.

## Related work

- #10903 covers qualified legacy Hermes rebuilds with no resolution metadata.
- #11024 implements that missing-metadata slice.
- #10826 preserves the general resolver behavior that can accept a proven local image after a required remote pin fails. This issue defines the narrower Hermes rebuild policy.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `685eab2f5ac0fbd18c07c44a39143abceac4ca03`.  There
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
{"case_id": "NVIDIA_NemoClaw__11072__685eab2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
