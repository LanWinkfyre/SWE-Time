# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][Install] onboard --resume treats its own leftover managed vLLM container as another process holding port 8000, so an interrupted install stays unrecoverable

> [!NOTE]
> **Follow-on from #11148**, which #11271 closed. That fix works: the
> `NEMOCLAW_SERVING_PRESET conflicts with NEMOCLAW_VLLM_MODEL` message is gone
> from `v0.0.122` — 0 occurrences across a full run. This is a **different**
> failure on the same journey, found while re-verifying #11148, and it leaves
> the original user-visible outcome unchanged: an interrupted managed vLLM
> install still cannot be recovered by either documented path.

## Description

After a managed vLLM profile install is interrupted, the managed container
`nemoclaw-vllm` is left **running** and holding port 8000. `onboard --resume`
then refuses, reporting that port 8000 is "already in use by another process" —
but that process is the docker proxy for the container the very same
interrupted install created seconds earlier.

Resume does not recognise its own leftover managed state, so it neither adopts
nor replaces it, and the operator is told to "stop that process" as though a
third party owned the port.

Both documented recovery paths therefore still fail, which is the outcome
#11148's expected result asked to be fixed ("at minimum one of the two
documented recovery paths has to succeed"). `--fresh`, which discards the
interrupted install rather than recovering it, remains the only way out.

## Environment

```text
Device:        DGX Spark (NVIDIA GB10)
OS:            Ubuntu 24.04 LTS
Architecture:  aarch64
Docker:        29.2.1
OpenShell CLI: openshell 0.0.106
NemoClaw:      v0.0.122
Profile:       vllm.dgx-spark-gb10.single.nemotron-3-nano-4b-fp8
```

The vLLM image and the model were already cached on the host, so the managed
container appears about 10 seconds into the run.

## Steps to Reproduce

Preconditions asserted before each run, not assumed: port 8000 free, no
leftover `nemoclaw-vllm` container, no onboarding session, and neither
`NEMOCLAW_SERVING_PRESET` nor `NEMOCLAW_VLLM_MODEL` set in the shell or the rc
files.

1. Start the managed install:

   ```bash
   nemoclaw onboard --profile vllm.dgx-spark-gb10.single.nemotron-3-nano-4b-fp8 \
     --name recovery-match --yes
   ```

2. Once the managed vLLM container has launched but before onboarding
   completes, send a real `SIGINT` to the CLI's process group.

3. Observe the leftover container and the port:

   ```bash
   docker ps -a --filter name=nemoclaw-vllm --format '{{.Names}} | {{.Status}} | {{.Ports}}'
   ss -ltn | grep :8000
   ```

4. Re-run the identical command from step 1.

5. Run the recovery path the product itself suggests:

   ```bash
   nemoclaw onboard --resume --name recovery-match
   ```

## Expected Result

Resume validates the recorded receipt, bindings, serving identity, expected
port and container identity, then adopts or replaces the interrupted managed
state and completes. If it genuinely cannot proceed, the diagnostic identifies
the port holder as NemoClaw's own managed container and says how to clear it,
rather than describing it as another process.

## Actual Result

Step 3 — the managed container is left running and owns the port:

```text
nemoclaw-vllm | Up | 0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
LISTEN 0 4096 0.0.0.0:8000 0.0.0.0:*
```

Step 4 — the identical command is refused, exit 1:

```text
A failed DGX Station Express session is waiting. Run nemoclaw onboard --resume
to continue it, or nemoclaw onboard --fresh to discard it.
```

Step 5 — the suggested recovery path, exit 1:

```text
[non-interactive] Provider: install-vllm
vLLM install failed: port 8000 is already in use by another process.
  sudo lsof reports docker-pr (PID <pid>) listening on port 8000
Stop that process, then rerun onboarding.
[non-interactive] Aborting: vLLM install failed. See errors above.
```

The port holder is not another process: the container's port mapping
(`0.0.0.0:8000->8000/tcp`) and its creation timestamp both fall inside this
run, seconds after `==> Starting vLLM container (nemoclaw-vllm)` was printed by
the install now being resumed.

## Notes

- Run twice with different interrupt delivery — a pattern-matched `SIGINT` and a
  true process-group `SIGINT` (the latter is what #11271's own reproduction
  describes) — to rule out the signal method. Both produced the identical
  outcome.
- Behaviour differs from #11148 in one detail worth recording: that report saw
  the managed container left `Exited`; on `v0.0.122` it is left `Up`. Either
  way it is left behind and resume cannot get past it.
- `#11271` is confirmed an ancestor of `v0.0.122`, and its own fix holds — the
  variable-conflict message does not appear at all.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e8071e858ecd5b52fe25d7bc4aedaeb6cc481993`.  There
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
{"case_id": "NVIDIA_NemoClaw__11426__e8071e8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
