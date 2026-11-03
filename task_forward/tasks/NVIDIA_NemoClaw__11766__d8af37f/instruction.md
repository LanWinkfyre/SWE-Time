# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Restore native plugin, package, and self-update behavior

Parent: https://github.com/NVIDIA/NemoClaw/issues/11255

## Problem

NemoClaw manages plugin inventories, bundled-plugin ownership, package locations, lazy-install targets, refresh behavior, and upgrade expectations beyond what OpenShell requires. Valid native plugin or package changes can be discarded, rejected, or lost during restart and rebuild.

## Desired behavior

Within the filesystem and network access granted by OpenShell, supported agents can install, remove, update, and execute plugins and user packages through their native mechanisms. NemoClaw may ship an initial qualified image but does not control later agent-owned mutations.

## Scope

- Remove plugin allowlists, image-owned plugin reconciliation, package reset logic, and NemoClaw-specific lazy-install restrictions.
- Restore native npm, Python/uv, and agent plugin locations and discovery behavior.
- Allow native self-update and package-update commands when the selected OpenShell posture permits them.
- Preserve only credential placement required by OpenShell; do not inject credentials into plugin-visible files or environments.
- Coordinate with #11357 so retiring the bundled NemoClaw plugin does not leave a replacement plugin-governance layer.

## Acceptance criteria

- User-installed OpenClaw and Hermes plugins and packages work immediately and survive restart.
- Native install, remove, upgrade, and discovery commands are not intercepted or reset by NemoClaw.
- Rebuild/restore preserves agent-owned plugin and package state without an image allowlist.
- OpenShell egress/filesystem policy remains the only sandbox restriction.
- NemoClaw-specific plugin/package restriction code and fixtures are deleted.


## Basic-onboarder end state and E2E amendments

The onboarder may ship an initially qualified image. Once launched, plugin, package, and update behavior belongs to the native agent within OpenShell. NemoClaw must not introduce an ongoing plugin registry, allowlist, package owner, update controller, or reconciliation service.

Amend the existing E2E inventory as follows:

- `test/e2e/live/openclaw-plugin-runtime-exdev.test.ts` (`openclaw-plugin-runtime-exdev`): remove NemoClaw rebuild/recreation and image-owned plugin reconciliation; verify native OpenClaw install, invoke, update, restart, and removal inside the same OpenShell sandbox.
- `test/e2e/live/messaging-providers.test.ts`: remove bundled/image allowlist assumptions and prove native plugin discovery and use for the supported channel fixtures.
- `test/e2e/live/rebuild-openclaw.test.ts` and `test/e2e/live/rebuild-hermes.test.ts`: remove selective plugin/package restore; if migration coverage remains, verify complete agent-owned state without NemoClaw ownership metadata.
- `test/e2e/live/managed-image-activation-e2e.test.ts`: add native package/plugin installation and discovery to the applicable agent cases without exposing OpenShell-held credentials.
- `test/e2e/live/full-e2e.test.ts` (`full-e2e`): exercise one ordinary native user-package or plugin operation after onboarding.

Amend or delete the matching support contracts in `test/e2e/support/openclaw-plugin-runtime-exdev-workflow-boundary.test.ts`, `test/e2e/support/openclaw-plugin-runtime-exdev-trusted-prebuild.test.ts`, and `test/e2e/support/messaging-providers-installed-runtime-paths.test.ts`. Remove dedicated workflow wiring if native plugin coverage can be owned by an existing standard-profile target.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d8af37f0fa9ebf130d1cd4b2846fa39ef84ced94`.  There
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
{"case_id": "NVIDIA_NemoClaw__11766__d8af37f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
