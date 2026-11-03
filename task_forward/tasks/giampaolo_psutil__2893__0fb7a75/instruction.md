# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
Drop Windows Vista, 7, 8, 8.1 and Windows Server 2008, 2012. New minimum: Windows 10 / Server 2016

psutil currently supports Windows Vista+. I propose raising the minimum to Windows 10 / Windows Server 2016.

## Numbers

PyPI download stats for the last 30 days (BigQuery), Windows only:

| release                | downloads | %     |
|------------------------|-----------|-------|
| 10 / 11 / Server 2016+ | ~13.56M   | 99.66 |
| 7 (+ 2008 R2)          | 21,885    | 0.16  |
| 8.1 (+ 2012 R2)        | 15,072    | 0.11  |
| 8 (+ 2012)             | 1,345     | 0.01  |
| Vista (+ 2008)         | 190       | 0.001 |

(determined via https://github.com/giampaolo/psutil/blob/ci-speedup/scripts/internal/print_downloads.py script).

Everything below Windows 10 combined is 0.34% of Windows traffic, which is ~0.01% of all psutil downloads. Of those, ~72% are pinned to a psutil version, so they are unaffected by anything we do. 

Also, CPython 3.9 already dropped everything below Windows 8.1, so old Windows can only run the latest psutil via Python 3.8. If / when we drop 3.8, this floor becomes self-enforcing through wheel tags.

## Versions

Dropped desktop versions:
- Windows Vista (NT 
- Windows 7 
- Windows 8 
- Windows 8.1 

Dropped server versions:
- Windows Server 2008 (NT 6.0)
- Windows Server 2008 R2 (NT 6.1)
- Windows Server 2012 (NT 6.2)
- Windows Server 2012 R2 (NT 6.3)

New floor:

- Windows 10
- Windows 11
- Windows Server 2016, 2019, 2022, 2025, including Nano Server (which psutil explicitly supports)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0fb7a75a3d01e115c0d1f0c69beaae2545c9ba7c`.  There
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
{"case_id": "giampaolo_psutil__2893__0fb7a75",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
