# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Windows] net_io_counters() performance

## Summary

- OS: Windows
- Type: performance

## Description

I was troubleshooting a CPU usage issue in Dask https://github.com/dask/distributed/issues/9161, and noticed that its usage of `psutil.net_io_counters()` was inducing nontrivial CPU load in the "Service Host: DNS Client" task.  (Each Dask worker is calling this at least once a second, which is turning out to add up to something non-trivial on a many-core machine)

I traced this to the use of `GetAdaptersAddresses` in `psutil_get_nic_addresses`. Experimenting with this interface, I determined there are a few opportunities to speed this up, with differing orders of complexity, some anticipated by https://github.com/giampaolo/psutil/issues/1426

I made a CLI utility to make the same sequence of syscalls as `psutil.net_io_counters`, to benchmark. The base version calls `GetAdapterAddresses` once to get a buffer size, then again to fetch data. Then it calls `GetIfEntry2` for each interface (of which there are maybe a dozen on my machine).

These are the optimization "phases"

Base version: 6.6 msec.
Skip flags: 2.8 msec.
Skip flags & remember size: 1.6 msec  
Cache all interfaces: 0.5 ms  (Possibly too aggressive)


First, there are flags that can be provided to `GetAdaptersAddresses` to skip the collection of various information. I tested with `GAA_FLAG_SKIP_DNS_INFO  | GAA_FLAG_SKIP_UNICAST | GAA_FLAG_SKIP_ANYCAST | GAA_FLAG_SKIP_MULTICAST  | GAA_FLAG_SKIP_DNS_SERVER`  which skips all the skippable options except the friendly name. This may render it incompatible with other uses of psutil_get_nic_addresses, so it might be necessary to take an input parameter to indicate whether the full information should be collected. But this is a big win.

If we remember the buffer size from the first call to `GetAdaptersAddresses` we can re-use it, and it will almost always be correct, differing only when a new interface appears. This means we only call `GetAdaptersAddresses` once per call, instead of twice, which helps a fair bit. (And if it does change, we'll still detect this and update the cached size, we won't miss any interfaces).

If we remember all the interfaces and don't call `GetAdaptersAddresses` at all, we get an even bigger speedup. This was suggested as a future optimization in https://github.com/giampaolo/psutil/issues/1426 but it means not detecting new interfaces when they come up, which changes the semantics since new interfaces won't be noticed.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `35529fae02722c8fa586a091992946e64fab1094`.  There
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
{"case_id": "giampaolo_psutil__2695__35529fa",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
