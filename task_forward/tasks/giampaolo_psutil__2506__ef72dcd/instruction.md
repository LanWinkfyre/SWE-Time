# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Windows] PSUTIL service lookup having unicode issue with special characters - (Č) to be specific

## Summary

* OS: Windows Server
* Architecture: x86
* Psutil version: 6.1.1
* Python version: 3.6.8
* Type: core

## Description

From Nagios NCPA.

There is apparent Unicode issue with the service status check for psutil.

Service names that have a non-standard UTF character will fail a lookup in service status:

```
File "psutil_pswindows.py", line 628, in status
File "psutil_pswindows.py", line 558, in _query_status
File "contextlib.py", line 158, in exit
File "psutil_pswindows.py", line 583, in _wrap_exceptions
psutil.NoSuchProcess: service 'ČSOB Business Connector' does not exist (name='ČSOB Business Connector')
```
I note that PSUTIL in the service iteration is doing a Unicode conversion.

```PyUnicode_FromWideChar(*)```

But...when looking up a specific service, it's not doing the transverse, which may be what causes this problem

```python
    def description(self):
        """Service long description."""
        return cext.winservice_query_descr(self.name())
```

AKA, converting self.name() via PyUnicode_AsWideChar(*) back to wchar format.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ef72dcd076f1cec94ba50ec30b5dbebb272845d0`.  There
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
{"case_id": "giampaolo_psutil__2506__ef72dcd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
