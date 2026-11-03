# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 26.04][Sandbox] destroy cannot reconcile a retained-recovery record when post-create failure happens before pending-create identity is published

## Description

When a sandbox creation fails before its pending-create identity is published, NemoClaw
writes a retained-recovery record but leaves the sandbox registry row without the identity
and lifecycle-generation fields that destroy needs to bind the two together. destroy then
cannot select a matching recovery record, refuses, and prints a message that tells the
user to resolve an identity conflict without naming any way to do so. The record can never
be reconciled through a supported command.

This is NOT a request to let --force bypass the immutable identity fence. That fence is
intentional and should stay. The ask is that a record the product itself wrote in a
half-initialized state be reconcilable through some supported path, or that the refusal
name a concrete remedy.

This is also distinct from the known case where the registry row DOES carry those fields.
In that case destroy prints a different message that names a remedy - make the owning
gateway report the sandbox absent, then rerun destroy - and following it works. That path
was verified working on a separate host during the same test session. The case reported
here is the one where that remedy does not help.

Platform scope: Reproduced on Ubuntu 25.04 x86_64 only; other platforms not tested.
Regression: Unknown - earlier versions not tested for this path.
OpenShell issue: No

## Environment

```text
Device:        Ubuntu 25.04 virtual machine, NVIDIA A100
OS:            Ubuntu 25.04
Architecture:  x86_64
Node.js:       v22.16.0
npm:           10.9.2
Docker:        Docker version 29.5.2, build 79eb04c
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.121
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```bash
1. Write a Dockerfile that builds successfully on top of a NemoClaw sandbox image and
   declares the tool-disclosure build contract:

     WORKDIR="$(mktemp -d)"
     printf '%s\n' \
       'FROM ghcr.io/nvidia/nemoclaw/sandbox-base:v0.0.121' \
       'ARG NEMOCLAW_TOOL_DISCLOSURE=progressive' \
       'ENV NEMOCLAW_TOOL_DISCLOSURE=$NEMOCLAW_TOOL_DISCLOSURE' \
       'RUN echo "BASELINE_BUILD_OK"' > "${WORKDIR}/Dockerfile"

2. Onboard from that Dockerfile on a host where sandbox creation fails after the image
   builds but before the sandbox is verified. On this host that happened because a GPU
   library required at container start was missing:

     nemoclaw onboard --from "${WORKDIR}/Dockerfile" --name tp2 --non-interactive \
       --fresh --yes

3. Try the documented cleanup:

     nemoclaw tp2 destroy --yes

4. Apply the remedy that resolves the other variant of this state - make the owning
   gateway report the sandbox absent, then reconcile:

     openshell sandbox delete tp2
     nemoclaw tp2 destroy --yes

5. Inspect the registry row and the retained recovery record for that sandbox name.
```

## Expected Result

A retained-recovery record the product wrote itself can be reconciled through a supported
command, or the refusal names a concrete action the user can take to resolve the identity
conflict it reports.

## Actual Result

Step 3, verbatim:

  Refusing to destroy retained sandbox 'tp2': NemoClaw could not select exactly one
  recovery record from the current immutable registry and Docker identities. No sandbox
  resources were removed. Resolve the identity conflict, then rerun 'nemoclaw tp2 destroy'.

Step 4: the openshell delete succeeded and the gateway no longer reported the sandbox:

  Deleted sandbox tp2

but the reconcile rerun printed the identical refusal:

  Refusing to destroy retained sandbox 'tp2': NemoClaw could not select exactly one
  recovery record from the current immutable registry and Docker identities. ...

The record remained unresolved. So the remedy that works for the other variant of this
state does not help here.

Step 5: the sandbox registry row for this name exists but carries neither a
pending-create identity nor a lifecycle generation value, while a retained-recovery record
for the same name does exist with reason "retained_after_sandbox_creation_failure" and
identityWasUnavailable false.

For contrast, in the same session on a different host a sandbox whose registry row DID
carry both fields produced a different refusal that named a remedy, and following that
remedy destroyed the sandbox cleanly and returned the unresolved record count to zero.

The only way to clear the affected state was to edit product state files by hand.

## Logs

```text
Not captured beyond the terminal output quoted in Actual Result. The registry row and the
retained-recovery record contents described in step 5 were read directly from the
product's own state files on the test host.
```

## Additional acceptance criteria: concise recovery output

- Present the existing recovery outcome in this order: cause, retained state, supported next action, diagnostic reference.
- Replace `Resolve the identity conflict` with a supported command or a concrete operator action.
- If no supported recovery action exists, state that limitation directly. Do not imply that rerunning the same command can progress.
- Keep detailed identity and lifecycle evidence in diagnostics unless the user needs one value for the next action.
- Return a nonzero exit status when no resource was removed and no recovery record was reconciled.
- Assert the cause, retained state, next action, and exit status in tests. Do not assert an entire formatted paragraph.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8bb779046526e92956967cf27ae42c2c42c2d9b2`.  There
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
{"case_id": "NVIDIA_NemoClaw__11418__8bb7790",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
