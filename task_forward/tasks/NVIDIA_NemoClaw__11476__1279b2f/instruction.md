# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Station][Install] Recognize GB300 DGX Station firmware without depending on name order

## Problem

A post-merge retest of #10914 reports that Station Express still stops before installation:

```text
This DGX Station generation is outside the validated Station GB300 express boundary.
```

The machine reports `GB300 DGX Station`. The firmware classifier requires `Station GB300` in that order. The attached operator report establishes the symptom and reported identity; it does not include the tested commit or raw firmware files.

Source inspection at `9e07bcfa2b` confirms the order dependency in `src/lib/inference/dgx-station-identity.ts` and `scripts/prepare-dgx-station-host.sh`. Existing fixtures cover `Station GB300`, OEM prefixes, and alternate firmware fields, but omit generation-first names. PR #10914 merged as `281e23efc5d8bc3c2c4a2a64f6e2dffb0ce56c01`.

## Research and proposed fix

[NVIDIA's Station development guide](https://docs.nvidia.com/dgx/dgx-station-development-guide/) identifies the current Station as a GB300 Grace Blackwell Ultra desktop system. [NVIDIA's ARM64 driver product table](https://download.nvidia.com/XFree86/Linux-aarch64/595.71.05/README/supportedchips.html) identifies GB300 devices as `31C2` and `31C3`. The table identifies GPUs, not a universal Station chassis identifier. Neither source defines a universal firmware product-name order.

Keep the existing firmware-plus-PCI contract. Recognize bounded `Station` and `GB300` identifiers in either order, with optional `DGX` between them and the existing ASCII separators. Preserve OEM prefixes and suffixes. This repairs the identity grammar without adding an OEM-name allowlist or trusting GPU names, memory size, or cosmetic release fields.

Apply the same grammar to the pre-Node shell helper and shared TypeScript classifier. Readiness, inference, direct-GPU policy, and remote topology must continue to consume the shared classifier. The Python probe collects facts; it does not need another classifier.

## Accepted scope

Decision: **Accept**, under Aaron Erickson's maintainer request to open this follow-up and implement a minimal complete fix.

- Reason: restore installation eligibility for an already-supported Station generation whose firmware reports the generation first.
- Placement: the two existing firmware classifiers and their regression tests.
- Accountable maintainer: Aaron Erickson.
- Validation: reproduce the failure before the fix; exercise both classifiers, installer routing, and TypeScript consumers; preserve denied cases. Record physical Station retest evidence separately before approval or merge.

## Acceptance criteria

- `GB300 DGX Station`, `NVIDIA DGX Station GB300`, and existing OEM Station identities classify consistently.
- Both word orders preserve ASCII case/separator behavior and token boundaries. Workstation substrings, `GB300X`, other generations, and non-ASCII separator lookalikes do not gain eligibility.
- Product, family, board, and device-tree evidence retain their existing bounds, terminators, and conflict rejection.
- Missing or wrong GB300 PCI evidence still prevents eligibility. Linux ARM64, Ubuntu 24.04, software qualification, and runtime checks remain required.
- The operator-reported name reaches Station Express preparation through the installer. An unsupported profile remains blocked.
- One narrow PR links this issue and records tests, detection-gap coverage, and remaining physical validation.

## Related work and exclusions

Follow-up to #10914 and #10928. Related architecture issue: #11133.

No new supported platforms, release profiles, dependencies, installer bypasses, or platform-identity architecture migration.

## Maintainer merge direction

Aaron Erickson directed: "please get the PR up, and once CI is green, just admin merge. This is a tiny change."

This direction followed disclosure that a physical Station retest remained outstanding. Record physical validation as outstanding and admin-merge this minimal follow-up after CI passes. Automated fixture tests do not constitute a physical Station retest. GitHub confirms `ericksoa` has repository admin permission.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1279b2f1b35790b767ff8252d9fa6e969d5f7d0f`.  There
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
{"case_id": "NVIDIA_NemoClaw__11476__1279b2f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
