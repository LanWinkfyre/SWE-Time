# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Complete asynchronous policy reads in portable lifecycle consumers

Parent capability: #9805. Parent epic: #9802.

## Outcome

Finish asynchronous policy observation for the Hermes portable lifecycle after the ordinary policy consumers migrate. Preserve the CLI transport, gateway targeting, currentness checks, and transaction authority.

## Scope and owner

Owner: @rsliter. This is the second consumer group in the accepted #9805 implementation, split to keep synchronous lock and uninstall changes independently reviewable.

- Migrate `proveHermesPortableLivePolicy` and its callers in portable onboarding, lifecycle qualification/requalification, startup checks, and uninstall authority capture.
- Await policy observation through the existing lifecycle wrappers and callbacks. Keep host fences and sandbox lifecycle locks held until the operation settles.
- Preserve bounded waits, failure classification, timing ownership, uninstall journal transitions, and cleanup order.
- Remove the transitional synchronous policy reader after its last consumer migrates.

## Acceptance

- A delayed policy observation cannot let startup, deletion, registry publication, or transaction advancement proceed early.
- A failed or malformed observation preserves the existing refusal and recovery result.
- Existing OpenClaw, Hermes, and portable lifecycle behavior remains unchanged outside policy observation.
- No production `src/` policy reader remains synchronous after completion.

## Validation

Use typed policy fakes with delayed and rejected promises; existing portable lifecycle, onboarding, uninstall, and lock tests; CLI type checks and required PR validation. Select focused live evidence only if the changed behavior requires a real boundary.

## Exclusions

No new policy semantics, runtime provider, uninstall design, retry policy, SDK transport, or dependency upgrade.

## Sequencing

Depends on #11483, which migrates ordinary policy and audit-setting consumers. The remaining synchronous reader is `createSyncCliOpenShellSandboxPolicyReader`, consumed by `proveHermesPortableLivePolicy` in `src/lib/onboard/experimental/hermes-portable-policy-state.ts`. Its direct production callers are portable lifecycle qualification/startup in `hermes-portable-lifecycle.ts` and the portable onboarding proof in `hermes-portable-onboarding.ts`; carry awaiting through their existing lifecycle, lock, and uninstall callers. Keep #9805 open until both consumer groups meet acceptance. Record final consumer disposition in #9813.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `633679ee17956c0035186eecc2dca7fea2d5d884`.  There
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
{"case_id": "NVIDIA_NemoClaw__11479__633679e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
