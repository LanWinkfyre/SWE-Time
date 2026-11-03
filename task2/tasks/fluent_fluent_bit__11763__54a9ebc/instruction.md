# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_node_exporter_metrics: netstat collector missing TcpExt_*/IpExt_* from /proc/net/netstat

**Is your feature request related to a problem? Please describe.**
The `node_exporter_metrics` plugin's `netstat` collector documents itself as *"Exposes network statistics from /proc/net/netstat"* (https://docs.fluentbit.io/manual/data-pipeline/inputs/node-exporter-metrics).

In practice, the collector reads `/proc/net/snmp` (not `/proc/net/netstat`) and only processes the `Tcp:` and `Udp:` sections. None of the `TcpExt:` / `IpExt:` counters from `/proc/net/netstat` are emitted

**Describe the solution you'd like**
Extend the existing `netstat` collector to also read `/proc/net/netstat` (in addition to `/proc/net/snmp`) and emit `node_netstat_TcpExt_*` / `node_netstat_IpExt_*` from its `TcpExt:` / `IpExt:` sections.

**Additional context**
- Fluent-bit version where the gap was observed: 5.0.3 (fluent/fluent-bit:5.0.3)
- Doc page that references /proc/net/netstat as the source: https://docs.fluentbit.io/manual/data-pipeline/inputs/node-exporter-metrics
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `54a9ebcee2baeb5c67b1d1f4677e6eab4b11ae1b`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__11763__54a9ebc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
