# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
syslog plugin: no warning when TLS enabled and mode == udp

## Bug Report

**Describe the bug**
When the syslog plugin is configured with `mode: udp` while TLS is enabled, it does not raise any error or warning. Instead, it silently falls back to sending logs over plain UDP without TLS. This behavior is misleading and can result in unencrypted log transmission without the user being aware.

**To Reproduce**

* Rubular link if applicable: N/A
* Example log message if applicable:


* Steps to reproduce the problem:

  1. Configure the syslog plugin with:

     * `mode: udp`
     * TLS-related options enabled (e.g., certificates configured)
  2. Start the service or logging pipeline
  3. Send a test log message
  4. Observe that logs are sent successfully over UDP without any TLS, and no error or warning is emitted

**Expected behavior**
The syslog plugin should fail fast and return an explicit error when `mode` is set to `udp` while TLS is enabled, since UDP does not support TLS. At minimum, it should log a clear warning and refuse to start with this invalid configuration.

**Screenshots**
N/A

**Your Environment**

* Version used: latest release and master branch
* Configuration: syslog plugin with `mode: udp` and TLS options enabled
* Environment name and version (e.g. Kubernetes? What version?): Linux and FreeBSD builds
* Server type and version: *
* Operating System and version: *
* Filters and plugins: syslog plugin

**Additional context**
This issue can lead to unintended insecure logging in production environments. Users may assume TLS is being used due to configuration, while logs are actually transmitted unencrypted over UDP. Failing fast on invalid configuration would prevent silent security misconfigurations and improve reliability.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c6111db72f3494c73aa35f6ab659a17655f6ca35`.  There
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
{"case_id": "fluent_fluent_bit__11703__c6111db",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
