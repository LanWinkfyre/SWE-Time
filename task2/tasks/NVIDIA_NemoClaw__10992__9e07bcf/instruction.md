# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Phase 1 slice 4c: Route SSH command transport and version probes through the OpenShell adapter

Parent Epic: #9802

Originating capability: #9804

Implementation owner: @rsliter

## Outcome

Route SSH configuration, SSH-backed command transport, and sandbox version probes through typed OpenShell interfaces.

## Scope

- Add typed SSH configuration and SSH command requests and results required by current consumers.
- Keep OpenShell SSH-config commands, parsing, temporary files, SSH argv, and subprocess errors inside the CLI implementation.
- Migrate the SSH half of `src/lib/adapters/sandbox/command-transport.ts`.
- Migrate the live sandbox version probe in `src/lib/sandbox/version.ts`.
- Preserve current gateway targeting, timeout, output, and fallback behavior.

## Acceptance evidence

- Named gateway targeting resolves the same sandbox SSH host as before the refactor.
- Missing configuration, malformed configuration, timeout, transport failure, and remote nonzero exit remain distinct.
- Temporary SSH configuration keeps its current access scope and is removed after success or failure.
- Consumers do not parse OpenShell SSH configuration or construct SSH process arguments.

## Test plan

- CLI implementation tests for OpenShell commands, SSH-config parsing, SSH argv, timeout, error mapping, and cleanup.
- Command-transport and version tests against typed SSH fakes.
- Existing gateway-scoping, command-transport, sandbox-version, rebuild-preflight, and cleanup tests.
- Use runtime evidence only if local tests cannot prove terminal or SSH process behavior.

## Dependencies and sequencing

Depends on the first partial PR for #9804. Add that PR link after publication.

## Deferred scope

- Interactive connect and terminal session behavior, tracked by the Slice 4d follow-up.
- SDK SSH implementation.
- New host-verification policy.
- File transfer and persistent forwarding.

<!-- openshell-partial-delivery-follow-on -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9e07bcfa2bd944c84582ed787a7c1d15a5d6e4b7`.  There
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
{"case_id": "NVIDIA_NemoClaw__10992__9e07bcf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
