# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Stuck TLS Connection Hangs Fluent-bit and Consumes 100% CPU

## Bug Report

**Describe the bug**

Using fluent-bit 4.2.2 in docker container, discovered that occasionally, fluent-bit will hang and consume 100% of one CPU. It does this indefinitely and only a restart of the application will recover it.

Looking into it further, it seems that it's the forward input plugin (in my case) that is stuck reading data from open SSL

```
Thread 4 (Thread 0x7f5ac2dfe6c0 (LWP 8) "flb-in-forward."):
#0  0x00007f5ac611f104 in BIO_test_flags () from /lib/x86_64-linux-gnu/libcrypto.so.3
#1  0x00007f5ac66567a8 in ?? () from /lib/x86_64-linux-gnu/libssl.so.3
#2  0x000055d424e421fb in tls_net_read (session=0x7f5ac03d8588, buf=0x7f5abe9848af, len=<optimized out>) at /src/fluent-bit/src/tls/openssl.c:1312
#3  0x000055d424e42ed0 in flb_tls_net_read (session=0x7f5ac03d8588, buf=buf@entry=0x7f5abe9848af, len=len@entry=999953) at /src/fluent-bit/src/tls/flb_tls.c:343
#4  0x000055d424e55650 in flb_io_net_read (connection=connection@entry=0x7f5ac2014cc0, buf=0x7f5abe9848af, len=999953) at /src/fluent-bit/src/flb_io.c:750
#5  0x000055d424edebd5 in fw_conn_event_internal (connection=0x7f5ac2014cc0) at /src/fluent-bit/plugins/in_forward/fw_conn.c:95
#6  fw_conn_event (data=0x7f5ac2014cc0) at /src/fluent-bit/plugins/in_forward/fw_conn.c:145
#7  0x000055d424dff2dc in input_thread (data=0x7f5ac36e4340) at /src/fluent-bit/src/flb_input_thread.c:447
#8  0x000055d424e25e6c in step_callback (data=0x7f5ac3639c00) at /src/fluent-bit/src/flb_worker.c:43
#9  0x00007f5ac596cb7b in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:448
#10 0x00007f5ac59ea5f0 in clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:100
```
(This looks the same when I continue and stop it again)


**To Reproduce**

The applicable config is 
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
      tls: on
      tls.verify: off
      tls.crt_file: <fluentbit_tls_cert_path>
      tls.key_file: <fluentbit_tls_key_path>
```

The main way this seems to reproduce is if there is an unreliable network connection and frequent drops in connection. This is somewhat expected in my use case, so I am able to reproduce it more reliably.

**Expected behavior**
Should not consume 100% CPU and hang

**Screenshots**


**Your Environment**
* Version used: 4.2.2
* Configuration: (copied above)
* Environment name and version (e.g. Kubernetes? What version?): Docker container pulled from docker hub
* Server type and version: N/A
* Operating System and version: RHEL
* Filters and plugins:

**Additional context**
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `cb7256c2867494ae404ab6e3da936e8f6e0c9c94`.  There
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
{"case_id": "fluent_fluent_bit__11551__cb7256c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
