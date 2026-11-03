# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
out: syslog: `mode:tls` without `tls:on` sends plaintext over TCP.

## Bug Report

**Describe the bug**
Found while updating the docs for a code change that was missing a corresponding docs PR on `pipeline/outputs/syslog.md`, it's a source issue rather than a doc gap: 

`mode:tls` does not by itself enable `TLS`. `FLB_SYSLOG_TLS` is parsed at `syslog_conf.c:97` and then never read again — `io_flags` is chosen purely from `ins->use_tls` (syslog.c:1032-1043), so `mode:tls` without `tls:on` sends plaintext over TCP. 

Need a code change for the syslog output plugin to reject that combination the way it rejects the other two. 

**To Reproduce**
`mode:tls` does not by itself enable `TLS. FLB_SYSLOG_TLS` is parsed at `syslog_conf.c:97` and then never read again — `io_flags` is chosen purely from `ins->use_tls` (syslog.c:1032-1043), so `mode:tls` without `tls:on` sends plaintext over TCP.

**Expected behavior**
It should reject sending plain text over TCP by not accepting the above described configuration.

**Screenshots**
N/A

**Your Environment**
This dates to v1.9.6 (June 2022), so 2.x, 3.x, and 4.x are all affected too. The cause is commit f43f3a137, "out_syslog: fix TLS handling in config and code logic (fix #5643)" (PR #5646), whose message says:

▎ - the 'mode' option no longer accepts 'tls' as a value.
▎ - if TLS is needed the user needs to: set 'mode' to 'tcp', enable TLS by adding a line like 'tls on'

That commit changed `io_flags` in `syslog.c` but never removed the "tls" branch from the mode parser, so the intent was only half-implemented. I confirmed `syslog_conf.c` still accepts "tls" in every release from v1.9.5 through v5.0.7 and master, while v1.9.5 was the last version where `mode:tls` actually selected `FLB_IO_TLS`.

* Version used: see above
* Configuration: see above
* Environment name and version (e.g. Kubernetes? What version?): All
* Server type and version: All
* Operating System and version: All
* Filters and plugins: output plugin syslog

**Additional context**
Three options:
- Error when `mode: tls` and `tls` is `off` — this is my plan, consistent with the `dtls` and `udp` validations, and breaks no working config.
- Make `mode: tls` imply `tls:on` — friendlier, but silently flips existing deployments from plaintext to `TLS`, which will surface as connection failures.
- Reject `mode:tls` entirely — matches the 2022 intent, but breaks configs that today pair mode: `tls` with `tls:on` and work fine.

Happy to hear suggestions on the fix to pick from this list?
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e1ec87c466d8572720f5bb335172269188b45245`.  There
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
{"case_id": "fluent_fluent_bit__12193__e1ec87c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
