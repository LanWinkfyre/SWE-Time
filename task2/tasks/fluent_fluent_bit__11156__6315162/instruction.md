# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_systemd: add journal namespace feature

**Is your feature request related to a problem? Please describe.**
I use systemd-journald namespace to isolate my application log.

**Describe the solution you'd like**
Add `Namespace` option, then use [`sd_journal_open_namespace`](https://www.freedesktop.org/software/systemd/man/latest/sd_journal_open_namespace.html).

**Describe alternatives you've considered**
N/A

**Additional context**
Journal 'namespaces' are both a mechanism for logically isolating the log stream of projects consisting of one or more services from the rest of the system and a mechanism for improving performance. Multiple journal namespaces may exist simultaneously, each defining its own, independent log stream managed by its own instance of systemd-journald.

https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html#Journal%20Namespaces

I've tried using `Path` option, specified to `/var/log/journal/<machine-id>.<namespace>`, it did work (with root privilege or in systemd-journal group), but it will be nice to have `Namespace` option.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6315162a8d4b1ef42b038834e639697f8cb44912`.  There
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
{"case_id": "fluent_fluent_bit__11156__6315162",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
