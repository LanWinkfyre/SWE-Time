# Recover the symbolic verification state this change produces

A regression report was filed against `ZSWatch/ZSWatch`.  The report is quoted verbatim below.

## Report

```
Implement "Find my watch" handler in firmware

The companion app already sends `{"t":"find","n":true/false}` via `GadgetbridgeProtocol.findDevice()` and has a "Find Watch" button, but the firmware's `parse_data()` in `ble_gadgetbridge.c` has no handler for the `"find"` message type, it falls through silently. Implementation needs a new case in the message dispatcher that triggers the vibration motor (and optionally the display) when `n:true` is received and stops when `n:false` is received.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `90df2bf3225b459950c1eea55e84888866a3b886`.  There
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
{"case_id": "ZSWatch_ZSWatch__537__90df2bf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
