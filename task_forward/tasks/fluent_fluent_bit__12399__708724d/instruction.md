# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Support RFC 6587 in out_syslog

**Is your feature request related to a problem? Please describe.**
Current implementation of `out_syslog` does not support octet counting which is required for sending multiline log messages. The `in_syslog` module `format` parameter supports both `newline` and `octet_counting` options, but `out_syslog` does not.

**Describe the solution you'd like**
Add support for RFC 6587, perhaps with a new `syslog_framing` parameter with `newline` and `octet_counting` values.

**Describe alternatives you've considered**
Not using FluentBit

**Additional context**
- Would be great to have a `syslog_sd_preset` that works in the same way as other `_preset` suffix fields
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `708724d97f6ce96a65b97d8330d6d38469ca745a`.  There
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
{"case_id": "fluent_fluent_bit__12399__708724d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
