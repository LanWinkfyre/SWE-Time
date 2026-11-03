# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Phase 1 slice 4d: Route interactive connect and session handoff through the OpenShell adapter

Parent Epic: #9802

Originating capability: #9804

Implementation owner: @rsliter

## Outcome

Route interactive connect and command-session handoff through typed OpenShell interfaces.

## Scope

- Add the typed interactive-session controls required by current connect and launch consumers.
- Keep terminal mode, TTY selection, subprocess wiring, signal handling, and OpenShell CLI flags inside the CLI implementation.
- Migrate interactive paths in connect, launch, agent pass-through, and session pass-through.
- Preserve concurrent-session detection, cancellation, terminal restoration, and exit behavior.

## Acceptance evidence

- Interactive commands retain current TTY, stdin, stdout, stderr, and exit behavior.
- SIGINT, SIGTERM, explicit cancellation, transport failure, and remote exit remain distinct.
- Terminal state is restored after success, failure, or cancellation.
- Interactive paths do not widen credential, process, or terminal access.
- Consumers do not construct OpenShell CLI argv or inspect process-shaped results.

## Compatibility retirement

- Remove interactive callers of `buildOpenshellExecArgs`, `runSandboxExecChild`, and their process-shaped types after they use the typed interactive interface.
- Remove those compatibility exports when this issue and #10991 leave no production callers.
- Add a repository architecture assertion that rejects new production imports of the action-owned compatibility helpers.

## Test plan

- CLI implementation tests for TTY, streams, signals, cancellation, and terminal cleanup.
- Connect, launch, agent pass-through, and session pass-through tests against typed interactive-session fakes.
- Existing concurrent-session, connect-recovery, launch-routing, and terminal behavior tests.
- An architecture test that prevents new callers from depending on the action-owned argv and child-process helpers.
- Run focused runtime evidence only for behavior that mocks cannot prove.

## Dependencies and sequencing

Depends on the streamed command boundary in #10995 and may reuse the typed SSH boundary from #10992.

## Deferred scope

- User-facing terminal redesign.
- SDK interactive-session implementation.
- File transfer, persistent forwarding, and log fallback.

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
{"case_id": "NVIDIA_NemoClaw__10994__9e07bcf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
