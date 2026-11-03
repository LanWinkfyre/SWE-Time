# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Add lifecycle hooks for external components around managed OpenShell onboarding

## Problem Statement

NemoClaw owns the generated OpenShell gateway configuration and the sandbox lifecycle. An external host component can need two integration points:

- Supply reviewed OpenShell settings before NemoClaw starts its managed gateway.
- Activate resources after NemoClaw verifies a new sandbox identity.

NemoClaw does not provide a supported contract for these actions. Editing the generated gateway configuration breaks NemoClaw ownership and integrity checks. Activation after onboarding can also be too late when an externally managed policy must exist during sandbox creation.

## Desired Behavior

NemoClaw provides a versioned lifecycle contract for registered external host components.

- Before gateway start, NemoClaw validates declarative component input and includes allowed settings in its generated configuration.
- NemoClaw remains the sole writer and lifecycle owner for its managed OpenShell gateway.
- After sandbox creation, NemoClaw verifies the immutable sandbox identity and effective policy before it supplies identity data to the component.
- NemoClaw waits for the component activation result before it reports onboarding success.
- A failed or ambiguous result stops onboarding and records recoverable incomplete state.
- An onboarding run without a registered component remains unchanged.

For example, an operator can register a host component, run fresh onboarding, and let NemoClaw configure its gateway before startup. NemoClaw then supplies the verified sandbox identity for component activation.

## Scope and Exclusions

Include:

- NemoClaw-managed OpenShell on Linux.
- Fresh sandbox onboarding.
- A schema-versioned and secret-free component declaration.
- Bounded pre-gateway and post-sandbox phases.
- Fail-closed validation, recovery evidence, and diagnostics.

Exclude:

- Integration-specific services, configuration, and vendor adapters.
- Direct edits to NemoClaw-generated OpenShell files.
- Generic shell hooks or execution of repository-provided commands.
- Credential transfer through arguments, environment variables, events, or logs.
- Changes to externally supervised gateway behavior.
- A new provider-attachment API in OpenShell.

## Ongoing Ownership

Proposed owner: NemoClaw maintainers own the lifecycle contract. External component maintainers own their adapters and runtime services.

## Placement and Support Expectations

Request placement in core NemoClaw because the contract controls NemoClaw-owned gateway and sandbox lifecycle boundaries. Start as an experimental interface until compatibility and recovery behavior are qualified.

## Validation Plan

- Unit tests validate the declaration schema, file ownership, file modes, unknown fields, and unsupported versions.
- Onboarding tests prove that pre-gateway input is validated before gateway effects.
- Onboarding tests prove that post-sandbox activation receives identity only after policy verification.
- Failure tests prove that invalid input and failed activation do not report onboarding success.
- Recovery tests prove that incomplete activation retains immutable identity evidence and does not remove a sandbox by mutable name.
- Installer integration tests use a generic test component.
- Regression tests prove that onboarding without a component is unchanged.
- Security review covers configuration ownership, data disclosure, command execution, and lifecycle authority.

## Compatibility Requirements

The first capability slice targets supported Linux installations that use a NemoClaw-managed OpenShell gateway and a fresh sandbox. Other platforms, external gateway supervision, resume, rebuild, and recreation remain outside the first slice.

## Security or Privacy Impact

The declaration and identity handoff must contain no credentials. Credentials remain in protected storage owned by the external component. NemoClaw does not read, persist, log, or remove them.

NemoClaw must reject symbolic links, unsafe ownership or modes, unknown fields, unsupported schema versions, and configuration that changes its lifecycle authority. Diagnostics must redact paths or values that can reveal credentials.

## Implementation Idea

Add a registered, versioned host-component contract to the onboarding state machine. Do not expose a generic command hook.

The first phase accepts only typed configuration fields that NemoClaw can render and validate. The second phase supplies the minimum verified sandbox and gateway identity fields needed for bounded activation.

## Product Scope Decision

Decision: Accept.

Recorded: September 9, 2026.

Accountable maintainer: @apurvvkumaria.

Scope: The experimental v1 external-component lifecycle contract belongs in core NemoClaw. The contract supports fresh sandbox onboarding on supported Linux installations that use a NemoClaw-managed OpenShell gateway.

Reason: NemoClaw needs an owned integration boundary before gateway startup and after verified sandbox creation. The boundary must preserve NemoClaw gateway ownership and OpenShell policy authority.

### Placement

Extend these existing owners:

- The onboarding state machine controls phase order.
- The gateway configuration writer renders the accepted OpenShell settings.
- Existing sandbox identity and policy checks establish handoff evidence.
- The finalization flow requires activation before onboarding reports success.
- The onboarding session records incomplete activation.

Do not create a parallel lifecycle manager, registry, state machine, or test harness.

### Ownership

- NemoClaw maintainers own the declaration schema, activation protocol, gateway rendering, lifecycle state, diagnostics, and compatibility contract.
- NemoClaw remains the sole writer and lifecycle owner of its managed gateway.
- OpenShell remains the source of truth for sandbox identity and effective policy.
- External component maintainers own their service process, sockets, credentials, resource activation, and component diagnostics.
- NemoClaw does not start, stop, supervise, or recover the external component.

### Compatibility and lifecycle support

- v1 supports zero or one registered component.
- v1 supports the OpenShell version pinned and validated by NemoClaw.
- v1 has no fallback for an unsupported OpenShell interceptor contract.
- v1 supports fresh sandbox onboarding only.
- Onboarding without a registered component remains unchanged.
- Resume, rebuild, recreation, migration, and externally supervised gateways remain unsupported.
- Integration-specific services, vendor adapters, and a new OpenShell provider-attachment API remain excluded.

### Registration and endpoint authority

NemoClaw discovers one optional declaration at `~/.config/nemoclaw/external-component.json`.

The v1 declaration contains only these fields:

```json
{
  "schemaVersion": 1,
  "componentId": "policy-governance",
  "interceptorSocketPath": "/run/user/1000/component/interceptor.sock",
  "activationSocketPath": "/run/user/1000/component/activation.sock"
}
```

NemoClaw must reject unknown fields, duplicate keys, unsupported versions, symbolic links, non-absolute socket paths, and ambiguous filesystem state.

The declaration must be a regular file that the current effective user owns. Its mode must be `0600`. Each endpoint must be a Unix socket that the same user owns. Socket parent directories must prevent writes from other users. NemoClaw must capture and recheck device, inode, owner, type, and mode before each use.

The current effective Linux user is the v1 trust principal. v1 does not claim isolation from a malicious process that runs as the same user. v1 does not transfer an authentication secret.

### Allowed OpenShell settings

NemoClaw may render one `openshell.gateway.interceptors` entry from the validated declaration.

NemoClaw fixes these values:

- `grpc_endpoint` uses `interceptorSocketPath` with the `unix://` scheme.
- `order = 10`.
- `failure_policy = "fail_closed"`.
- `binding_policy = "exact"`.
- `timeout = "500ms"`.
- `max_response_bytes = 1048576`.
- `max_patches = 32`.
- `openshell.v1.OpenShell/CreateSandbox` permits `modify_operation` and `validate`.
- `openshell.v1.OpenShell/UpdateConfig` permits `validate`.

v1 does not permit `post_commit`, provider profile sources, network endpoints, TLS fields, credentials, arbitrary TOML, or declaration-controlled limits and failure behavior.

### Activation protocol

After sandbox creation and policy verification, NemoClaw sends one HTTP/1.1 `POST /v1/activate` request over `activationSocketPath`. The request body is strict JSON:

```json
{
  "schemaVersion": 1,
  "activationId": "<random UUID>",
  "componentId": "policy-governance",
  "gateway": {
    "name": "nemoclaw"
  },
  "sandbox": {
    "id": "<durable OpenShell ID>",
    "identityFingerprint": "sha256:<digest>",
    "lifecycleGeneration": "<generation>"
  },
  "policy": {
    "source": "sandbox",
    "hash": "sha256:<digest>",
    "activeVersion": 1
  }
}
```

The response must use HTTP status 200 and strict JSON. It must contain only these fields:

```json
{
  "schemaVersion": 1,
  "activationId": "<matching UUID>",
  "componentId": "policy-governance",
  "sandboxId": "<matching durable OpenShell ID>",
  "policyHash": "sha256:<matching digest>",
  "result": "activated"
}
```

`result` can be `activated` or `rejected`. The response must not contain a free-form message. NemoClaw must reject unknown fields, duplicate keys, oversized bodies, extra responses, invalid values, and evidence mismatches.

### Activation proof and result

The OpenShell interceptor timeout is fixed at 500 milliseconds. The NemoClaw activation deadline is fixed at 30 seconds. v1 has no command-line, environment, or declaration override for either limit.

Before identity handoff, NemoClaw must:

- Revalidate the immutable sandbox identity against the verified create boundary.
- Read the effective policy from the recorded gateway.
- Require effective policy status.
- Require the policy to contain NemoClaw policy requirements.
- Require a valid policy hash and active version.
- Require the active version to match the sandbox observation.

After an `activated` response, NemoClaw must revalidate the same identity and policy hash before it reports success.

An explicit `rejected` response is a failed activation. A timeout, disconnect, malformed response, invalid status, or evidence mismatch is an ambiguous activation. NemoClaw must not retry activation automatically.

Failed and ambiguous activation must preserve the sandbox. The onboarding session must record bounded incomplete state with the activation ID, component ID, lifecycle generation, immutable identity fingerprint, and result class. NemoClaw must not make a deletion or recovery decision from the mutable sandbox name. NemoClaw must remove operation-local activation evidence after success. NemoClaw must not retain a policy copy or durable policy authority.

### Security and data handling

The declaration, activation request, activation response, events, logs, and artifacts must contain no credentials. Credentials remain in component-owned protected storage. NemoClaw must not read, persist, log, transfer, or remove them.

NemoClaw must not execute component commands or repository-provided commands. Diagnostics must use bounded reason classes. Diagnostics must not include request bodies, response bodies, socket paths, or component-provided text.

### Validation expectations

Focused deterministic tests must cover:

- A valid declaration.
- Every rejected declaration class.
- Validation before gateway mutation.
- Identity and effective-policy verification before handoff.
- Activation success, rejection, and ambiguous results.
- Post-response identity and policy revalidation.
- Durable incomplete state bound to immutable identity.
- No deletion or recovery decision based only on a mutable sandbox name.
- Redaction and absence of credentials.
- Unchanged onboarding when no component is registered.

Use existing fixtures and test organization. Use installer integration or live end-to-end validation only when deterministic tests cannot prove a real filesystem, process, gateway, or sandbox boundary.

## Category

Feature

## Checklist

- [x] I searched existing issues and this is not a duplicate.
- [x] I described the problem and desired behavior.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8d6643be25fb9ae80f6e2357b45b69ef4f3e0416`.  There
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
{"case_id": "NVIDIA_NemoClaw__11340__8d6643b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
