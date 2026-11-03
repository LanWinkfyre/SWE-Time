# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Qualify and adopt the OpenShell release that preserves provider identity during updates

## Outcome

NemoClaw installs and qualifies a stable OpenShell release that preserves stored provider identity during credential-only updates.

This task tracks a semantic dependency migration. It does not add a provider or a new supported integration.

## Current state

- NemoClaw currently pins OpenShell 0.0.101 across the installer, blueprint, managed images, and credential-boundary manifests.
- OpenShell issue NVIDIA/OpenShell#2991 tracks credential updates that omit the stored provider type.
- NVIDIA/OpenShell#3014 and NVIDIA/OpenShell#3109 contain merged fixes.
- NemoClaw #8893 records the previous OpenShell release-qualification pattern.
- NemoClaw #6691 owns candidate-version compatibility evidence.
- NemoClaw #9806 owns typed provider and credential operations.
- NemoClaw #10942 requires one compatible OpenShell component set across install and recovery.

A development build can provide early evidence. NemoClaw must not change its stable pin until an immutable OpenShell release contains the required behavior.

## Required behavior

- Select the first immutable OpenShell release that contains the provider-identity fix.
- Audit every compatibility and security contract from OpenShell 0.0.101 through the selected release.
- Update all NemoClaw OpenShell pins, checksums, images, manifests, and provenance records as one reviewed migration.
- Preserve provider type and provider-profile identity during credential-only updates.
- Keep create, get, list, update, attach, detach, import, export, and delete behavior compatible with current NemoClaw consumers.
- Reject an update before mutation when stored provider identity cannot be verified.
- Keep provider credentials out of process arguments, logs, errors, test artifacts, and sandbox-visible state.
- Preserve enough state for recovery when an update or replacement fails.

## Acceptance criteria

- [ ] A candidate run from #6691 exercises the selected OpenShell revision against the exact NemoClaw commit under review.
- [ ] The candidate run records the requested revision, resolved artifact identity, digest, and observed runtime version.
- [ ] A credential-only provider update preserves the stored provider type and profile identity.
- [ ] An authorized credential update succeeds without replacing the provider or detaching its sandbox.
- [ ] A missing, ambiguous, or mismatched provider identity fails before mutation.
- [ ] Interrupted and rejected updates leave the previous provider and sandbox attachment usable.
- [ ] Provider credentials are absent from command arguments, logs, errors, snapshots, and retained test artifacts.
- [ ] Installer, onboarding, provider, restart, rebuild, and cleanup tests pass with one compatible OpenShell component set.
- [ ] Live end-to-end evidence covers provider creation, credential rotation, authenticated use, gateway restart, sandbox rebuild, and deletion.
- [ ] Stable NemoClaw pins change only after the selected OpenShell release and immutable artifacts are published.

## Delivery order

1. Qualify a development or candidate OpenShell build through #6691.
2. Record the semantic migration and any required NemoClaw changes.
3. Wait for the immutable OpenShell release.
4. Update the stable pins and run the required deterministic and live tests.

## Non-goals

- Add a new provider type or provider profile.
- Accept a development build as a production dependency.
- Bypass OpenShell authorization or provider-identity checks.
- Store provider credentials in NemoClaw state.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `38b5e3cabdff3efe71663a2bbeeffb39e89bd942`.  There
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
{"case_id": "NVIDIA_NemoClaw__10943__38b5e3c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
