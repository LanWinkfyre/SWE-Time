# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
DGX Station Express rejects the qualified Colossus BaseOS display-name variant

## Investigation summary

- A DGX Station GB300 reports `DGX_PRETTY_NAME="NVIDIA DGX GB300WS"`, `DGX_SWBUILD_VERSION="7.5.0-GB300ws-GB200ws"`, and `DGX_SWBUILD_DATE="2026-04-02-08-20-16"`.
- `--force-station-install` completes Station host preparation, but topology discovery and onboarding classify the same release marker again and stop with `DGX Station hardware or software profile is not qualified.`
- Current `main` at `0673b122147433e8025222a135c7b8a3ebdbd27a` reproduces the release-classification failure.
- Both current classifiers recognize the same version and build date as `supported-colossus-baseos` only when `DGX_PRETTY_NAME="NVIDIA DGX Server"`.
- No open issue matches this exact metadata variant.

## Description

Station Express rejects an observed display-name variant of the already qualified April 2026 Colossus BaseOS profile. The installer’s temporary metadata override reaches `STATION_FACTORY_HOST_READY`, but later readiness and onboarding checks reparse `/etc/dgx-release` without an override contract and reject the profile.

The expected result is automatic recognition of this exact qualified profile variant. Unknown release metadata must remain fail-closed.

## Reproduction steps

1. Use a DGX Station GB300 on Ubuntu 24.04 with:

   ```text
   DGX_PRETTY_NAME="NVIDIA DGX GB300WS"
   DGX_SWBUILD_VERSION="7.5.0-GB300ws-GB200ws"
   DGX_SWBUILD_DATE="2026-04-02-08-20-16"
   DGX_PLATFORM="DGX Server for GALAXY-GB300"
   ```

2. Run:

   ```bash
   curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash -s -- --force-station-install
   ```

3. Continue with either the default Nemotron Ultra selection or `--station-deepseek`.
4. Observe that host preparation succeeds, but topology discovery or onboarding stops before model or sandbox creation.
5. Run the suggested `nemoclaw onboard --resume --name my-assistant` command and observe the same failure.

## Environment

- Hardware: DGX Station GB300
- OS: Ubuntu 24.04
- Reported install result: NemoClaw v0.0.109
- Current-source reproduction: NemoClaw `main` commit `0673b122147433e8025222a135c7b8a3ebdbd27a`
- GPU, driver, ECC, Docker, CDI, disk, and factory-runtime checks: reported healthy

## Debug output

```text
This DGX Station OS image is outside the recognized Station Express release-metadata boundary.
STATION_FACTORY_HOST_READY
DGX Station hardware or software profile is not qualified.
```

No model or sandbox is created.

## Proposed design

Decision: Accept

Reason and placement: Core NemoClaw. Extend the existing Colossus BaseOS release profile in `scripts/prepare-dgx-station-host.sh` and `src/lib/readiness/platform-qualification.ts`. Accept both reviewed display names for the exact `7.5.0-GB300ws-GB200ws` and `2026-04-02-08-20-16` tuple. Do not propagate `--force-station-install` into general readiness or direct-GPU policy checks.

Accountable maintainer: @ericksoa

Validation plan:

- Add focused classifier tests for both accepted display names.
- Keep build-version, build-date, platform, unsafe-marker, and near-match variants denied.
- Add readiness regression coverage for the reported tuple.
- Run the focused Station installer and readiness tests.
- Update the Station preparation documentation.
- Provide DGX Station evidence for the tested commit before approval, as repository policy requires.

This design keeps the release marker fail-closed and uses the existing `supported-colossus-baseos` owner. It does not add override state, an environment-variable bypass, or another policy authority.

## Related work

- #7124 accepted the exact April 2026 Colossus BaseOS profile and requires separate approval for metadata variants.
- #7132 added the temporary metadata-only installer override.
- #9898 established that reviewed DGX display-name variants can share one qualified release family while other fields remain constrained.
- #7979 resolved a different 7.5.0 factory-image tuple through exact profile recognition.

## Acceptance criteria

- Both current Station classifiers return `supported-colossus-baseos` for either reviewed display name when version, build date, and platform match.
- Version, build-date, platform, marker-safety, and near-match drift remain denied.
- Host readiness qualifies the reported profile only when the existing Station GB300 hardware, Ubuntu 24.04, ARM64, PCI, GPU, and runtime requirements pass.
- Stock DGX OS, NVIDIA AI Developer Tools, and generic Ubuntu behavior does not change.
- The canonical Station preparation page describes both accepted display names for this exact profile.
- Reviewable DGX Station evidence identifies the tested commit, profile, result, and supporting link before approval.

## Checklist

- [x] I confirmed this bug is reproducible
- [x] I searched existing issues and this is not a duplicate
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
{"case_id": "NVIDIA_NemoClaw__10906__87d6dfa",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
