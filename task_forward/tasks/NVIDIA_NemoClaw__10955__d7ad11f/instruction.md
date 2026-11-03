# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[N1x Linux][Sandbox] Compaction summarization always times out due to --max-num-seqs 1 single-request vLLM concurrency limit

## Description

NemoClaw v0.0.119 on N1x Linux. The N1x vLLM recipe (PR #10625) uses `--max-num-seqs 1` to stay within N1x unified memory budget. After 3-5 turns of conversation, context compaction triggers but always times out at 120s because vLLM is already serving the active conversation response and cannot accept a second concurrent request.

User-visible symptoms:
- "agent is too busy" after 3-5 conversation turns
- "Context is too large and auto-compaction could not recover this turn. Try again, use /compact, or use /new to start a fresh session."
- Manual `/compact` also fails with the same timeout

Platform scope: Reproduced on N1x Linux only; other platforms not tested (N1x is the only platform with `--max-num-seqs 1` recipe)
Regression: No — N1x vLLM recipe is new in v0.0.118 (PR #10625), never worked with concurrent requests
OpenShell issue: No

## Environment

```text
Device:        N1x Linux Laptop (RTX Spark N1X, aarch64, 61 GiB unified RAM)
OS:            Ubuntu 24.04 (aarch64)
Architecture:  aarch64
Node.js:       TBD (machine unreachable at time of filing)
npm:           TBD
Docker:        TBD
OpenShell CLI: TBD
NemoClaw:      v0.0.119
OpenClaw:      TBD (sandbox was running, version not captured)
```

## Steps to Reproduce

1. Install NemoClaw v0.0.119 on N1x Linux via express installer:
   ```bash
   curl -fsSL https://www.nvidia.com/nemoclaw.sh | NEMOCLAW_INSTALL_TAG=v0.0.119 bash
   ```
2. Wait for vLLM container to start (downloads ~9.6 GB image, loads model).
3. Open sandbox TUI: `nemoclaw my-assistant`
4. Have 3-5 turns of normal conversation (each response takes ~60-120s at ~15 tok/s).
5. Observe "agent is too busy" / "Context is too large and auto-compaction could not recover this turn" error.
6. Try `/compact` — also fails with the same timeout.

## Expected Result

Compaction succeeds and conversation continues beyond 5 turns without interruption.

## Actual Result

Compaction always times out at 120s. Sandbox container logs show repeated failures:

```text
[compaction-diag] outcome=failed reason=timeout durationMs=120018
[compaction-safeguard] Compaction summarization failed; cancelling compaction to preserve history: Request was aborted.
[compaction-diag] outcome=failed reason=timeout durationMs=120021
[compaction-safeguard] Compaction summarization failed; cancelling compaction to preserve history: Request was aborted.
```

The TUI displays:
"Context is too large and auto-compaction could not recover this turn. Try again, use /compact, or use /new to start a fresh session."

vLLM logs show no errors — all inference requests return 200 OK. The issue is purely a concurrency constraint: `--max-num-seqs 1` means only one request can be processed at a time. A conversation response generation (~120s at ~15 tok/s for long replies) occupies the sole inference slot, so the compaction summarization request is queued and exceeds its 120s timeout.

vLLM generation throughput: ~15 tok/s (generation), ~150-250 tok/s (prompt processing)
vLLM process RSS: ~36.5 GiB (59.8% of 61 GiB unified RAM)

## Logs

Sandbox container compaction logs (from `nemoclaw my-assistant logs`):

```text
09:44:07 [compaction-diag] outcome=failed reason=timeout durationMs=120018
09:44:07 [compaction-safeguard] Compaction summarization failed; cancelling compaction to preserve history: Request was aborted.
09:47:37 [compaction-diag] outcome=failed reason=timeout durationMs=120021
09:47:37 [compaction-safeguard] Compaction summarization failed; cancelling compaction to preserve history: Request was aborted.
```

vLLM container logs (concurrent with the compaction attempts):

```text
09:42:02 INFO: "POST /v1/chat/completions HTTP/1.1" 200 OK
09:44:12 INFO: Avg generation throughput: 15.2 toks/s, ...
09:44:12 INFO: "POST /v1/chat/completions HTTP/1.1" 200 OK
```

Note: The first request ran from 09:42:02 to 09:44:12 (~130s), during which the compaction request at 09:44:07 was either queued or immediately timed out. No vLLM errors — all requests eventually complete with 200 OK when they get the inference slot.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d7ad11fc64e0066057b958cbc5206b34727ea980`.  There
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
{"case_id": "NVIDIA_NemoClaw__10955__d7ad11f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
