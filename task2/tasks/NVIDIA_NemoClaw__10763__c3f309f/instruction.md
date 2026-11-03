# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
internal uninstall plan previews the wrong gateway on a non-default port

## Summary

`nemoclaw internal uninstall plan` previews the wrong gateway on a non-default
`NEMOCLAW_GATEWAY_PORT`. It defaults `--gateway` to the literal `nemoclaw`, while
`internal uninstall run-plan` defaults to `resolveGatewayName(GATEWAY_PORT)`, so the
preview names the default environment's gateway and Docker volume as removal targets.

## Steps to reproduce

```
$ NEMOCLAW_GATEWAY_PORT=8091 nemoclaw internal uninstall plan --json
gatewayName: nemoclaw
  {'kind': 'destroy-openshell-gateway', 'name': 'nemoclaw'}
  {'kind': 'delete-docker-volume', 'name': 'openshell-cluster-nemoclaw'}
  {'path': '<home>/.nemoclaw/gateways/8091'}
```

## Expected

`nemoclaw-8091` and `openshell-cluster-nemoclaw-8091`, matching what `run-plan` removes:

```
$ NEMOCLAW_GATEWAY_PORT=8091 nemoclaw internal uninstall run-plan --help
      --gateway=<value>    [default: nemoclaw-8091] Gateway name
```

## Notes

The same plan already reports the port-scoped state root `~/.nemoclaw/gateways/8091`, so a
single plan mixes two gateways. #6711 introduced the per-port binding and updated
`run-plan.ts` and the path resolver, but not `src/commands/internal/uninstall/plan.ts`.

Signed-off-by: Udaya Tejas <udayatejas2004@gmail.com>
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c3f309f2f344a4b25e58d204e0b423e54a4cb379`.  There
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
{"case_id": "NVIDIA_NemoClaw__10763__c3f309f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
