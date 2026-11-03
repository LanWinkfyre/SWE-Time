# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][DGX Station][CLI&UX] config export fails for every sandbox on the default NVIDIA hosted provider with only a generic live-verification error

## Description

`nemoclaw config export` fails for every sandbox onboarded against NVIDIA's hosted inference
provider, which is the default onboarding path. The command exits 2 and prints only a generic
message, "Config export failed (live-verification-failed). Required live source state could not
be read or verified.", with no indication of which piece of state it could not verify.

The sandbox is healthy at the time: it is Ready, its gateway is running, its dashboard serves
content, and the gateway's live inference route reports exactly the provider and model recorded
in the registry.

Tested on three hosts and five sandboxes, covering both the OpenClaw and NemoHermes runtimes,
sandboxes created before the upgrade and a sandbox freshly onboarded on the release under test,
and hosts with one sandbox as well as hosts with three. Export failed identically in every case,
so the documented happy path of this command is unusable on these systems.

The command is new in this release, so there is no earlier behaviour to compare against.

Platform scope: Reproduced on DGX Spark aarch64 and DGX Station GB300 aarch64; x86_64 not
                tested for this path.
Regression: No - the command is new in this release.
OpenShell issue: No. The failing command is NemoClaw's own config export command.

## Environment

```text
Device:        NVIDIA DGX Spark and NVIDIA DGX Station GB300
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
1. On a host with no registered sandboxes, onboard one OpenClaw sandbox against the hosted
   NVIDIA provider:
     nemoclaw onboard --agent openclaw --name {sandbox} --fresh --yes --no-gpu

2. Confirm the sandbox is healthy and that the live gateway route matches what the registry
   recorded for it:
     nemoclaw {sandbox} status
     openshell inference get

3. Export the sandbox configuration to a file and record the exit code:
     nemoclaw config export {sandbox} --output {output path}

4. Export to standard output instead and record the exit code:
     nemoclaw config export {sandbox} --output -

5. Inspect how OpenShell registered the provider that the sandbox uses:
     openshell provider list
```

## Expected Result

Export exits 0 and writes one canonical YAML document describing the sandbox, or, if some
required live state genuinely cannot be verified, names which piece of state failed so the user
can act on it.

## Actual Result

Both export forms fail identically:

  Config export failed (live-verification-failed).
  Required live source state could not be read or verified.
  exit code 2

No file is created, and the stdout form writes zero bytes to standard output and 109 bytes to
standard error. The message is the same regardless of which underlying check failed, so it
gives the user nothing to act on.

The sandbox itself is healthy throughout. Its status reports Ready with a healthy inference
route, and the gateway's live route matches the registry exactly:

  registry:            provider nvidia-prod, model nvidia/nemotron-3-super-120b-a12b
  live gateway route:  provider nvidia-prod, model nvidia/nemotron-3-super-120b-a12b

The registry records preferredInferenceApi as "openai-completions" for this sandbox, while
OpenShell registers the same provider with a different type and no configuration keys:

  NAME         TYPE    CREDENTIAL_KEYS  CONFIG_KEYS
  nvidia-prod  nvidia  1                0

Every sandbox tested used this provider, and every export failed.

## Logs

```text
Export to file:

  Config export failed (live-verification-failed).
  Required live source state could not be read or verified.
  exit code 2

Export to standard output:

  stdout 0 bytes, stderr 109 bytes, exit code 2
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `680c113bdaaded08550308e8bbb5bababe589f17`.  There
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
{"case_id": "NVIDIA_NemoClaw__11154__680c113",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
