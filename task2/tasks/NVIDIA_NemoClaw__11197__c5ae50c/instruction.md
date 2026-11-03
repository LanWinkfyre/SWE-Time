# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Jetson][Onboard] onboard GPU-mode failure error message silently truncated, discarding actual docker error

## Description

When Docker fails to accept a GPU mode during `nemoclaw onboard`'s managed-bootstrap sandbox creation step, the thrown error message is silently truncated to 240 characters per attempt with no truncation indicator. For NemoClaw's standard long digest-pinned image references (`ghcr.io/nvidia/nemoclaw/{image}@sha256:{64-hex-digest}`), that reference is embedded twice in the underlying docker error text, so the two ~114-character occurrences plus fixed surrounding text already exceed the 240-character budget on their own — leaving effectively no room for the actual underlying docker failure reason (registry auth, network failure, manifest not found, etc). This is a systematic, near-total loss of diagnostic content for this code path whenever it fires with NemoClaw's normal image reference format, not an occasional edge case.

**Platform scope:** Reproduced on Jetson only in this session; other platforms not independently retested. For context only (not fully verified): the affected function is shared code used for GPU-mode-selection attempts across managed-bootstrap platforms generally, not Jetson-specific logic, so other platforms hitting a sufficiently long docker error on this code path would likely be affected too — but only the Jetson reproduction is confirmed here.

**Regression:** Unknown — earlier versions not bisected in this session. The affected function was introduced by a prior fix for a related-but-distinct issue (see Related section) and is confirmed present in the current build.

**OpenShell issue:** No — this is NemoClaw core onboard/managed-bootstrap code, not the OpenShell CLI.

## Environment

```text
Device:        Jetson Thor (arm64 CI runner)
OS:            Linux (Jetson Thor / L4T) -- exact version TBD
Architecture:  aarch64
NemoClaw:      current build (v0.0.120 release line)
OpenClaw:      N/A (onboard not completed)
```

## Steps to Reproduce

1. On a Jetson host, run a GPU-enabled onboard (do not pass `--no-gpu` / `--no-sandbox-gpu`):
   ```bash
   nemoclaw onboard --fresh --non-interactive --yes --name {sandbox} --yes-i-accept-third-party-software
   ```
2. Reach a state where the underlying docker create probe for the `--runtime nvidia` GPU mode fails to pull/find the managed sandbox image (e.g. registry auth failure, network failure, or manifest not found for the digest/architecture) during onboard's `[6/8] "Creating sandbox"` step.
3. Observe the error message onboard prints/throws.

## Expected Result

The error surfaces the actual underlying docker failure reason (or clearly indicates that content was cut, e.g. an explicit truncation marker) so the real cause — registry auth, network, manifest-not-found, etc — is diagnosable from the CLI output alone.

## Actual Result

The error message cuts off mid-digest with no truncation marker. This exact truncated text was reproduced identically at 3 independent points within the same job log, which rules out a log-capture artifact and confirms the truncation originates in NemoClaw's own error-message construction.

```text
Error: Docker did not accept the Jetson NVIDIA runtime GPU mode for managed bootstrap. Attempts: --runtime nvidia (NVIDIA_VISIBLE_DEVICES=all): Unable to find image
'ghcr.io/nvidia/nemoclaw/openclaw-sandbox@sha256:41eb2663a761897dec9cd999d938f7aae8a97698f041739c7aee7344c1a24c08'
locally ghcr.io/nvidia/nemoclaw/openclaw-sandbox@sha256:41eb2663a761897dec9cd999d938f7aae8a97698f041739c
```

## Related

`src/lib/onboard/managed-bootstrap/docker-runtime.ts`, function `formatDockerGpuModeFailureDetails` (lines 188-199) is the source of the truncation: it slices each per-attempt docker error string to `.slice(0, 240)` with no truncation indicator, then joins the results into the thrown Error at `selectedDockerMode` (line 179).

This function was introduced by a prior fix for #10086 ("intermittent GPU onboard failure discards the real Docker error, no retry on GPU-mode probe"), whose whole point was to stop the real per-mode docker error text from being discarded entirely. This is a new, different regression of that same intent: the function now surfaces some detail, but silently truncates it for any sufficiently long docker error or image reference — not a duplicate of #10086 (that issue was a total content discard with a generic message and no per-mode detail at all; this issue is a partial silent truncation of detail that is present).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c5ae50c6cf5de2c9fc7b37dcdb24938124c795d9`.  There
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
{"case_id": "NVIDIA_NemoClaw__11197__c5ae50c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
