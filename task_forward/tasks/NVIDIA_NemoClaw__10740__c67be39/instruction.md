# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][Onboard] every onboarding is refused when an empty ~/.config/nemoclaw/portable directory is not exactly mode 0700, and the error names no remedy

## Summary

An empty `~/.config/nemoclaw/portable` directory created by an ordinary `mkdir -p` makes every subsequent `nemoclaw onboard` fail with `Error: Unsafe portable authority directory: <path>`, exit 1. The directory holds no portable lifecycle resource, the onboarding being attempted is an ordinary (non-portable) one, and the message names only the path — it does not say the mode is the problem, does not name the required mode, and does not say the directory may be removed. The host cannot onboard again until the operator guesses `chmod 700` or deletes the directory.

The accepted mode is **exactly 0700**, so every common umask produces a directory that blocks onboarding: umask 022 yields 0755 and umask 002 yields 0775, and both are refused.

The refusal itself is reasonable fail-closed hardening. The defect is that it is unactionable, and that an empty directory owning no portable resource gates ordinary onboarding at all. There is a direct precedent on the uninstall side: the fix for #10545 made `nemoclaw uninstall` proceed when the host owns no portable lifecycle resource. Onboarding has not had the equivalent treatment.

## Environment

| | |
|---|---|
| Device | DGX Spark (NVIDIA GB10) |
| OS | Ubuntu 24.04, aarch64 |
| NemoClaw | v0.0.116 |
| OpenShell CLI | 0.0.106 |
| Provider | local Ollama (qwen3.5:9b) |
| Shell umask | 0002 |

## Steps to reproduce

Controlled experiment, three runs on one host, one variable (the directory mode):

```bash
# 1. Control — no portable directory at all
rm -rf ~/.config/nemoclaw/portable
nemoclaw onboard --fresh --non-interactive --no-gpu --name <name> --yes-i-accept-third-party-software
# exit 0

# 2. Reproduction — created exactly as an operator would create it
mkdir -p ~/.config/nemoclaw/portable      # 0775 under umask 002, 0755 under umask 022
nemoclaw onboard --fresh --non-interactive --no-gpu --name <name> --yes-i-accept-third-party-software
# exit 1 — Error: Unsafe portable authority directory: <path>

# 3. Control — same directory at mode 0700
chmod 700 ~/.config/nemoclaw/portable
nemoclaw onboard --fresh --non-interactive --no-gpu --name <name> --yes-i-accept-third-party-software
# exit 0
```

Mode sweep on the same empty directory, one onboarding attempt per mode:

| mode | onboard | refusal |
|---|---|---|
| 0755 | exit 1 | yes |
| 0750 | exit 1 | yes |
| 0711 | exit 1 | yes |
| 0700 | exit 0 | no |

This is reachable from the product's own manual test material: two cases instruct the operator to run `mkdir -p ~/.config/nemoclaw/portable/` as a step. Following either leaves the host unable to onboard.

## Expected

Either:

1. An empty portable authority directory that owns no portable lifecycle resource does not block an ordinary onboarding, mirroring the uninstall-side behaviour delivered for #10545; or
2. If the refusal must stand, the message states which property failed and how to correct it — e.g. *the directory must be owned by the current user with mode 0700; run `chmod 700 <path>`, or remove the directory if no portable install is in use.*

## Actual

```
Error: Unsafe portable authority directory: /home/<user>/.config/nemoclaw/portable
exit=1
```

Occurrences of a remediation hint in the whole onboarding output (searched for `chmod`, `0700`, "remove the directory", `delete`): **0**.

Onboarding stops before any sandbox work. The condition is sticky: every later onboarding on that host fails the same way until the directory is corrected by hand.

## Code cross-check (diagnosis only)

`src/lib/state/portable-uninstall-retirement.ts`, `readPortableAuthorityDirectory()` raises this one message for six distinct conditions — uid mismatch, not a directory, symlink, stat mismatch, `(before.mode & 0o777n) !== 0o700n`, and `nlink < 1` — so the operator cannot tell which check failed. The same function carries a `permitAnyMode` parameter that other callers use, which is why the strict-mode requirement is reached only on this path.

## Platform scope / regression

- **Platform scope:** reproduced with a controlled experiment on DGX Spark (aarch64, Ubuntu 24.04) and observed incidentally on DGX Station GB300 (aarch64). Other platforms not tested. The failing check reads a path under the user config directory and is not hardware specific, so it is expected to be broader, but that has not been directly verified.
- **Regression:** unknown — earlier releases were not tested for this path.
- **OpenShell issue:** no. The refusing check is NemoClaw's.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c67be3984f2d629ed767393ddefd32c403efb2f9`.  There
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
{"case_id": "NVIDIA_NemoClaw__10740__c67be39",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
