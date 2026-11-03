# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Bug] Exclude Stopped sibling sandboxes from active Ollama ownership

Parent epic: https://github.com/NVIDIA/NemoClaw/issues/11573

A Stopped sibling prevents exclusive Ollama ownership discovery during stop. The real inventory parser omits Stopped and returns an unusable phase. If the parser alone recognizes Stopped, the ownership loop still counts that sibling as active.

Both boundaries were reproduced at `e9cf24220532e33e704298632d9006b30254efdd`. The failing regression uses the real parser.

## Reproduction

Stop a sandbox whose only sibling using the selected Ollama endpoint is Stopped. Parse actual inventory output through `parseCliOpenShellSandboxInventory`. Assert successful exclusive-owner discovery.

## Acceptance

- Recognize Stopped in the inventory parser.
- Exclude Stopped siblings from active ownership.
- Preserve conservative handling of unknown phases and unavailable inventory.
- Preserve models used by active siblings at the same daemon.
- Keep endpoint identity checks: the same model name at another port or remote endpoint does not establish shared ownership.
- Pass real-parser and endpoint regression tests. Distinguish ownership classification from live GPU memory-release evidence.

Affected code: `src/lib/adapters/openshell/sandbox-observer-cli.ts` and `src/lib/actions/sandbox/stop.ts`.


## Recorded evidence

The real inventory parser classified Stopped as an unusable phase. The exclusive-owner discovery assertion failed. A separate recognized-phase injection confirmed that changing only the parser still counts the sibling as active.

Reproduction baseline: `e9cf24220532e33e704298632d9006b30254efdd`. Canonical main was checked at `cad153cc1b761353e4a9590da7fa2f5121913056` before filing. The listed behavior owners are unchanged between those revisions; after-fix validation is pending.

- [Behavior owner: `src/lib/adapters/openshell/sandbox-observer-cli.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/adapters/openshell/sandbox-observer-cli.ts)
- [Behavior owner: `src/lib/actions/sandbox/stop.ts`](https://github.com/NVIDIA/NemoClaw/blob/e9cf24220532e33e704298632d9006b30254efdd/src/lib/actions/sandbox/stop.ts)

## Related work

The scope is active ownership discovery for Stopped siblings at the selected Ollama daemon. Live GPU memory release remains separate evidence.

## Delivery

One focused PR will link this issue with `Fixes`. It must include the before/after reproduction, relevant regression evidence, and review and CI outcomes for its final commit. Preserve installed kiosk launchers and existing user sandboxes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `74f14bf2179aba35e3db4adcb7e9626db522b1ef`.  There
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
{"case_id": "NVIDIA_NemoClaw__11650__74f14bf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
