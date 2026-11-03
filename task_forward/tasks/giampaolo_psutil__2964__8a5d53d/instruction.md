# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[POSIX] net_if_addrs() returns a bogus broadcast address for /32 addresses

Found this while running the test suite on an Alpine box on the GCC compile farm. The machine has an interface configured with a `/32` address:

```text
FAILED tests/test_linux.py::TestNetIfAddrs::test_ips
tests/test_linux.py:1088: in test_ips
    assert addr.broadcast == get_ipv4_broadcast(name)
E   AssertionError: assert '89.234.156.160' == '0.0.0.0'
```

psutil reports the interface's own IP as the broadcast address:

```console
$ ip -4 addr show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    inet 89.234.156.160/32 scope global eth0
```

```python
>>> psutil.net_if_addrs()["eth0"][0].broadcast
'89.234.156.160'
```

That's wrong. A `/32` represents a single host, so it has no broadcast address. 

The problem is in `psutil/arch/posix/net.c`. We read `ifa_broadaddr` whenever the interface has `IFF_BROADCAST`. But `IFF_BROADCAST` only says that the interface supports broadcasting; it doesn't mean every address assigned to it has a broadcast address.

This is not specific to musl or Alpine; glibc behaves the same way. 
The fix should be to return `None` when the netmask represents a single-host network.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8a5d53df33e28831f4833803b89e40e857d5632d`.  There
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
{"case_id": "giampaolo_psutil__2964__8a5d53d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
