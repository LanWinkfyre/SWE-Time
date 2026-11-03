# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[CLI&UX] rebuild's own printed recovery guidance breaks itself: destroy (step 3) makes --retire-recovery (step 5) fail

**Description**

When `nemoclaw <sandbox> rebuild` bails with a retained credential-bearing policy handoff, its own printed recovery guidance is self-contradicting: step 3 tells the user to run `nemoclaw <sandbox> destroy --yes`, then step 5 tells them to run `nemoclaw <sandbox> rebuild --retire-recovery <id> --yes`. Following steps 3 then 5 in the printed order fails, because `destroy` fully removes the sandbox's registry entry, and `--retire-recovery` cannot resolve the sandbox name afterward. Skipping step 3 and running `--retire-recovery` directly (while the sandbox is still registered in its "interrupted at sandbox" state) works correctly and exits 0.

Platform scope: Reproduced on Ubuntu 24.04 x86_64 only; other platforms not tested this pass.
Regression: Unknown - earlier versions not tested this pass.
OpenShell issue: No


**Environment**

Device:        Ubuntu 24.04 x86_64 server
OS:            Ubuntu 24.04
Architecture:  x86_64
Docker:        29.5.2
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.121


**Steps to Reproduce**

1. Get a sandbox into the "retained credential-bearing policy handoff" state (rebuild bails with a message including a `--retire-recovery <transactionid>` suggestion and a numbered recovery list whose step 3 is `nemoclaw <sandbox> destroy --yes` and step 5 is `nemoclaw <sandbox> rebuild --retire-recovery <transactionid> --yes`).
2. Follow the guidance in the printed order: run step 3, `nemoclaw <sandbox> destroy --yes` (exits 0, "Sandbox destroyed").
3. Then run step 5 exactly as printed: `nemoclaw <sandbox> rebuild --retire-recovery <transactionid> --yes`.
4. For comparison: on a fresh reproduction of the same retained-handoff state, skip step 3 entirely and run step 5 directly instead.


**Expected Result**

Following the tool's own printed recovery steps in the order it prints them should succeed at every step. `--retire-recovery` should be able to retire the named transaction regardless of whether `destroy` was already run, since the transaction ID and backup path are independent identifiers already known to the tool (printed in its own message) and do not require the target name to still resolve as a live sandbox.


**Actual Result**

After step 3 (`destroy --yes`, exit 0), step 5 fails:
  Sandbox 'gw1-sb' does not exist.
  Run 'nemoclaw onboard' to create one.
  (exit 1)

Without running destroy first, the identical `--retire-recovery` command against the identical transaction ID succeeds:
  Retired rebuild recovery '78624bbf-e419-4b52-a00b-6e42376970bc' for sandbox 'gw1-sb' from /home/<user>/.nemoclaw/rebuild-backups/gw1-sb/<timestamp>.
  (exit 0)

Confirmed the successful retire is otherwise correct: the credential-bearing `rebuild-policy-handoff.*.yaml` file and the manifest's `rebuildPolicyHandoff` field were both removed, while the rest of the backup directory (agents, extensions, workspace, etc.) was left intact -- selective retirement of only the matching transaction works as designed. The defect is specifically that the tool's own recovery guidance's step ordering (destroy before retire-recovery) leads the operator into a dead end.


**Logs**

Not captured beyond the exact command output pasted above.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `48cefc6f53bc158fae59ee319718fc00345f660a`.  There
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
{"case_id": "NVIDIA_NemoClaw__11394__48cefc6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
