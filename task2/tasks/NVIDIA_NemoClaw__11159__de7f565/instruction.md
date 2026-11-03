# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][CLI&UX] bare nemoclaw doctor still resolves to a sandbox named doctor and hangs instead of running the global diagnostic

> Follow-up to #10212, which was closed as completed. The global form now exists, but the
> underlying name-resolution ambiguity it described was not resolved, and the symptom has
> changed from a fast misleading error into an unbounded hang.

## Description

When a sandbox is registered under the exact name `doctor`, the bare `nemoclaw doctor`
invocation is still resolved to that sandbox instead of to the global diagnostic. Instead of
printing a global report it opens an interactive session to the sandbox, so in any
non-interactive context the command never returns.

Adding any flag disambiguates it: `nemoclaw doctor --json` resolves to the global form and
returns immediately on the same host. That contrast is what makes the parsing behaviour visible.

The practical effect is worse than the original report. #10212 described a fast, misleading
"sandbox does not exist" error. Here the documented global command blocks forever, so any
script, CI step, or support workflow that calls it on such a host hangs instead of failing.

## Environment

```text
Device:        NVIDIA DGX Spark
OS:            Ubuntu 24.04.4 LTS
Architecture:  aarch64
Node.js:       v22.23.1
Docker:        Docker version 29.2.1
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.120
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
# 1. Register a sandbox whose exact name is "doctor"
nemoclaw onboard --agent openclaw --name doctor --fresh --yes --no-gpu

# 2. Run the bare global command with a timeout and record the exit code
timeout 120 nemoclaw doctor; echo "EXIT=$?"

# 3. Run the same command with a flag, as a control
timeout 120 nemoclaw doctor --json; echo "EXIT=$?"

# 4. Run the sandbox-scoped form, as a second control
timeout 120 nemoclaw doctor doctor; echo "EXIT=$?"
```

## Expected Result

The bare invocation runs the global diagnostic, prints the unsuffixed `NemoClaw doctor`
heading, and exits promptly. A sandbox that happens to be named `doctor` does not change how
the global command is resolved.

## Actual Result

```text
nemoclaw doctor          exit 124 after a 120s timeout; never returns
nemoclaw doctor --json   exit 0 in under 1s, 788 bytes of global JSON
nemoclaw doctor doctor   exit 0 in 3s, sandbox-scoped report, healthy
```

The bare invocation runs no diagnostic at all. Its output is an interactive sandbox session: it
prints a note that an existing SSH session to `doctor` was detected, followed by that sandbox's
policy hints, and ends with a bracketed-paste escape sequence. It then waits at the prompt.

## Suggested acceptance check

With a sandbox registered under the exact name `doctor`, bare `nemoclaw doctor` must produce the
global report with the unsuffixed heading and exit promptly, and must not open a session to the
similarly named sandbox.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `de7f565dd062b6f5affe12218ad825c97efee042`.  There
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
{"case_id": "NVIDIA_NemoClaw__11159__de7f565",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
