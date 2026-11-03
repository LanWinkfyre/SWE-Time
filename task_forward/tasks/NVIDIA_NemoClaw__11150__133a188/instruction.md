# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[All Platforms][CLI&UX] doctor --text --json is accepted instead of rejected, printing a 507 KB payload with no mutual-exclusion error

## Description

`nemoclaw doctor` accepts `--text` and `--json` together instead of rejecting the combination.
The command exits 1 but prints no message saying the two output modes are mutually exclusive.
Instead it writes roughly half a megabyte to standard output: an oclif error object followed by
a very large dump. A normal `nemoclaw doctor --json` on the same host writes under one kilobyte.

Any caller that pipes doctor output into a JSON parser gets a half-megabyte payload and a bare
exit 1 with nothing on standard error explaining what was wrong with the invocation.

Platform scope: Reproduced on Linux aarch64 and Linux x86_64; both architectures behave the same.
Regression: Unknown - the global doctor command is new, earlier releases had no global form.
OpenShell issue: No. The failing command is NemoClaw's own doctor command.

## Environment

```text
Device:        NVIDIA DGX Spark (aarch64) and a generic x86_64 host
OS:            Ubuntu 24.04.4 LTS (aarch64); Ubuntu 24.04 under WSL2 (x86_64)
Architecture:  aarch64 and x86_64
Node.js:       v22.23.1
npm:           10.9.8
Docker:        Docker version 29.2.1 (aarch64); Docker version 29.5.3 (x86_64)
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.120
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
1. On a host with the NemoClaw CLI installed, run the global doctor with both output flags and
   record the exit code and the size of each stream:

     nemoclaw doctor --text --json
   redirecting standard output to /tmp/both.out and standard error to /tmp/both.err, then
   record the exit code and run: wc -c /tmp/both.out /tmp/both.err

2. Search both streams for any mutual-exclusion diagnostic:

     grep -icE "mutually exclusive|cannot be used together" /tmp/both.out /tmp/both.err

3. Run the single-flag form as a control and compare the output size:

     nemoclaw doctor --json
   redirecting standard output to /tmp/one.out, then run: wc -c /tmp/one.out
```

## Expected Result

The command rejects the combination before doing any work, states that the output-mode flags are
mutually exclusive, and exits non-zero with that message on standard error.

## Actual Result

The command exits 1 with no explanation and an oversized standard-output payload.

  aarch64:  EXIT=1  stdout 507489 bytes  stderr 0 bytes
  x86_64:   EXIT=1  stdout 507415 bytes  stderr 0 bytes

Matches for a mutual-exclusion diagnostic in either stream: 0.

Control on the same hosts, single flag:

  nemoclaw doctor --json  yields 788 bytes (aarch64) and 956 bytes (x86_64)

## Logs

```text
First lines of the half-megabyte standard-output payload:

  {
    "error": {
      "oclif": {
```

## Related Bugs / not duplicate of

Same command, different symptom, not a duplicate:

- **#10212** — there was no global doctor command and a bare invocation was parsed as a sandbox name. That report asked for the global form to exist; this report concerns flag validation on the global form that now exists.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `133a1886c318a45adc0a979cc1e6ebfc407bf066`.  There
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
{"case_id": "NVIDIA_NemoClaw__11150__133a188",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
