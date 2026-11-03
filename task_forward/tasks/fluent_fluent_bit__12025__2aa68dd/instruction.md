# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Forward input: connection cleanup fails, hangs CPU at 100%

## Bug Report

**Describe the bug**
We have a setup where several fluent-bit instances feed one central one using the forward input/output plugins. We're seeing that every couple days of operation, the central instance (flb forward input) will hang with no log messages, and consume 100% of one CPU core.

A restart will bring everything back fine. 

Using ps, showed that the forward input thread was the one stuck consuming 100% CPU. I was able to attach gdb and determine that the thread is spinning in the event loop on a network socket that's in the CLOSED_WAIT state, but the handler never gets called and it never gets cleaned up (see first comment for more details).


**To Reproduce**
- Configure forward input plugin to receive lots of data from other fluent-bit instances whose connections may be a bit unstable.
- Using threaded forward input with TLS enabled
- I haven't been able to consistently reproduce this at will, it takes a few days for a production system to get into this state before I can debug.


**Expected behavior**
Fluent-bit does not hang 

**Screenshots**
<!--- If applicable, add screenshots to help explain your problem. -->

**Your Environment**

* Version used: v5.0.7
* Configuration: 
```
pipeline:
  inputs:
    - name: forward
      listen: 0.0.0.0
      port: 24224
      buffer_chunk_size: 1M
      buffer_max_size: 100M
      threaded: True
      storage.type: filesystem
      net.keepalive: on

      # Set IO timeout to to give up on connection if it's unresponsive
      net.io_timeout: 20

      # TLS Configuration
      tls: on
      tls.verify: off
      tls.crt_file: /etc/fluent-bit/certs/server.crt
      tls.key_file: /etc/fluent-bit/certs/server.key
```


* Environment name and version (e.g. Kubernetes? What version?): docker container
* Server type and version: Several different ones
* Operating System and version: reproduced on a RHEL and Ubuntu system
* Filters and plugins:

**Additional context**
Unfortunately, this has started to happen more frequently as it gets deployed across more servers requiring restarts of the service
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2aa68dd1a3ca68a8a62de329ff733d70fdc9fbc8`.  There
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
{"case_id": "fluent_fluent_bit__12025__2aa68dd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
