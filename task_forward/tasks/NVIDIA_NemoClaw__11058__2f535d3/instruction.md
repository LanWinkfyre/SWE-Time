# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[WSL2][Onboard] Open tier onboard does not apply messaging channel presets (slack, discord, telegram, wechat, whatsapp)

## Description

After onboarding with the Open policy tier, `nemoclaw policy-list` shows only `[brave, brew, huggingface, jira, npm, openclaw-pricing, outlook, public-reference, pypi, weather]` applied. Per official docs, the Open tier is documented to also include `slack`, `discord`, `telegram`, `wechat` (experimental), `whatsapp` (experimental), and `teams` (experimental) by default — all 5 non-experimental/experimental messaging-channel presets are missing from the applied set.

Platform scope: Reproduced on WSL2 (x86) only; other platforms not tested.
Regression: Unknown — earlier versions not tested.

## Environment

```text
Device:        WSL2 x86_64 CI runner
OS:            WSL2 (Ubuntu on Windows)
Architecture:  x86_64
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.119
```

## Steps to Reproduce

1. Run `nemoclaw onboard` and select the Open policy tier during the interactive wizard
2. Complete onboarding
3. Run `nemoclaw policy-list` (or equivalent) to see which presets are applied

## Expected Result

`policy-list` should show all Open-tier presets applied, including `slack`, `discord`, `telegram`, `wechat`, `whatsapp`, `teams`, `jira`, `outlook`, `npm`, `pypi`, `huggingface`, `brew`, `brave`, `weather`, `public-reference` — per the documented Open tier preset list.

## Actual Result

```text
policy-list must show every required Open-tier preset as applied. Missing: [slack, discord, telegram, wechat, whatsapp]. Applied set: [brave, brew, huggingface, jira, npm, openclaw-pricing, outlook, public-reference, pypi, weather].
```

## Logs

Not captured
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2f535d32e82ecf5291d09611a91cc56fbb6e6ea0`.  There
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
{"case_id": "NVIDIA_NemoClaw__11058__2f535d3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
