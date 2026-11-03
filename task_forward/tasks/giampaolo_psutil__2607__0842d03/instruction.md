# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Windows] can't query some services' description

## Summary

- OS: Windows
- Type: core

## Description

Observed in CI:
```
2025-08-05T14:22:41.4307406Z Traceback (most recent call last):
2025-08-05T14:22:41.4317939Z   File "C:\a\psutil\psutil\scripts\winservices.py", line 63, in <module>
2025-08-05T14:22:41.4318375Z     sys.exit(main())
2025-08-05T14:22:41.4318685Z   File "C:\a\psutil\psutil\scripts\winservices.py", line 49, in main
2025-08-05T14:22:41.4318971Z     info = service.as_dict()
2025-08-05T14:22:41.4319509Z   File "C:\Users\runneradmin\AppData\Local\Temp\cibw-run-dd0tjgcx\cp310-win_arm64\venv-test\lib\site-packages\psutil\_pswindows.py", line 615, in as_dict
2025-08-05T14:22:41.4320060Z     d['description'] = self.description()
2025-08-05T14:22:41.4320641Z   File "C:\Users\runneradmin\AppData\Local\Temp\cibw-run-dd0tjgcx\cp310-win_arm64\venv-test\lib\site-packages\psutil\_pswindows.py", line 603, in description
2025-08-05T14:22:41.4321220Z     return cext.winservice_query_descr(self.name())
2025-08-05T14:22:41.4321590Z OSError: [WinError 1168] Element not found: '(originated from QueryServiceConfig2W)'
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0842d0350210d45df9410870b7622da1ab60c0e5`.  There
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
{"case_id": "giampaolo_psutil__2607__0842d03",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
