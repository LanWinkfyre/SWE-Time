# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
S3 output buffer consumed by stale files after multiple failed retries

## Bug Report

**Describe the bug**
On s3 failures, files are left stale on disk and thus do not relinquish output buffer space back by removing the file and decrementing `current_buffer_size`. Repeated errors cause stale output files to persist in the buffer which the output handler is completely unaware of, so errors accumulate into a full output buffer and can no longer process any data.

i.e. Occasional failures on S3 uploads (of which there are a lot) gradually stack up to consume every byte of `StoreDirLimitSize` until everything grinds to a complete halt and the pod gets killed.

This appears to be related to these lines:
- https://github.com/fluent/fluent-bit/blob/master/plugins/out_s3/s3.c#L1965 < This is the line specific to this bug, but the one below may also experience the same issue. 
- https://github.com/fluent/fluent-bit/blob/master/plugins/out_s3/s3.c#L3866

In both cases:
- `s3_store_file_inactive` is called 
- Which, in turn calls `flb_fstore_file_inactive`
- This function closes the I/O but _intentionally_ does not delete the file
- Nothing behind `s3_store_file_inactive` liberates buffer space, even though all references to that file have been relinquished and the output has 'given up' with the file.
  - As opposed to `s3_store_file_delete` which *does* release buffer space: `ctx->current_buffer_size -= s3_file->size;` and deletes the file
  - Obviously, `s3_store_file_inactive` is not relinquishing buffer space _because_ it's not deleting the files.

In conjunction with this, v4.2.3 also has an off-by-one error (fixed in later versions) so `retry_limit = 1` is actually 'No retries', and this opt defaults to `1` rather than `5` as seen in previous versions. Thus, on v4.2.3 if you are not manually specifying a retryLimit > 1, transient failures become a catastrophic loss of records and the buffer will be permanently tainted with those lost records. 

**To Reproduce**
- Rubular link if applicable: u/k
- Example log message if applicable:

There's lots of correlative bits of information here, so bear with me:

Files on disk:

```text
-rw-------    1 root     root       1183744 Apr 29 11:41 12681897966366703112-14606954368872656564
-rw-------    1 root     root       3411968 Apr 29 11:41 15393042439759612772-10689248011551476248
-rw-------    1 root     root        102400 Apr 29 11:41 16404582273068644347-5967513073307950096
-rw-------    1 root     root      10391552 Apr 29 11:41 17968601020670848119-7239896667824836330
-rw-------    1 root     root          4096 Apr 29 11:41 17266151877237876228-6718229405376101401
-rw-------    1 root     root         36864 Apr 29 11:41 16956281325476515959-5472663707595791072
-rw-------    1 root     root      12128256 Apr 29 11:39 17968601020670848119-17888715470891049674
-rw-------    1 root     root      13570048 Apr 29 11:36 17968601020670848119-9719238430729505548
-rw-------    1 root     root      13242368 Apr 29 11:17 17968601020670848119-2361698986790864637
-rw-------    1 root     root      12292096 Apr 29 11:04 15393042439759612772-18069702356910709128
-rw-------    1 root     root      20221952 Apr 29 11:01 17968601020670848119-13084062489286803840
-rw-------    1 root     root      11636736 Apr 29 10:57 17968601020670848119-11644061896093015244
-rw-------    1 root     root      12652544 Apr 29 10:54 17968601020670848119-294124939407482723
-rw-------    1 root     root          4096 Apr 29 10:54 18346669338110208780-8330162164832928582
-rw-------    1 root     root      12324864 Apr 29 10:51 17968601020670848119-6978170714041475120
-rw-------    1 root     root      14684160 Apr 29 10:24 17968601020670848119-13808492304039359588
-rw-------    1 root     root      12062720 Apr 29 10:17 17968601020670848119-12665229349350099937
-rw-------    1 root     root      13275136 Apr 29 10:16 17968601020670848119-6725517038024379648
-rw-------    1 root     root      12324864 Apr 29 10:15 17968601020670848119-8189199610958239434
-rw-------    1 root     root      14028800 Apr 29 10:12 17968601020670848119-11088013945658484385
-rw-------    1 root     root      13799424 Apr 29 10:10 17968601020670848119-13726761029458994180
-rw-------    1 root     root        495616 Apr 29 10:10 16404582273068644347-11939250306710512735
-rw-------    1 root     root      13209600 Apr 29 10:09 17968601020670848119-17079909337996210440
-rw-------    1 root     root      10293248 Apr 29 09:58 17968601020670848119-5303520551613184777
-rw-------    1 root     root      10948608 Apr 29 09:50 17968601020670848119-6142455639810240160
-rw-------    1 root     root      12947456 Apr 29 09:35 15393042439759612772-2661160915295300259
-rw-------    1 root     root      19304448 Apr 29 09:04 15393042439759612772-4886553951790287162
-rw-------    1 root     root      20025344 Apr 29 09:03 17968601020670848119-11363852993441694475
-rw-------    1 root     root      20254720 Apr 29 09:02 17968601020670848119-11574945865466687512
-rw-------    1 root     root       8327168 Apr 29 08:58 15393042439759612772-17961139713936533472
-rw-------    1 root     root      11014144 Apr 29 08:44 17968601020670848119-10742523279820995919
-rw-------    1 root     root      12357632 Apr 29 08:38 17968601020670848119-13542879461489352312
-rw-------    1 root     root      15273984 Apr 29 08:22 17968601020670848119-8991173050528632184
-rw-------    1 root     root      10915840 Apr 29 08:18 17968601020670848119-3867850942261909169
-rw-------    1 root     root      11014144 Apr 29 08:17 17968601020670848119-2611234149650838141
-rw-------    1 root     root      10883072 Apr 29 08:14 17968601020670848119-3227245893658905412
-rw-------    1 root     root      11866112 Apr 29 08:10 17968601020670848119-16407279727121294508
-rw-------    1 root     root      19468288 Apr 29 08:00 17968601020670848119-1756037490726720884
```

Error logs for latest error (redacted):

```text
[2026/04/29 11:39:11.873176864] [debug] [upstream] KA connection #45 to s3.eu-central-1.amazonaws.com:443 has been assigned (recycled)
[2026/04/29 11:39:11.873191674] [debug] [http_client] not using http_proxy for header 
[2026/04/29 11:39:11.873207925] [debug] [aws_credentials] Requesting credentials from the EKS provider..
[2026/04/29 11:39:11.873821001] [error] [http_client] broken connection to s3.eu-central-1.amazonaws.com:443 ?
[2026/04/29 11:39:11.873834421] [debug] [aws_client] s3.eu-central-1.amazonaws.com: http_do=-1, HTTP Status: 0 
[2026/04/29 11:39:11.873849522] [debug] [upstream] KA connection #45 to s3.eu-central-1.amazonaws.com:443 is now available
[2026/04/29 11:39:11.873857062] [debug] [aws_client] auto-retrying
[2026/04/29 11:39:11.873864952] [debug] [upstream] KA connection #45 to s3.eu-central-1.amazonaws.com:443 has been assigned (recycled)
[2026/04/29 11:39:11.873871012] [debug] [http_client] not using http_proxy for header
[2026/04/29 11:39:11.873884672] [debug] [aws_credentials] Requesting credentials from the EKS provider..
[2026/04/29 11:39:11.968864211] [error] [http_client] broken connection to s3.eu-central-1.amazonaws.com:443 ? 
[2026/04/29 11:39:11.968878961] [debug] [aws_client] s3.eu-central-1.amazonaws.com: http_do=-1, HTTP Status: 0
[2026/04/29 11:39:11.968893262] [debug] [upstream] KA connection #45 to s3.eu-central-1.amazonaws.com:443 is now available
[2026/04/29 11:39:11.968899502] [error] [output:s3:<name>] PutObject request failed 
[2026/04/29 11:39:11.969948899] [ warn] [output:s3:<name>] Chunk file failed to send 1 times, will not retry
```

We have debug logging on at the moment, so we don't have logs dating back for all the stale files - but the stale files on disk correlate quite nicely with errors reported in the stats:

<img width="1894" height="798" alt="Image" src="https://github.com/user-attachments/assets/c53875d3-10be-4b79-a53f-ba715b0b867a" />

- Steps to reproduce the problem:

I actually don't know how to reproduce it without temporarily breaking S3 outbounds or something? This is just something we are actively experiencing. 

**Expected behavior**

Files should be deleted rather than left stale on disk. I suspect it would be more appropriate to use `s3_store_file_delete` in this case, unless there's a specific reason as to why fluent does *not* do this. 

**Screenshots**
n/a. All screenshots etc are included with bug logs/info.

**Your Environment**
* Version used: Fluent-bit v4.2.3 // Fluent-operator v3.5.0
* Configuration: 

```yaml
# cluster config
[...]
    flushSeconds: 1
    hcErrorsCount: 5
    hcPeriod: 5
    hcRetryFailureCount: 5
    healthCheck: true
    httpServer: true
    logLevel: debug
    parsersFile: parsers.conf
    storage:
      backlogMemLimit: 50MB
      checksum: 'off'
      deleteIrrecoverableChunks: 'on'
      maxChunksUp: 128
      metrics: 'on'
      path: /host/fluent-bit-buffer/
      sync: normal
```

```yaml
# s3 output config (redacted)
[...]
  s3:
    Bucket: [BUCKET]
    Compression: gzip
    Region: eu-central-1
    S3KeyFormat: [IRRELEVANT] 
    StaticFilePath: true
    StoreDirLimitSize: 500m
    TotalFileSize: 20M
    UploadTimeout: 60s
    UsePutObject: true
```

* Environment name and version (e.g. Kubernetes? What version?): Kubernetes (EKS) v1.33.5
* Server type and version: 
* Operating System and version: 
* Filters and plugins: Tail, but specifically S3 output relevant to this case.

**Additional context**
We have enabled `RetryLimit: 5` on the output config, which appears to be smoothing over the transient failures quite nicely, and there are no longer stale files on disk. However, if a user is _intentionally_ not retrying uploads or has not specified a retry limit on v4.2.3, they will be affected by this bug.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6474297f3d6e540848d9116f05570b9d8a8501b2`.  There
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
{"case_id": "fluent_fluent_bit__11759__6474297",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
