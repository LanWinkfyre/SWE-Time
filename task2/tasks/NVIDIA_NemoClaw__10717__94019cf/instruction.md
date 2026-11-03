# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[OEM GB10][Onboard] DGX Spark FastOS is misclassified as failed N1x identity

## Description

NemoClaw 0.0.109 blocks onboarding on an OEM GB10 system whose trusted `/etc/fastos-release` contains `NAME="DGX SPARK FASTOS"`.

The system is a GB10/DGX Spark-class device, not N1x. The installer does not recognize the OEM product name as DGX Spark. Onboarding then treats the presence of `/etc/fastos-release` as N1x candidacy, rejects the DGX Spark name, and reports the host as unqualified N1x.

The same logic remains in later release tags and current `main`.

## Maintainer decision

- **Decision:** Accept
- **Reason and placement:** Accept as a core NemoClaw platform-classification bug. The existing DGX Spark installer and readiness paths own OEM GB10 systems that carry a trusted DGX Spark FastOS marker. The fix must restore that existing surface without adding vendor-specific product names or broadening N1x admission.
- **Accountable maintainer:** @ericksoa
- **Validation plan:** Add focused TypeScript platform-identity and qualification coverage plus real-installer integration coverage for an OEM GB10 product name with a trusted exact DGX Spark FastOS marker. Preserve negative coverage for N1x, malformed or ambiguous marker contents, untrusted metadata, symbolic links, unreadable evidence, wrong architecture, and unavailable GPUs.

## Reproduction

1. Use a Linux ARM64 OEM GB10 system whose product name does not contain `DGX Spark`.
2. Confirm `/etc/fastos-release` contains exactly one `NAME="DGX SPARK FASTOS"` line.
3. Install NemoClaw 0.0.109 and start onboarding.
4. Observe preflight fail with:

```text
N1x requires the trusted FastOS marker, NVIDIA PCI identity, Arm64 host, and available NVIDIA GPU.
```

## Root cause

The TypeScript platform collector checks product-name identity first. If the product name is unknown, the N1x collector sets `candidate = true` when any `/etc/fastos-release` file opens. A trusted marker whose name is `DGX SPARK FASTOS` then produces `n1xFastOsMarker = false`. Readiness treats `n1xCandidate = true` as N1x identity and blocks generic Linux admission.

The shell installer has the sibling gap: its express classifier recognizes product names that contain `DGX Spark`, but it does not use the trusted DGX Spark FastOS marker for OEM product names.

## Expected result

A trusted exact `NAME="DGX SPARK FASTOS"` marker classifies the ARM64 OEM GB10 host as DGX Spark in both installer and readiness paths. Onboarding does not emit an N1x finding.

## Acceptance criteria

- The installer identifies an OEM GB10 host as `DGX Spark` when the trusted marker contains exactly one `NAME="DGX SPARK FASTOS"` line.
- TypeScript platform identity reports `nvidiaPlatform: "spark"` for the same evidence and does not report N1x candidacy.
- DGX Spark readiness retains its existing ARM64 and available-GPU requirements.
- Exact `NAME="N1x FASTOS"` behavior remains unchanged.
- Missing markers retain generic platform handling.
- Malformed, duplicate, unknown, unreadable, linked, oversized, non-root-owned, or writable marker evidence does not gain DGX Spark admission.
- The implementation does not add a partner-specific DMI allowlist and does not require users to edit the system marker.
- Focused CLI and installer-integration tests cover the allowed and denied cases.

## Related work

- #10076 and #10099 address N1x PCI device-ID matching. They do not address this FastOS platform collision.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `94019cfaaf5fe48371b8ed96f5e1f14bd05f483a`.  There
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
{"case_id": "NVIDIA_NemoClaw__10717__94019cf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
