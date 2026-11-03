# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 26.04][Onboard] Hermes Portable onboarding fails on Ubuntu's default ~/.local/bin permissions

## Description

Hermes Portable onboarding fails at sandbox creation on a host that uses the standard Ubuntu login umask of `0002`. Under that umask the user's own `~/.local/bin` directory is created at mode `0775`, and the Portable executable-authority check rejects it.

The error text names no path, no mode, and no remedy, so the user is told only that a "safe executable generation" could not be captured.

No other user can write that directory. Its group is the user's private group with an empty member list, and its parent directories are owned by the same user, so the group write bit grants no real access to any other principal.

`umask 0002` is the default for ordinary users on Ubuntu, and `~/.local/bin` is the directory the NemoClaw CLI itself is installed into, so an ordinary installation lands in the rejected state without the user doing anything unusual.

This blocked a P0 release test case: only the first step of the case could run, and the remaining lifecycle coverage could not be exercised at all.

- **Platform scope:** Reproduced on Ubuntu 26.04 x86_64 only; other platforms not tested.
- **Regression:** Unknown — earlier versions not tested for this path.
- **OpenShell issue:** No

## Environment

```text
Device:        Ubuntu 26.04 host, x86_64, NVIDIA GeForce RTX 5070 Ti
OS:            Ubuntu 26.04 LTS
Architecture:  x86_64
Node.js:       v22.23.1
npm:           10.9.8
Docker:        Docker version 29.6.1, build 8900f1d
Podman:        podman version 5.7.0
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.123 (nemohermes v0.0.123)
OpenClaw:      N/A (onboard not completed)
```

## Steps to Reproduce

1. On a supported Linux host with rootless Podman, a GPU, a CDI spec, and Ollama available, confirm the login umask is the Ubuntu default:

   ```bash
   umask     # 0002
   ```

2. Confirm the state of the directory the CLI is installed into. Under that umask it is mode `0775`, owned by the current user:

   ```bash
   which nemohermes
   stat -c "%n %a %U:%G" ~/.local/bin
   ```

3. Confirm no other user can write it. The group is the user's own private group with no other members:

   ```bash
   id
   getent group $(id -gn)
   ```

4. Choose an unused non-default gateway port and start Portable Hermes onboarding:

   ```bash
   NEMOCLAW_GATEWAY_PORT=8143 NEMOCLAW_ACCEPT_THIRD_PARTY_SOFTWARE=1 \
     nemohermes onboard --experimental-profile portable --fresh --name hermes-portable-alt
   ```

## Expected Result

Onboarding accepts a user-owned directory whose group is the user's own private group and completes sandbox creation.

If a stricter permission model is genuinely required, the error names the exact path and mode it rejects and states the change that would satisfy it, and that requirement is documented on the Portable page.

## Actual Result

Onboarding reaches step `[6/8] Creating sandbox` and then exits 1 with:

```text
Error: Hermes portable OpenShell executable authority could not capture a safe executable
generation

  Onboarding did not finish. Resume from the step that failed with:
    nemohermes onboard --resume
```

The message identifies no path, no mode, and no corrective action.

**A two-arm control isolates the directory mode as the single cause.** Both arms ran the same command on the same host with a clean starting state, each on its own unused gateway port so no leftover state from the other arm could interfere.

Arm 1 — `~/.local/bin` left at the umask-produced mode `0775`:

```text
$ stat -c "%n %a" ~/.local/bin
.../.local/bin 775
$ NEMOCLAW_GATEWAY_PORT=8143 ... nemohermes onboard --experimental-profile portable --fresh
  reached [6/8], then:
  Error: Hermes portable OpenShell executable authority could not capture a safe
  executable generation
```

Arm 2 — group write bit removed, nothing else changed:

```text
$ chmod g-w ~/.local/bin
$ stat -c "%n %a" ~/.local/bin
.../.local/bin 755
$ NEMOCLAW_GATEWAY_PORT=8147 ... nemohermes onboard --experimental-profile portable --fresh
  progressed past [6/8] through [7/8] and [8/8] and onboarding COMPLETED.
  The "safe executable generation" error did not appear at all.
```

Arm 2 completing end to end, with only the group write bit changed, shows the failure is caused by the directory mode and not by GPU, Podman, registry, or model state.

The directory state that fails is what an ordinary installation produces: `umask 0002` is the Ubuntu default for regular users, and `~/.local/bin` is where the CLI itself lives.

The consequence for the affected test case: after this failure no sandbox was registered, so the status, doctor, stop, start, recover, repeated-stop, and overlapping-lifecycle coverage could not be run at all.

No documentation on the Portable or troubleshooting pages mentions this error text or asks the user to change the permissions of the directory holding the CLI.

## Logs

```text
Not captured beyond the terminal output quoted in Actual Result.
```


<!-- accepted-implementation-plan:11717 -->
## Accepted implementation plan

- Decision: Accept actionable strict-permission diagnostics. Defer permission relaxation and Ubuntu 26.04 support.
- Reason: Fail-closed executable authority is accepted scope. Treating a private group as sufficient authority needs a separate security decision and stable membership semantics.
- Placement: Preserve `src/lib/adapters/podman/executable-authority.ts` as the single authority. Carry only a filtered path, observed mode, and fixed remedy through Hermes Portable OpenShell capture, revalidation, onboarding diagnostics, and the Hermes Portable guide.
- Accountable maintainer: @rsliter. Existing assignee @cv remains assigned.
- Capability slice: Report the rejected path and mode, an owned-path permission remedy, and resume guidance without weakening any admission check.
- Acceptance evidence: Cover executable and ancestor mode `0775`, mode `0755` recovery, all capture and revalidation paths, no effects after denial, unrelated-error opacity, control-character and credential-shaped paths, and nested diagnostic redaction.
- Validation plan: Reconcile PR #11733 with current `main`; run focused authority, OpenShell, onboarding-diagnostic, and real-filesystem recovery tests; then run `npm run typecheck:cli`, `npm run docs`, and `npm run validate:pr`.
- Deferred scope: Private-group permission acceptance, Ubuntu 26.04 qualification, Podman socket policy, and full Portable lifecycle requalification.
- Stop conditions: Stop before automatic `chmod`, NSS or group-membership machinery, broader Podman policy changes, or an Ubuntu 26.04 support claim.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2b012bb4d60d1de2acec6f3e0aa24baa26ff8ac5`.  There
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
{"case_id": "NVIDIA_NemoClaw__11717__2b012bb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
