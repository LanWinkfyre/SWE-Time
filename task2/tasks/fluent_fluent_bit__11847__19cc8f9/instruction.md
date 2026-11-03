# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Fluent Bit 5.0.5 becomes non-functional after corrupted filesystem storage chunks

## Bug Report

**Describe the bug**
Fluent Bit 5.0.5 reported many filesystem storage chunk errors during startup, for both `tail.*` chunks and `emitter.*` chunks:

- `[storage] [cio file] invalid crc32`
- `[storage] format check failed`

After that, the Fluent Bit pod stayed running, but the agent did not collect/forward logs from that Kubernetes node. The pod did not crash, so the DaemonSet did not automatically replace it.

After manually deleting the Fluent Bit pod, the DaemonSet recreated it and Fluent Bit started working again. I did not manually delete the corrupted `.flb` chunks from the filesystem storage directory before recreating the pod.

This caused logs from workloads scheduled on that node to be missing. In our case, around 85% of the affected Airflow task pods were scheduled on the same worker node, and the Fluent Bit pod on that node was in this bad state.

This looks different from https://github.com/fluent/fluent-bit/issues/5003 because in this case Fluent Bit did not obviously crash. Instead, the pod stayed running but did not collect/forward logs correctly.

**To Reproduce**
- Example log message if applicable:
```
[2026/05/22 11:20:21.557] [ info] Configuration:
[2026/05/22 11:20:21.557] [ info]  flush time     | 1.000000 seconds
[2026/05/22 11:20:21.557] [ info]  grace          | 5 seconds
[2026/05/22 11:20:21.557] [ info]  daemon         | 0
[2026/05/22 11:20:21.557] [ info] ___________
[2026/05/22 11:20:21.557] [ info]  inputs:
[2026/05/22 11:20:21.557] [ info] ___________
[2026/05/22 11:20:21.557] [ info]  filters:
[2026/05/22 11:20:21.557] [ info] ___________
[2026/05/22 11:20:21.557] [ info]  outputs:
[2026/05/22 11:20:21.557] [ info] ___________
[2026/05/22 11:20:21.557] [ info]  collectors:
[2026/05/22 11:20:21.599] [ info] [fluent bit] version=5.0.5, commit=05121015a7, pid=1
[2026/05/22 11:20:21.599] [debug] [engine] coroutine stack size: 24576 bytes (24.0K)
[2026/05/22 11:20:21.599] [ info] [storage] [cio file] invalid crc32 at 1-177560529.168611552.flb/var/log/fluent-bit-storage/tail.5/1-177560529.168611552.flb
[2026/05/22 11:20:21.599] [error] [storage] format check failed: tail.5/1-177560529.168611552.flb
[2026/05/22 11:20:21.599] [ info] [storage] [cio file] invalid crc32 at 1-177560529.188062249.flb/var/log/fluent-bit-storage/tail.5/1-177560529.188062249.flb
[2026/05/22 11:20:21.599] [error] [storage] format check failed: tail.5/1-177560529.188062249.flb
[2026/05/22 11:20:21.599] [ info] [storage] [cio file] invalid crc32 at 1-177560529.205007451.flb/var/log/fluent-bit-storage/tail.5/1-177560529.205007451.flb
[2026/05/22 11:20:21.599] [error] [storage] format check failed: tail.5/1-177560529.205007451.flb
[2026/05/22 11:20:21.599] [ info] [storage] [cio file] invalid crc32 at 1-177560529.22498632.flb/var/log/fluent-bit-storage/tail.5/1-177560529.22498632.flb
[2026/05/22 11:20:21.599] [error] [storage] format check failed: tail.5/1-177560529.22498632.flb
[2026/05/22 11:20:21.599] [ info] [storage] [cio file] invalid crc32 at 1-177560529.237614716.flb/var/log/fluent-bit-storage/tail.5/1-177560529.237614716.flb
[2026/05/22 11:20:21.599] [error] [storage] format check failed: tail.5/1-177560529.237614716.flb
[2026/05/22 11:20:21.599] [ info] [storage] [cio file] invalid crc32 at 1-177560529.247818917.flb/var/log/fluent-bit-storage/tail.5/1-177560529.247818917.flb
[2026/05/22 11:20:21.599] [error] [storage] format check failed: tail.5/1-177560529.247818917.flb
...
[2026/05/22 11:20:21.562] [error] [storage] format check failed: emitter.39/1-1775223090.93727533.flb
[2026/05/22 11:20:21.562] [ info] [storage] [cio file] invalid crc32 at 1-1775223090.937498086.flb/var/log/fluent-bit-storage/emitter.39/1-1775223090.937498086.flb
[2026/05/22 11:20:21.562] [error] [storage] format check failed: emitter.39/1-1775223090.937498086.flb
[2026/05/22 11:20:21.562] [ info] [storage] [cio file] invalid crc32 at 1-1775484933.923154068.flb/var/log/fluent-bit-storage/emitter.39/1-1775484933.923154068.flb
[2026/05/22 11:20:21.562] [error] [storage] format check failed: emitter.39/1-1775484933.923154068.flb
[2026/05/22 11:20:21.562] [ info] [storage] [cio file] invalid crc32 at 1-1775554685.944618710.flb/var/log/fluent-bit-storage/emitter.39/1-1775554685.944618710.flb
[2026/05/22 11:20:21.562] [error] [storage] format check failed: emitter.39/1-1775554685.944618710.flb
[2026/05/22 11:20:21.562] [ info] [storage] [cio file] invalid crc32 at 1-1775605028.933645422.flb/var/log/fluent-bit-storage/emitter.39/1-1775605028.933645422.flb
[2026/05/22 11:20:21.562] [error] [storage] format check failed: emitter.39/1-1775605028.933645422.flb
[2026/05/22 11:20:21.562] [ info] [storage] [cio file] invalid crc32 at 1-1775667191.938036179.flb/var/log/fluent-bit-storage/emitter.39/1-1775667191.938036179.flb
[2026/05/22 11:20:21.562] [error] [storage] format check failed: emitter.39/1-1775667191.938036179.flb
[2026/05/22 11:20:21.562] [ info] [storage] [cio file] invalid crc32 at 1-1776043821.942157237.flb/var/log/fluent-bit-storage/emitter.39/1-1776043821.942157237.flb
[2026/05/22 11:20:21.562] [error] [storage] format check failed: emitter.39/1-1776043821.942157237.flb
[2026/05/22 11:20:21.562] [ info] [storage] [cio file] invalid crc32 at 1-1776343372.92255743.flb/var/log/fluent-bit-storage/emitter.39/1-1776343372.92255743.flb
[2026/05/22 11:20:21.562] [error] [storage] format check failed: emitter.39/1-1776343372.92255743.flb
[2026/05/22 11:20:21.562] [ info] [storage] ver=1.5.4, type=memory+filesystem, sync=normal, checksum=on, max_chunks_up=128
[2026/05/22 11:20:21.562] [ info] [storage] backlog input plugin: storage_backlog.0
[2026/05/22 11:20:21.562] [ info] [simd    ] SSE2
[2026/05/22 11:20:21.562] [ info] [cmetrics] version=1.0.3
[2026/05/22 11:20:21.562] [ info] [ctraces ] version=0.7.1
[2026/05/22 11:20:21.562] [ info] [input:storage_backlog:storage_backlog.0] initializing
[2026/05/22 11:20:21.562] [ info] [input:storage_backlog:storage_backlog.0] storage_strategy='memory' (memory only)
[2026/05/22 11:20:21.562] [debug] [storage_backlog:storage_backlog.0] created event channels: read=21 write=22
[2026/05/22 11:20:21.562] [ info] [input:storage_backlog:storage_backlog.0] queue memory limit: 95.4M
[2026/05/22 11:20:21.562] [debug] [downstream] listening on 0.0.0.0:2020
[2026/05/22 11:20:21.562] [ info] [http_server] listen iface=0.0.0.0 tcp_port=2020
[2026/05/22 11:20:21.562] [ info] [sp] stream processor started
[2026/05/22 11:20:21.562] [ info] [engine] Shutdown Grace Period=5, Shutdown Input Grace Period=2
```
- Steps to reproduce the problem:
1. Run Fluent Bit 5.0.5 as a Kubernetes DaemonSet.
2. Enable filesystem buffering for Tail input.
3. Enable storage checksum and deletion of irrecoverable chunks.
4. Let Fluent Bit accumulate some filesystem storage chunks.
5. Restart the Fluent Bit pod on one node or restart the node abruptly to try to trigger corrupted chunks
6. During startup, Fluent Bit reports many invalid crc32 and format check failed messages for existing .flb chunks under /var/log/fluent-bit-storage.
7. The pod remains running, but the agent does not collect/forward logs from that node.
8. Delete the pod manually and let the DaemonSet recreate it.
9. The newly recreated pod starts working again, without manually deleting the corrupted .flb chunk files.

**Expected behavior**
When Fluent Bit detects corrupted filesystem storage chunks during startup, especially with storage.checksum: on and storage.delete_irrecoverable_chunks: on, it should either: delete/drop/quarantine the corrupted chunks and continue collecting new logs normally, or fail clearly and exit, so Kubernetes can restart the pod.
It should not remain running in a state where the pod looks healthy but the agent does not collect or forward logs.

**Your Environment**
<!--- Include as many relevant details about the environment you experienced the bug in -->
* Version used: 5.0.5-debug
* Configuration: 
   <img width="538" height="363" alt="Image" src="https://github.com/user-attachments/assets/aa177c10-ef44-4116-b44a-8d053efe32cb" />

* Environment name and version (e.g. Kubernetes? What version?): Openshift with version 4.20

Could you please confirm whether `storage.delete_irrecoverable_chunks: on` is expected to delete these chunks during startup recovery, and whether Fluent Bit should continue collecting new logs after these `invalid crc32` / `format check failed` messages?
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `19cc8f9c63ab23bb98404b76407c9c81ab2b6914`.  There
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
{"case_id": "fluent_fluent_bit__11847__19cc8f9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
