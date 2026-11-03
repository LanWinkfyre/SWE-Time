# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_tail: memory usage does not decrease even after shipping all the log files

## Bug Report

**Describe the bug**
Fluent Bit’s memory usage does not decrease after all log files have been shipped, even when the ignore_older property is configured to stop monitoring older files. This suggests that memory is not being released as expected.

**To Reproduce**
- Start Fluent Bit on a directory containing a large number of log files (> 5,000).
- Configure the Tail input plugin with an output plugin (tested with file, s3, and stdout and the issue occurs in all cases).
- Continuously add new files until reaching ~55,000 files.
- Observe memory usage: it keeps increasing even after older files are ignored and shipped.

**Expected behavior**
Memory usage should decrease after all files have been shipped and older files are no longer monitored.

**Screenshots**

<img width="1210" height="308" alt="Image" src="https://github.com/user-attachments/assets/9f3b05b8-c321-4710-84b0-8085837a237f" />

**Your Environment**
* Version used: latest
* Configuration:
```
  http_server: on
  http_listen: localhost
  http_port: ${HEALTH_CHECK_PORT}
  health_check: on

pipeline:
  inputs:
    - name: tail
      path: path/to/files/*, path/to/files/*/*, path/to/files/*/*/*
      exclude_path: '*.log.0,*.log.1,*.log.2,*.log.3,*.log.4,*.log.5
      tag_regex: (path/to/files/*|path/to/files/*/*|path/to/files/*/*/*)(?<original_path>.*)
      tag: tail:<original_path>
      skip_long_lines: true
      ignore_older: 10m
      db: offsets.db
      db.locking: true
      inotify_watcher: false
      mem_buf_limit: 256MB
  filters:
    - name: lua
      match: tail:*
      script: compute_target_path.lua
      call: compute_target_path

    - name: rewrite_tag
      match: tail:*
      rule: $target_path ^(.*)$ $1 false

  outputs:
    - name: s3
      match: '*'
      endpoint: s3.endpoint.com
      bucket: test-bucket
      region: us-west-2
      profile: default
      use_put_object: false
      static_file_path: true
      s3_key_format: /s3/path/%Y/%m/%d/$TAG-%H_%M_%S
      log_key: log
      content_type: text
      upload_timeout: 5m
      upload_chunk_size: 10M
```
* Environment name and version: docker 
* Operating System and version: rhel-9
* Filters and plugins: see the configuration provided

**Additional context**
We are processing a very large number of files. The memory growth seems to originate from the Tail input plugin, as memory usage continues to increase with more files added, even when older files are ignored.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3a501b239fffffe199d769aaf36bb5d30fad2367`.  There
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
{"case_id": "fluent_fluent_bit__11282__3a501b2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
