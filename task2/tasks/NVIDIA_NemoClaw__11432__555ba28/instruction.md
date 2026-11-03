# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Export managed Hermes configuration with Nous API-key authentication

Parent: #10904
Planning priority: P1, next batch. Dependencies: #11286 and its implementation PR #11323.

## Problem Statement

Canonical Hermes export excludes explicit Hermes authentication state. A normally configured Hermes sandbox using a Nous API key cannot yet preserve that authentication intent through the shared export contract.

Three public selectors describe the same authentication choice. One complete export capability should cover them without adding three schema fields.

## Desired Behavior

Export one managed Hermes sandbox with hosted Nous inference, explicit API-key authentication, and otherwise canonical startup state.

| Input | First covered value | Semantic destination |
|---|---|---|
| NEMOCLAW_HERMES_AUTH_METHOD | api-key | Agent authentication method and provider reference |
| NEMOCLAW_HERMES_AUTH | api-key | Alias of the same method |
| NEMOCLAW_NOUS_AUTH_METHOD | nous-api-key | Alias of the same method |

Proposed representation: agents[].auth.method = api-key, with auth.providerRef referencing the verified inference provider. That provider carries the accepted credential reference {env: NOUS_API_KEY}. Confirm these additive field names when accepting the issue.

The existing input parser normalizes these values to api_key. Preserve existing selector precedence. Export observes retained state; it does not inspect the invoking shell to recover the original alias.

Both nemoclaw config export and nemohermes config export must produce semantically identical documents.

## Scope and Exclusions

Include one primary Hermes agent, managed immutable image, default workspace, canonical disabled dashboard, hosted Nous inference, and verified effective policy.

Exclude OAuth, device-code login, refresh, tool gateways, web search, messaging, local inference, secondary agents, new credential resolvers, and config apply. Do not infer API-key authentication from a credential-key name alone.

This issue does not depend on the sibling Hermes-interface extension. A combined configuration is a composition case after both capabilities land.

## Ongoing Ownership

Proposed maintainers: NemoClaw CLI, Hermes authentication, and onboarding maintainers.

## Placement and Support Expectations

The [epic's Accept decision](https://github.com/NVIDIA/NemoClaw/issues/10904#issuecomment-5529712248) establishes the shared architecture. This child is a proposed bounded export extension; a child-specific Accept decision is still required before implementation.

Proposed placement: core NemoClaw CLI and the shared configuration-export domain. Proposed accountable maintainer: the NemoClaw team, including the component maintainers named below. Implementation assignee: unassigned.

The accepting decision must confirm the reason, placement, accountable maintainer, bounded supported configuration, and validation plan. Publishing this issue does not assert implementation approval or completed qualification.

Reason for the proposal: preserve an existing maintained authentication choice through the shared read-only exporter, covering three public input names with one bounded method.

## Validation Plan

| Case | Required result | Shortest stable evidence |
|---|---|---|
| Allowed | Retained api_key method, correct provider/API/endpoint, and NOUS_API_KEY key metadata export canonical auth intent | Real alias parser plus profile/registry-to-verifier-to-document/action tests |
| Alias equivalence | Each selector used separately produces the same semantic document; current precedence remains unchanged | Existing Hermes auth parser tests and export fixtures |
| Denied | OAuth, wrong agent, unknown auth fields, extra gateway attachments, or method/key mismatch produces no output | Schema, verifier, and full action rejection tests |
| Ambiguous | Missing explicit auth provenance or missing/foreign provider binding does not become an inferred API-key method | Observation and verifier tests |
| Changing source | Provider identity, revision, or auth method changes between snapshots; export rejects publication | Shared observation/action tests |
| Credential boundary | Credential-value getters remain unread; synthetic secret canaries are absent from YAML, stdout, diagnostics, and artifacts | Adapter getter regressions and complete action tests |
| Failure/cleanup | Read or publication failure preserves destination and performs no runtime or credential operation | Existing action/publication fixtures extended for this source |

Run schema generation/checks, focused CLI tests, CLI type checking, and repository PR validation. Preserve canonical OpenClaw and canonical Hermes regression coverage.

The missing live dimension is an actual Nous API-key provider attachment exported from managed Hermes. Extend the existing Hermes qualification owner after confirming target ownership. Use GitHub runners and owner-provided test credentials. Export twice, validate the public schema and semantic equality, then exercise a controlled identity/binding mismatch with no publication. Retain redacted evidence. Do not create a duplicate target or weaken existing assertions to satisfy growth checks.

## Compatibility Requirements

This is an additive, read-only extension of nemoclaw.nvidia.com/v1. Existing valid documents and canonical default exports retain their meaning and serialization. No existing environment input, flag, onboarding behavior, credential resolver, or lifecycle operation changes.

Use the maintained managed images and repository-pinned OpenShell version. The first qualification is native Linux with a NemoClaw-managed gateway and Docker runtime. Other platforms and runtimes need separate evidence. This slice does not establish config apply support.

Include implementation, schema generation, behavioral tests, and owning repository guidance in one PR. User documentation follows the repository's post-merge catch-up workflow where permitted.

## Security or Privacy Impact

The operator supplies NOUS_API_KEY through existing onboarding credential custody. OpenShell retains the registered provider credential for its existing lifecycle. Export reads only allowlisted binding and credential-name metadata. It does not read, hash, validate, refresh, or remove the key value.

OAuth minted keys and broker tokens remain outside this slice. No host credential-store lookup or reconstruction of the original prompt/store/environment source is permitted.

Use two stable observations containing every new authority field. Reject unsupported, missing, foreign, stale, contradictory, or changing evidence before publication. Substitute only validated supported profile leaves, then retain the complete residual-profile comparison.

A read failure is an infrastructure failure: stop without output. Inconclusive identity or ownership is not success: stop with a redacted diagnostic. On publication failure, preserve the prior destination and remove only exporter-owned temporary output. Export never repairs, starts, stops, enrolls, adopts, or deletes a runtime resource. No new retry policy is introduced.

Preserve URL/SSRF restrictions, effective policy, immutable workload identity, strict unknown-field rejection, and private atomic file publication. Add no dependency, broad environment reader, arbitrary settings dictionary, second export engine, or custom cryptography.

## Implementation Idea

Current behavior owners:
- [Auth selector normalization](https://github.com/NVIDIA/NemoClaw/blob/main/src/lib/onboard/hermes-auth.ts).
- [Hermes provider authentication](https://github.com/NVIDIA/NemoClaw/blob/main/src/lib/hermes-provider-auth.ts).
- [Registry types](https://github.com/NVIDIA/NemoClaw/blob/main/src/lib/state/registry/types.ts).
- The Hermes-specific export projection from #11323.

Sibling paths checked: canonical Hermes hosted export, API-key registration, OAuth registration, gateway preset selection, and alias entry points. OAuth and tool-gateway cases remain rejected.

Extend the existing configuration model/schema, export evidence, verifier, document builder, and complete export action. Add a narrow adapter observation only where the capability requires new evidence. Regenerate the public JSON schema from its source.

Coordinate edits to src/lib/config/model.ts, src/lib/config/schema.ts, src/lib/domain/config/export-evidence.ts, src/lib/domain/config/verify-export-source.ts, and src/lib/domain/config/export-document.ts. Keep one owner for each behavior and reuse existing validators and fixtures. Do not hand-merge generated schema output.

Stop if #11323 cannot support this additive extension, auth provenance cannot distinguish API-key and OAuth state, or verification requires exposing a credential.

## Category

Feature

## Checklist

- [x] Searched the epic's sub-issues and related export issues; no duplicate of this bounded capability was found.
- [x] Described the problem, desired behavior, scope, and acceptance evidence.
- [ ] Record the child-specific Accept decision before implementation.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `555ba281feb4924935bda74dc35baa42129218fe`.  There
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
{"case_id": "NVIDIA_NemoClaw__11432__555ba28",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
