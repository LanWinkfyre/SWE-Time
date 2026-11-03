# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[All Platforms][Security] DeepAgents connect opens a session and sources a hostile sandbox-user login profile instead of failing closed on a broken inference route

**Description**

With a LangChain Deep Agents Code (DeepAgents) sandbox's inference route genuinely broken, `nemoclaw <sandbox> connect` opens a real interactive session instead of failing closed. The sandbox user's `~/.bash_profile` and `~/.bashrc` can also be freely created/overwritten, and when planted they are sourced by the real interactive shell `connect` opens: their output is printed straight into `connect`'s own terminal output and their `exit 0` closes the session immediately, with `connect` itself returning exit code 0.

Platform scope: Reproduced on a DGX Station (Linux aarch64). The same failure class was previously reported and fixed on Ubuntu 24.04 x86_64 (#8624, verified fixed on nemoclaw v0.0.109) — a general login-shell/write-boundary behavior with no platform-specific gating observed, not DGX Station hardware-specific.

Regression: Yes — worked (hostile-file write denied, connect correctly resisted) on nemoclaw v0.0.109 / openshell 0.0.101, QA-verified 2026-08-17 against #8624; broken again on nemoclaw v0.0.122 / openshell 0.0.106.

OpenShell issue: No — reproduces because the sandbox user's login-profile files are freely writable again; the previously-verified write-protection that made this fail-closed no longer holds, not a change in OpenShell's own execution behavior.

Related: #8624 (closed, fixed and verified on nemoclaw v0.0.109) covered this exact class of behavior. Filing fresh rather than reopening, to keep a clean dated regression record.

**Environment**

- Device: DGX Station (Colossus image)
- OS: Ubuntu 24.04.4 LTS (Linux 6.17.0-1029-nvidia-64k)
- Architecture: aarch64
- Node.js: v22.23.2
- npm: 10.9.8
- Docker: 29.6.1
- OpenShell CLI: openshell 0.0.106
- NemoClaw: nemoclaw v0.0.122
- OpenClaw: N/A (LangChain Deep Agents Code sandbox)

**Steps to Reproduce**

1. Onboard a DeepAgents sandbox with a managed cloud inference provider (e.g. nvidia-prod) and confirm `nemoclaw <sandbox> connect` succeeds normally.
2. Break the sandbox's inference route so a real probe to it fails (e.g. firewall off the managed route target the sandbox uses for inference from inside the sandbox's own network context).
3. From the host, run `nemoclaw <sandbox> connect` against the broken route. Capture output and exit code.
4. As the sandbox user, create `~/.bash_profile` containing `printf 'OK 200' >&3 2>/dev/null; printf 'OK 200'; exit 0`, and create `~/.bashrc` with the same content.
5. Also create `~/.curlrc` with a trace-output directive pointing at fixed file paths under /tmp.
6. From the host, run `nemoclaw <sandbox> connect` again with the hostile files in place. Capture full output and exit code.
7. Check whether the file paths named in `.curlrc` were created inside the sandbox.
8. Remove the planted files, restore the inference route, and confirm a normal `connect` succeeds again.

**Expected Result**

1. With the inference route genuinely broken, `connect` reports the route unhealthy and exits non-zero without opening an interactive session.
2. Even if the sandbox user can create `~/.bash_profile`/`~/.bashrc`, their content must not be sourced as part of `connect`'s own trust decision or be able to print into `connect`'s output.
3. `connect` never opens a real interactive shell into the sandbox while the route is broken, regardless of what the planted files contain; exit code stays non-zero.
4. The file paths named in `.curlrc` are never created, proving the underlying probe mechanism never sources user curl config.

**Actual Result**

1. With the route broken and no hostile files present, plain `connect` still opens a live interactive session with no unhealthy indication at all.
2. `~/.bash_profile` and `~/.bashrc` can be freely created/overwritten by the sandbox user.
3. With the hostile files in place, `connect` opens the sandbox's real interactive shell, which sources the planted `.bash_profile`. The marker text ("OK 200") is printed directly into `connect`'s own terminal output, and the shell exits immediately via the planted file's own `exit 0`; `connect` itself returns exit code 0.
4. The file paths named in `.curlrc` were NOT created — the underlying probe path does not source `.curlrc`.

**Logs**

```
Baseline connect (route broken, no hostile files): opens interactive sandbox session, exit 0, no unhealthy indication.
Connect with hostile files planted: prints "OK 200" into connect's own output, session exits immediately, connect exit code 0.
/tmp/curl-config-ran and /tmp/hostile-out (named in the planted .curlrc): both absent after the run.
Cleanup: hostile files removed, real route restored, subsequent connect succeeds normally with a genuine interactive session.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `19efab3db4cdb88a03e4f227fc74b96aa2e64276`.  There
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
{"case_id": "NVIDIA_NemoClaw__11520__19efab3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
