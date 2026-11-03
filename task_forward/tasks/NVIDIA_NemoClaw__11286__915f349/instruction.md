# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Support config export for managed Hermes sandboxes with hosted inference

Parent: #10904

## Problem Statement

`nemoclaw config export` supports one managed OpenClaw sandbox with hosted external inference. A managed Hermes sandbox cannot produce the same canonical, secret-free `NemoClawConfig`, even when it uses the same supported gateway, image, inference, and policy boundaries.

This leaves Hermes operators without the read-only configuration export that #10938 established for OpenClaw. The export architecture in #11065 provides shared observation, verification, document construction, validation, and publication boundaries, but its schema and source verifier still require OpenClaw.

Implementation depends on #11065. Do not start implementation until that PR merges and this issue records an `Accept` decision.

## Desired Behavior

Export one supported NemoClaw-managed Hermes sandbox:

```bash
nemohermes config export <sandbox> --output <path|->
```

The equivalent `nemoclaw config export` invocation must use the same command, verifier, and export pipeline. It must not introduce a Hermes-specific implementation or document format.

The command emits the aggregate `nemoclaw.nvidia.com/v1` `NemoClawConfig`. The document contains one Hermes agent and its hosted inference route. It contains credential references, never credential values.

The command must use the shared configuration type and export pipeline from #11065. It must verify Hermes-specific startup state without applying OpenClaw defaults or accepting OpenClaw provenance.

## Scope and Exclusions

### Included

- One primary Hermes agent.
- The default workspace.
- A NemoClaw-managed gateway.
- An immutable NemoClaw-managed Hermes image.
- Hosted external inference with a supported API family.
- A verified, losslessly representable effective policy.
- The existing file, standard-output, JSON-result, redaction, stability, and atomic-publication contracts.
- Specific diagnostics for missing, ambiguous, unsupported, drifted, or unstable Hermes evidence.
- The canonical hosted-inference Hermes startup state: web search disabled, no messaging, no enabled Hermes tool gateways, progressive tool disclosure, and the dashboard state produced by noninteractive managed onboarding.

### Excluded

- OpenClaw and Deep Agents Code behavior changes.
- Local or managed inference, including vLLM, Ollama, llama.cpp, and NIM.
- Secondary agents, added plugins, messaging, enabled web search, enabled Hermes tool gateways or other managed tools, non-progressive tool disclosure, mounts, direct sandbox GPU, observability, and custom images.
- Non-default Hermes dashboard or API configuration unless the accepted design proves exact representation and live evidence.
- Multi-sandbox export, apply, UID binding, adoption, pruning, rollback, and resume.

This issue expands only the successful export profile. Existing fail-closed behavior remains unchanged for excluded or unverified configurations.

## Ongoing Ownership

Proposed owner: NemoClaw CLI, Hermes, and onboarding maintainers.

The accepted decision must name one accountable implementation owner.

## Placement and Support Expectations

Requested placement: core NemoClaw CLI.

After merge, the supported export contract includes the bounded Hermes profile in this issue. Other Hermes configurations remain unsupported unless a later accepted issue adds them.

**Proposed product decision: Accept.**

Reason: Hermes is a maintained NemoClaw agent. Extending the existing read-only export pipeline to one canonical Hermes profile provides configuration portability without adding mutation behavior or a second export engine.

## Validation Plan

- Derive the static and runtime schema from the shared configuration model.
- Verify that a canonical managed Hermes fixture exports schema-valid YAML.
- Verify Hermes image, gateway, lifecycle, startup-profile, inference-route, endpoint, credential-reference, and policy agreement.
- Reject OpenClaw startup provenance for a Hermes sandbox.
- Reject non-canonical or incomplete Hermes startup state with a specific fidelity diagnostic.
- Verify that credential values never enter YAML, JSON, diagnostics, arguments, or temporary files.
- Preserve the existing stable-observation retry and zero-mutation guarantees.
- Preserve OpenClaw export behavior and its existing tests.
- Prefer extending `security-posture-hermes`, currently the nearest existing managed-Hermes and NVIDIA-hosted-inference target, after confirming that its owning paths cover configuration export. Do not add a duplicate live target.
- Verify that `nemoclaw config export` and its `nemohermes` alias use the same verifier and produce semantically identical documents.
- In live evidence, export a managed Hermes sandbox, validate its agent, image, endpoint, and explicit policy, then change recorded identity and require a drift failure with no output file.

## Compatibility Requirements

- Hermes managed images and hosted external inference supported by the maintained release.
- The OpenShell SDK and gateway version pinned by NemoClaw after #11065 merges.
- Linux file output. Standard-output behavior follows the existing supported-host contract.
- Existing OpenClaw exports remain compatible.
- The schema change must be additive within `nemoclaw.nvidia.com/v1`. If Hermes cannot be represented additively, stop for a schema-version decision.
- After #11065 merges, confirm that its merged schema and verifier still support this additive extension. If they do not, return this issue for design review before implementation.

## Security or Privacy Impact

The export remains read-only and secret-free.

Credential entries may contain an approved environment-variable name. The command must not read, test, hash, log, or serialize the credential value.

Hermes state, conversations, caches, learned data, environment values, and untracked in-sandbox changes must not enter the document. Name agreement does not establish ownership. Export requires matching registry, live sandbox, gateway, lifecycle, image, inference, and policy identity.

Missing or inconsistent evidence must stop before output publication. A failure must not mutate the sandbox, gateway, provider, policy, registry, checkpoint, session, or ownership state.

## Implementation Idea

- Extend the shared agent schema with a Hermes variant. Do not create a Hermes-only document type.
- Add Hermes-specific startup-profile reconstruction behind the existing verified export-source boundary.
- Reuse shared provider, sandbox, configuration, inference, policy, serialization, and publication adapters where their contracts suffice.
- Keep agent-specific comparison in the domain verifier. Keep the command adapter thin.
- Report unsupported Hermes fields instead of omitting them or applying OpenClaw defaults.

## Category

Feature

## Checklist

- [x] I searched existing issues and found no duplicate.
- [x] I described the problem and desired behavior.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `915f34957c6b190603562541f8a6c33dc238837c`.  There
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
{"case_id": "NVIDIA_NemoClaw__11286__915f349",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
