# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[illumos] Assertion failed: num_ent * sizeof(mib2_udpEntry_t) == mibhdr.len

## Summary

* OS: OpenIndiana (illumos)
* Architecture: 64bit
* Psutil version: 7.0.0
* Python version: Python 3.9.21
* Type: core

## Description

I noticed the following core file while running tests:
```
> ::status
debugging core file of python3.9 (64-bit) from il-bld
file: /usr/bin/python3.9
initial argv: /usr/bin/python3.9 -m pytest --verbose --color=no
threading model: native threads
status: process terminated by SIGABRT (Abort), pid=12733 uid=5001 code=-1
libc panic message: Assertion failed: num_ent * sizeof(mib2_udpEntry_t) == mibhdr.len, file psutil/_psutil_sunos.c, line 1332, function psutil_net_connections
>
```
To solve the issue I use the following patch:
```
--- psutil-7.0.0/psutil/_psutil_sunos.c.orig
+++ psutil-7.0.0/psutil/_psutil_sunos.c
@@ -1327,7 +1327,7 @@
         }
 #endif
         // UDPv4
-        else if (mibhdr.level == MIB2_UDP || mibhdr.level == MIB2_UDP_ENTRY) {
+        else if (mibhdr.level == MIB2_UDP && mibhdr.name == MIB2_UDP_ENTRY) {
             num_ent = mibhdr.len / sizeof(mib2_udpEntry_t);
             assert(num_ent * sizeof(mib2_udpEntry_t) == mibhdr.len);
             for (i = 0; i < num_ent; i++) {
```
I confirmed that during the testing the condition is evaluated true at least once.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `963b2a0fabfc6cae9a9f5122abe6fe19dd92701a`.  There
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
{"case_id": "giampaolo_psutil__2545__963b2a0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
