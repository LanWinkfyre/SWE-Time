# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Provision the Docker network before authenticated component preparation

## Problem

Fresh Linux onboarding with an authenticated external component needs the Docker bridge address before it can prepare component connections. OpenShell creates that network during Docker driver startup. This creates a startup-order dependency on a fresh host.

Draft #11595 addresses this by calling `openshell-gateway prepare-docker-network`. OpenShell 0.0.116 does not provide that command. A new upstream command is not a confirmed OpenShell roadmap commitment.

OpenShell 0.0.116 already [validates and reuses an existing bridge network](https://github.com/NVIDIA/OpenShell/blob/v0.0.116/crates/openshell-driver-docker/src/lib.rs#L3234). This permits a narrower NemoClaw-side approach, subject to compatibility and runtime validation.

## Accepted direction and ownership

Decision: **Accept the scoped NemoClaw-side network-provisioning approach**, as approved by Apurv Kumaria for this issue. This is not a release or full integration support claim.

- Placement: the existing core NemoClaw external-component onboarding path.
- Accountable maintainer for this decision: Apurv Kumaria. Implementation owner is not yet assigned.
- NemoClaw provisions a missing Docker bridge as a host prerequisite and remains the sole writer of its generated gateway configuration and the gateway lifecycle owner.
- OpenShell reuses the validated network and retains sandbox lifecycle and policy enforcement. The external component retains its policy authority.

This explicitly revises the earlier requirement that OpenShell alone create the network. It does not transfer policy handling to NemoClaw.

## Required behavior

1. Use the selected Docker connection and configured network name through the existing runtime adapter.
2. Inspect the selected network. If it is absent, create one compatible bridge through Docker with a bounded operation.
3. Validate the network identity, bridge properties, private IPv4 subnet, and usable gateway address.
4. Use the inspected address for authenticated component preparation and generated gateway configuration.
5. Revalidate the network and existing trust evidence before starting the gateway with its complete configuration.

Reuse and validate existing compatible networks without changing them. Do not start a temporary gateway or create a sandbox to initialize networking.

## Safety and failure requirements

- Confirm absence before creation. Inspection errors are not evidence of absence.
- Reject incompatible, ambiguous, replaced, or address-drifted networks. Do not repair, delete, or recreate them automatically.
- Preserve the existing requirement for one local, non-internal bridge with one usable private IPv4 subnet/gateway pair.
- Use the same Docker daemon for inspection, creation, and OpenShell startup. Do not use an unrelated default Docker context.
- Do not hard-code the gateway address, add broad listener bindings, or weaken endpoint validation.
- Preserve TLS verification, caller authentication, protected trust files, dynamic callback registration, and bounded preparation and activation.
- Preserve the component manifest's callback and failure policies. Do not introduce an unauthenticated or permissive startup path.
- Preserve the selected network if a later step fails. Report incomplete preparation without claiming success.
- Bound command time and output. Reconcile a creation race or uncertain result through inspection. Do not retry a mutation blindly.
- Do not change Docker permissions, daemon configuration, host firewall rules, or credential handling.

## Scope and related work

- Revise the network-preparation approach in #11595. Do not create a parallel onboarding implementation.
- Remove this path's dependency on the proposed OpenShell preparation command.
- Keep ordinary onboarding, version 1 component registration, and non-Docker paths unchanged.
- Keep the separate providerless agent image fix outside this issue. Related lifecycle qualification remains tracked in #11548.
- Do not change runtime version pins, declaration schemas, inference configuration, policy evaluation, or activation protocols.
- No OpenShell source changes are included. Other runtime compatibility requirements still apply.

## Validation and acceptance

- [ ] Missing network: create once, inspect the result, prepare the component, then start the gateway.
- [ ] Existing compatible network: preserve its identity and configuration. Do not issue a create or delete operation.
- [ ] Inspection failure, incompatible network, ambiguous addressing, or identity drift: stop before component preparation or gateway startup, as applicable.
- [ ] Creation failure, timeout, and competing creation: preserve state and return a bounded, accurate outcome without blind retries.
- [ ] Rejected preparation, invalid trust, or failed authentication: stop before gateway startup. Do not weaken the existing controls.
- [ ] Ordinary onboarding, version 1 registration, and non-Docker regression tests pass unchanged.
- [ ] On an isolated fresh Linux Docker environment, record the NemoClaw and OpenShell revisions. Verify networking, authenticated preparation, and gateway startup without the proposed OpenShell command.
- [ ] Cover both OpenClaw and Hermes at this boundary. Report later image or runtime blockers separately. Do not report complete onboarding if activation or workload checks were not reached.
- [ ] Update the owning guidance with network ownership, failure preservation, compatibility limits, and verified evidence.

Unit and integration tests must cover deterministic outcomes. Real Docker and OpenShell evidence is required for the network-reuse claim. OpenShell 0.0.116 is the observed missing-command baseline, not a full external-component compatibility guarantee.

## Follow-up: agree on the long-term approach with OpenShell

Work with OpenShell maintainers to agree on the supported lifecycle for preparing networking before gateway startup. Confirm network ownership, compatibility guarantees, and whether an existing mechanism or a dedicated preparation interface is appropriate.

Track that coordination here. Do not assume an upstream implementation or delivery date. If an agreed OpenShell interface becomes available, evaluate replacing NemoClaw-side provisioning in a separately reviewed change.

The immediate fix must use existing Docker/OpenShell behavior and pass the validation above. This issue does not authorize creating or commenting on issues or PRs in the OpenShell repository.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bb6800b8fbb15b962822a1ef92a460dd1eab0229`.  There
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
{"case_id": "NVIDIA_NemoClaw__11606__bb6800b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
