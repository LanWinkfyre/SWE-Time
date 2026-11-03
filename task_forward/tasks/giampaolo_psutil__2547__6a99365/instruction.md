# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[illumos] `TestConnectedSocket.test_unix` fails

## Summary

* OS: OpenIndiana (illumos)
* Architecture: 64bit
* Psutil version: 7.0.0
* Python version: Python 3.9.21
* Type: core

## Description

The following test fails on OpenIndiana:
```
________________________ TestConnectedSocket.test_unix _________________________

self = <psutil.tests.test_connections.TestConnectedSocket testMethod=test_unix>

    @pytest.mark.skipif(not POSIX, reason="POSIX only")
    def test_unix(self):
        testfn = self.get_testfn()
        server, client = unix_socketpair(testfn)
        try:
>           cons = this_proc_net_connections(kind='unix')

psutil/tests/test_connections.py:232:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
psutil/tests/test_connections.py:50: in this_proc_net_connections
    cons = psutil.Process().net_connections(kind=kind)
psutil/__init__.py:1234: in net_connections
    _check_conn_kind(kind)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

kind = 'unix'

    def _check_conn_kind(kind):
        """Check net_connections()'s `kind` parameter."""
        kinds = tuple(_common.conn_tmap)
        if kind not in kinds:
            msg = f"invalid kind argument {kind!r}; valid ones are: {kinds}"
>           raise ValueError(msg)
E           ValueError: invalid kind argument 'unix'; valid ones are: ('all', 'tcp', 'tcp4', 'udp', 'udp4', 'inet', 'inet4', 'inet6', 'tcp6', 'udp6')

psutil/__init__.py:280: ValueError
```
When I revert (partially) changeset 5d4be42bd309dc3c7e93d5d319577ec4b8027445 using this:
```
--- psutil-7.0.0/psutil/_common.py.orig
+++ psutil-7.0.0/psutil/_common.py
@@ -249,7 +249,7 @@
         "udp6": ([AF_INET6], [SOCK_DGRAM]),
     })

-if AF_UNIX is not None and not SUNOS:
+if AF_UNIX is not None:
     conn_tmap.update({"unix": ([AF_UNIX], [SOCK_STREAM, SOCK_DGRAM])})


```
Then the test passes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6a99365b73950e6c9a8d2dade55a1a90aa5c450e`.  There
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
{"case_id": "giampaolo_psutil__2547__6a99365",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
