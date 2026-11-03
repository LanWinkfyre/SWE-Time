# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Epic: optimize Hermes stopped-container recovery latency

## Outcome

Track and deliver measured reductions in Hermes Portable stopped-container recovery latency while preserving exact receipt, runtime, executable, container, policy, health, and rollback authority.

A Portable B40 stopped-recovery investigation reduced one measured compatible candidate from 24.181 seconds to 19.478/19.358 seconds total. Detailed timing identified repeated Podman executable authority work and exact-container subprocess captures as the dominant recoverable control-plane costs. These observations are directional evidence, not an SLO or generalized performance claim.

## Confirmed Scope

Core NemoClaw, limited to the accepted experimental Hermes Portable recovery contract in #10423 and #9211. This epic does not widen the supported runtime or platform matrix.

Optimization must preserve:

- full entry qualification;
- full final qualification;
- operation-local lifecycle locking and receipt generation fences;
- exact Podman socket and executable authority;
- exact full container ID, image, labels, name, sandbox identity, status, and restart policy;
- live OpenShell policy and registry binding;
- credential-safe authenticated health;
- bounded deadlines, ambiguous-mutation reconciliation, and exact rollback;
- credential-free timing output.

## Accountable Maintainer

@jyaunches

## Capability Slices

- [ ] Complete Hermes recovery timing coverage across every normal recovery path.
- [ ] Share one opaque, operation-local Podman executable proof across bound engines.
- [ ] Use retained metadata checks with operation-wide periodic full rehash and failure latching.
- [ ] Remove duplicate executable checks around Podman captures without removing adapter guards.
- [ ] Reuse receipt-bound exact-container observations only within one health iteration.
- [ ] Reduce Hermes forward-recovery subprocess and settlement overhead using additive measurements.

Each capability is tracked as a linked subissue. For CI/CD expediency, the first five implementation slices may be delivered in one reviewed PR, while retaining separate commits/tests and issue relationships for attribution.

## Validation Contract

Deterministic tests must cover allowed, denied, drift, ambiguous mutation, rollback, and timing-sink failure states. In particular:

- caller-forged proof rejection;
- full rehash at commands 64 and 128 across shared engines;
- stable-metadata byte drift and metadata identity drift;
- socket-precheck and thrown-capture counter semantics;
- cross-engine failure latching;
- receipt-bound reused observations before credential-bearing health;
- running/unpaused/status/restart-policy requirements;
- fresh observations after health, mutation, OpenShell command, sleep, and every poll;
- managed-bootstrap and workload-cleanup preservation;
- unchanged full entry and final qualification.

Controlled runtime evidence must record exact build/image/container/policy identity and compare expected counters before wall-clock totals. A complete current-source candidate image is required when packaged runtime boundaries differ from an older deployed image.

## Delivery and Stop Conditions

1. Land observability before claiming optimization impact.
2. Keep structural proof ownership separate from validation-frequency changes in review evidence.
3. Do not remove full final qualification or weaken ownership/rollback to meet a latency target.
4. Stop if a change requires trusting TCP reachability, names instead of immutable IDs, caller-supplied verification callbacks, or stale observations across an external boundary.

## Related Work

- #10839 merged detailed Hermes currentness and container-inspection timing.
- #10830 explores scheduling authenticated health from image readiness.
- The original #10822 forward-recovery optimization scope is preserved in its dedicated child issue.

## Category

Platform / Performance
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6831ed251641b6885939deef6dd34bf3e10266b0`.  There
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
{"case_id": "NVIDIA_NemoClaw__10822__6831ed2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
