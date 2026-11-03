# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Onboard] Re-onboarding a Ready sandbox rejects its existing ForwardTcp dashboard listener

## Investigation Summary

- A first OpenClaw onboarding completes and starts the dashboard on the registered port `18789`.
- Re-running onboarding for the same Ready sandbox correctly selects sandbox reuse, then fails during finalization because that same port is already bound.
- The failure is deterministic in the current implementation: `ensureDashboardForward` rejects any bound persisted port before it can reconcile the already-running direct ForwardTcp service.
- The regression follows the direct ForwardTcp migration in #10695 and conflicts with the same-sandbox re-onboarding contract previously fixed by #8970.
- This currently blocks the required re-onboarding evidence for #10782.

## Description

Re-onboarding an existing Ready OpenClaw sandbox reuses the healthy OpenShell gateway and sandbox, but exits during step 7 with:

```text
Error: Registered dashboard port 18789 is already occupied; it cannot be reallocated or adopted.
```

The listener is expected to remain live from the first successful onboarding. Sandbox reuse therefore reaches a dashboard-forward launch boundary that cannot distinguish the expected existing direct ForwardTcp service from a foreign listener.

The safety rule from #10691 remains required: NemoClaw must not adopt or signal an arbitrary listener. The missing behavior is an idempotent re-onboarding path that retains or verifies the already-healthy dashboard forward without recreating the sandbox.

## Reproduction Steps

1. Onboard an OpenClaw sandbox named `tm` and let onboarding complete successfully.
2. Confirm the dashboard is registered on `http://127.0.0.1:18789/`.
3. Without stopping or recreating the sandbox, run:

   ```bash
   nemoclaw onboard --name tm --agent openclaw --yes-i-accept-third-party-software
   ```

4. Select and apply a valid inference provider configuration.
5. Observe `[reuse] Skipping sandbox (tm)` followed by the dashboard-port error during step 7.

## Environment

- NemoClaw: `v0.0.117-161-gd99d1dc579`
- OpenShell: `0.0.106`
- Docker server: `29.6.1`
- OpenClaw: `2026.7.1`
- Runtime: Docker, x86_64, CPU-only host
- Resources: 12 vCPU / 23.4 GiB RAM
- Host OS: not captured in the reproduction output

## Debug Output

A debug bundle was not collected. The exact CLI versions, successful first-onboard output, failing second-onboard transition, and source-level trigger are recorded here.

Source inspection at commit `d99d1dc579` shows this sequence in `src/lib/onboard/dashboard.ts`:

1. Read the preferred and registry-persisted dashboard port.
2. Observe that the host port is bound.
3. Throw `Registered dashboard port ... is already occupied` before launching or reconciling the forward.

The guard and its lower-level unit test were introduced by #10695. The accepted migration issue #10691 intentionally requires occupied foreign listeners to fail closed, but it also requires normal recovery to retain or relaunch dashboard forwarding.

## Logs

```shell
[6/8] Creating sandbox
──────────────────────────────────────────────────
[reuse] Skipping sandbox (tm)
✓ Active gateway set to 'nemoclaw'

[7/8] Setting up OpenClaw inside sandbox
──────────────────────────────────────────────────
✓ OpenClaw gateway launched inside sandbox
Error: Registered dashboard port 18789 is already occupied; it cannot be reallocated or adopted.

Onboarding did not finish. Resume from the step that failed with:
  nemoclaw onboard --resume
```

`onboard --resume` is not expected to make progress while the existing listener remains bound, because it reaches the same persisted-port guard.

## Expected Result

- Re-onboarding the same Ready sandbox retains its sandbox identity and registered dashboard port.
- A healthy existing dashboard forward is retained or verified through the accepted ForwardTcp lifecycle without launching a duplicate process.
- Onboarding completes deployment verification and exits 0.
- A genuinely foreign listener on the registered port still fails closed and is never adopted or signaled.
- No sandbox deletion or recreation occurs solely to reconcile a healthy dashboard forward.

## Actual Result

The sandbox is reused, but onboarding treats its expected live dashboard listener as an unadoptable port conflict and exits before policy finalization.

## Regression and Scope

- Related accepted ForwardTcp migration: #10691
- Introducing implementation: #10695
- Previously fixed same-sandbox re-onboarding contract: #8970
- Evidence workflow currently blocked: #10782

This is a bug fix to an existing supported lifecycle, not a request to adopt unknown listeners or add a new product surface.

## Acceptance Evidence

- Add regression coverage for two consecutive successful onboarding runs against the same Ready OpenClaw sandbox using a direct ForwardTcp dashboard service.
- Prove the second run retains the same sandbox identity and dashboard port, performs no duplicate forward launch, completes verification, and exits 0.
- Preserve a negative test showing that an unrelated listener on the persisted port remains fail-closed and is not signaled.
- Verify the printed resume path does not loop on the same healthy existing listener.

## Checklist

- [x] I confirmed this bug is reproducible
- [x] I searched existing issues and this is not a duplicate

## Exact-candidate E2E impact

The same occupied-listener failure blocks four jobs in [run 33915961523](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523), candidate `0ddc3ea52`:

- [Brave search](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163749169)
- [Gateway reuse](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163750568)
- [Interrupted onboarding resume](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163750643)
- [Provider token rotation](https://github.com/NVIDIA/NemoClaw/actions/runs/33915961523/job/101163750778)

These jobs fail on their second onboarding or resume pass with the expected registered dashboard port already bound. This makes #11074 a high-fanout epic blocker.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `efd56a372999acc9d97936e9b30b2164743255a5`.  There
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
{"case_id": "NVIDIA_NemoClaw__11074__efd56a3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
