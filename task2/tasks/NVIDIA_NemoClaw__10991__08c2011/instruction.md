# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Phase 1 slice 4b: Route buffered sandbox exec consumers through the OpenShell adapter

Parent Epic: #9802

Originating capability: #9804

Implementation owner: @rsliter

## Outcome

Route buffered sandbox execution and probe consumers through the typed OpenShell command interface.

## Scope

- Add typed buffered command requests and results for environment, input, stdout, stderr, exit status, signals, timeout, and transport failure.
- Keep OpenShell CLI flags, subprocess environment, output capture, and process errors inside the CLI implementation.
- Migrate the buffered half of `src/lib/adapters/sandbox/command-transport.ts`.
- Migrate onboarding verification, health probes, agent setup, binary checks, and compatible-endpoint smoke checks that are in scope for #9804.
- Preserve existing local Docker fallback decisions without widening fallback eligibility.

## Acceptance evidence

- Command arguments, working directory, environment, input, stdout, stderr, and exit status retain their current meaning.
- Timeout, missing executable, transport failure, malformed output, and remote nonzero exit remain distinct.
- A failed OpenShell command does not trigger a broader or ambiguous retry.
- Consumers use typed results and do not inspect CLI argv or process-shaped results.

## Compatibility retirement

- Remove buffered callers of `buildOpenshellExecArgs` after they use the typed buffered interface.
- Remove the compatibility export when this issue and #10994 leave no production callers.
- Add a repository architecture assertion that rejects new buffered imports of the action-owned compatibility helper.

## Test plan

- CLI implementation tests for command construction, environment, input, capture limits, timeout, and failure mapping.
- Consumer tests against a typed buffered-command fake.
- Existing command-transport, onboarding verification, health-probe, agent setup, and compatible-endpoint tests.
- An architecture test that prevents new buffered callers from depending on `buildOpenshellExecArgs`.
- Run the affected Vitest projects and repository architecture checks.

## Dependencies and sequencing

Depends on the streamed command boundary in #10995.

## Deferred scope

- SSH configuration and SSH-backed command transport, tracked by #10992.
- Interactive connect and terminal session behavior, tracked by #10994.
- SDK command implementation.
- File transfer, persistent forwarding, and log fallback.

<!-- openshell-partial-delivery-follow-on -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `08c2011321168ee506f030c8cf66c72b16a42a63`.  There
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
{"case_id": "NVIDIA_NemoClaw__10991__08c2011",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
