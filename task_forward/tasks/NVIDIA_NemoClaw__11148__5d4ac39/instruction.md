# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][Install] An interrupted managed vLLM install cannot be recovered: --resume fails with NEMOCLAW_SERVING_PRESET conflicts with NEMOCLAW_VLLM_MODEL

## Description

Interrupting a managed vLLM profile install leaves the installation unrecoverable. Both documented ways forward are refused, and the second one fails with an internal conflict between two settings the user never set.

Re-running the identical onboarding command is refused and points at `--resume`:

```text
A failed DGX Station Express session is waiting. Run nemoclaw onboard --resume to
continue it, or nemoclaw onboard --fresh to discard it.
```

Running the suggested `--resume` then fails during the vLLM step:

```text
vLLM install failed: NEMOCLAW_SERVING_PRESET conflicts with NEMOCLAW_VLLM_MODEL
[non-interactive] Aborting: vLLM install failed. See errors above.
```

Neither `NEMOCLAW_SERVING_PRESET` nor `NEMOCLAW_VLLM_MODEL` is set anywhere on the host — not in the login shell, not in the shell rc files, not in the gateway env file. The conflict is produced from the interrupted state itself: the profile supplies a serving preset while the persisted session carries a recorded model, and the resume path combines them.

Controlled comparison on the same host, same profile, same command:

```text
clean uninterrupted install   exit 0, sandbox Ready, managed container running
interrupted, same command     exit 1, refused, points at --resume
interrupted, --resume         exit 1, the conflict above; managed container stays Exited
```

So the failure is specific to recovering an interrupted install, not to the profile or the host.

Related: #9582 reported this same scenario — an interrupted local-profile vLLM install whose every recovery path is refused — and was closed as completed on 2026-08-20. On v0.0.119 the scenario still ends with an unrecoverable install; only the message on the `--resume` path has changed. Filing as a fresh symptom of the same user-visible problem rather than a duplicate.

Platform scope: Reproduced on DGX Spark (Linux arm64) only; other platforms not tested.
Regression: Unknown — earlier versions not tested for this exact message.
OpenShell issue: No

## Environment

```text
Device:        DGX Spark
OS:            Ubuntu 24.04
Architecture:  aarch64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        Docker version 29.2.1
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.119
OpenClaw:      N/A (onboarding never completes)
```

## Steps to Reproduce

1. On a DGX Spark with no NemoClaw sandboxes and port 8000 free, pick a compatible managed vLLM profile from `nemoclaw profiles list`, for example the single-host Nemotron-3 Nano 4B FP8 recipe.
2. Start the onboarding:

   ```bash
   nemoclaw onboard --profile <profile-id> --name recovery-match --yes
   ```

3. Once the managed vLLM container has launched but before onboarding completes, interrupt it with Ctrl-C.
4. Confirm the managed container exists:

   ```bash
   docker ps -a --filter name=nemoclaw-vllm
   ```

5. Re-run the identical command from step 2 and read its output and exit code.
6. Run the command the product suggests and read its output and exit code:

   ```bash
   nemoclaw onboard --resume --name recovery-match
   ```

7. For the control, destroy the sandbox, remove the managed container, clear the onboarding session, and run step 2 again without interrupting it.

## Expected Result

Re-running the same onboarding command validates the recorded receipt, bindings, serving identity, API-key fingerprint, expected port and container identity, then adopts or replaces the interrupted managed state and completes, leaving the sandbox Ready and serving inference. At minimum one of the two documented recovery paths has to succeed.

## Actual Result

Step 5 exits 1 without attempting recovery:

```text
A failed DGX Station Express session is waiting. Run nemoclaw onboard --resume to
continue it, or nemoclaw onboard --fresh to discard it.
```

Step 6 exits 1:

```text
[non-interactive] Provider: install-vllm
vLLM install failed: NEMOCLAW_SERVING_PRESET conflicts with NEMOCLAW_VLLM_MODEL
[non-interactive] Aborting: vLLM install failed. See errors above.
```

The managed container remains in Exited state and no sandbox is registered. The only way out is `--fresh`, which discards the interrupted installation rather than recovering it.

Step 7, the control, exits 0 on the same host with the same profile: the sandbox reaches Ready and the managed container runs. The conflict message does not appear at all in that run.

## Logs

Not captured beyond the messages quoted above; the failure is the exit status plus those lines.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5d4ac392c471de5323496a0d1df6d0118851d7d7`.  There
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
{"case_id": "NVIDIA_NemoClaw__11148__5d4ac39",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
