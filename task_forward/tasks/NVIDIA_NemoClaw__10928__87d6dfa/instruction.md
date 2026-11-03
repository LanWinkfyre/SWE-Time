# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Converge DGX Station qualification on stable identity signals

## Outcome

Make DGX Station qualification tolerate cosmetic release-label changes without accepting a new hardware generation or software build family.

NemoClaw must preserve every currently qualified Station profile. `DGX_PRETTY_NAME` must remain diagnostic evidence instead of deciding Station hardware or software lineage.

## Current problem

Station qualification uses two release classifiers and multiple firmware-product matchers. Both release classifiers have repeatedly rejected qualified hosts when NVIDIA changed or omitted a descriptive field.

Recent examples include:

- #7224: an OTA-upgraded host omitted `DGX_OTA_PRETTY_NAME`.
- #7979: an AI Developer Tools image used another qualified build date.
- #9898: stock DGX OS used another `DGX_PRETTY_NAME` value.
- #10906: the qualified Colossus image used the same display-name variant in a second profile.

The current host checks already obtain stronger Station evidence from firmware, the exact GB300 PCI identity, ARM64 Ubuntu, `DGX_PLATFORM`, release-version structure, and runtime probes.

Operation and failure class: read-only DGX Station platform qualification; false negative caused by cosmetic metadata and duplicated classifier behavior.

## Product decision

Decision: Accept

Reason and placement: Core NemoClaw. Converge the Station release contract across the shell installer and TypeScript readiness path. Stop using `DGX_PRETTY_NAME` as an authoritative identity field. Preserve all existing hardware, software-family, runtime, and action-safety gates.

Accountable maintainer: @ericksoa

Validation plan: Run one shared corpus through both production classifiers. Preserve all current positive profiles and negative near matches. Run the focused Station installer, readiness, onboarding, and documentation tests. Obtain exact-commit DGX Station evidence before approval because the host-preparation classifier is security-sensitive.

This decision is consistent with the accepted readiness direction in #7407 and the Station Express delivery scope in #8379.

## Required behavior

### Hardware identity

Keep the existing fail-closed requirements:

- Linux ARM64 on Ubuntu 24.04.
- Qualified DGX Station GB300 firmware identity.
- A display-class NVIDIA PCI device with GB300 device ID `0x31c2` or `0x31c3`.
- An effective NVIDIA GPU.

### Release classification

- Keep `/etc/dgx-release` file ownership, file type, size, schema, duplicate-field, and OTA-pair validation unchanged.
- Keep `DGX_PLATFORM="DGX Server for GALAXY-GB300"` mandatory for every DGX release profile.
- Keep the accepted OTA versions, no-OTA `7.6.x` family, and exact factory build-version and build-date boundaries unchanged.
- Keep `DGX_OTA_PRETTY_NAME="DGX OS"` authoritative when that optional lineage field is present.
- Do not require a specific `DGX_PRETTY_NAME` value after hardware, platform, version, OTA shape, and factory-build identity qualify.
- Continue parsing `DGX_PRETTY_NAME` as bounded inert metadata, but do not use it for qualification.

### Current positive corpus

Both production classifiers must continue to accept:

- Generic Ubuntu 24.04 ARM64 on qualified Station GB300 hardware.
- OTA DGX OS `7.2.0`, `7.4.0`, and `7.5.0`, with the accepted full-image and OTA-upgrade marker forms.
- No-OTA DGX OS numeric `7.6.x` with both observed display names.
- April 2026 Colossus BaseOS with both observed display names.
- May and June 2026 AI Developer Tools images.
- Both accepted GB300 PCI device IDs.

### Negative corpus

Both classifiers must continue to reject:

- Unsafe, malformed, oversized, or ambiguous release markers.
- A different `DGX_PLATFORM`.
- Partial or malformed OTA history.
- Unsupported OTA versions and future no-OTA release families.
- Factory-image version or build-date drift.
- Non-Station firmware, non-GB300 hardware, unsupported OS, and unsupported architecture.

## Implementation constraints

- Use one shared behavior corpus to assert shell and TypeScript classifier parity.
- Do not add a runtime network lookup or remote profile catalog.
- Do not propagate `--force-station-install` into general readiness.
- Do not broaden package, service, driver, Docker, CDI, or direct-GPU mutation authority.
- Do not classify arbitrary future Colossus or AI Developer Tools builds as supported.
- Keep unknown or contradictory evidence fail-closed with actionable diagnostics.

## Acceptance criteria

- [ ] Every current positive corpus entry returns the same qualified profile from both classifiers.
- [ ] Every current negative corpus entry returns the same denied result from both classifiers.
- [ ] Changing only `DGX_PRETTY_NAME` does not change the result for an otherwise qualified profile.
- [ ] Changing platform, release version, OTA structure, factory build date, marker safety, firmware identity, or PCI identity still denies qualification.
- [ ] Installer detection, host preparation, topology selection, onboarding, resume, and direct-GPU policy consume the same qualification result.
- [ ] Public Station documentation describes display names as diagnostic values rather than qualification requirements.
- [ ] Exact-commit physical Station evidence confirms one accepted profile and one denied near match before approval.

## Non-goals

- Automatic support for unqualified future Station image families.
- A durable metadata-bypass receipt.
- Changes to Station package installation or factory-runtime repair.
- Changes to the supported-platform or managed-inference matrices.

## Related work

- #7407
- #7410
- #7411
- #8379
- #8382
- #10906
- #10914
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `87d6dfae852ede67a5acb63e2beae17020a754b6`.  There
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
{"case_id": "NVIDIA_NemoClaw__10928__87d6dfa",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
