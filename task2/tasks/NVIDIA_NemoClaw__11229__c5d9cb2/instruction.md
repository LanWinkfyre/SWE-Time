# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Qualify and activate exact OpenShell v0.0.116 compatibility

## Decision

**Accept.** Qualify and activate OpenShell v0.0.116 as NemoClaw's only supported managed runtime. Existing managed installations on v0.0.106 and all other versions must converge to exact v0.0.116 rather than remaining in a dual-version compatibility window.

## Reason

NemoClaw already trusts the immutable OpenShell v0.0.116 release artifacts through #10790. OpenShell v0.0.112 and later contain the upstream fix for independently withholding unbound static credentials, so the v0.0.106-only inference-profile compensation can be removed when NemoClaw cuts over completely. A single exact runtime keeps the installer template, supervisor identity, credential boundary, and E2E qualification aligned and avoids claiming support for unqualified intervening releases.

## Placement

- Managed-runtime selection and installer pins under `scripts/` and the blueprint compatibility contract.
- The v0.0.116 child-visible credential manifest and its TypeScript, Python/Hermes, image, and workflow consumers.
- MCP/provider compatibility logic under `src/lib/actions/sandbox/`.
- Existing typed E2E planning and qualification surfaces; no duplicate runtime registry.
- Owning user documentation for supported OpenShell versions and upgrade behavior.

## Accountable maintainer

@prekshivyas

## Accepted behavior

- Exact OpenShell v0.0.116 is the only supported managed runtime.
- Fresh installations select exact v0.0.116.
- Existing installations on v0.0.106, v0.0.107-v0.0.115, older releases, or newer unqualified releases are rejected or reconciled to exact v0.0.116 by the owning lifecycle path.
- The v0.0.116 credential-boundary manifest is required by every credential-sensitive runtime path.
- The profileless `openai` compatibility workaround for v0.0.106 is removed; v0.0.116 relies on the upstream OpenShell fix.
- Credential-sensitive paths fail closed unless the selected runtime is exact v0.0.116 and matches its reviewed boundary.

## Validation plan

- Audit every adjacent OpenShell release from v0.0.106 through v0.0.116 and map changed contracts to NemoClaw consumers.
- Verify immutable v0.0.116 source, release, installer, sandbox, gateway, supervisor, and SDK identities.
- Add deterministic coverage for exact v0.0.116 selection, rejection or upgrade of every other version, and the v0.0.116 credential boundary.
- Qualify upgrade from v0.0.106 to v0.0.116 and fresh v0.0.116 installation.
- Run exact-v0.0.116 MCP, messaging/Slack, inference, restart/rebuild, managed-image, and credential-boundary E2E coverage.
- Keep activation in draft or otherwise gated until required exact-version CI and E2E evidence pass.

## Related work

- Refs #10790
- Refs #6256
- Refs NVIDIA/OpenShell#2862
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c5d9cb2b1873a5e2397cd67656c505304e848818`.  There
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
{"case_id": "NVIDIA_NemoClaw__11229__c5d9cb2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
