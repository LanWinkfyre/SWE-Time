# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[SunOS] drop SunOS 10 support

SunOS 10 (Solaris 10) is no longer actively maintained by Oracle:

* Solaris 10 was released in January 2005.
* Premier Support ended on January 2018.
* Extended Support ended on January 2023.
* After Jan 2023, the only option is Oracle’s “Sustaining Support,” which provides no new patches, no security updates, and no new certifications — just access to old fixes and documentation.

In practice, this means Solaris 10 has been fully out of regular support for over two years, and is not receiving security updates or maintenance, so let's just drop it.

Here's the relevant commits which were done in order to add support for it:

* 69a4efef (CC @wiggin15)
* #1077 (CC @alxchk)
* #1081
* https://github.com/giampaolo/psutil/pull/1491 (CC @qcha0)
* https://github.com/giampaolo/psutil/issues/421
* https://github.com/giampaolo/psutil/issues/1637
* https://github.com/giampaolo/psutil/pull/1638 (CC @vser1)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8aca550dd16ec6b78d0160471bda4d24fe7e4d21`.  There
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
{"case_id": "giampaolo_psutil__2645__8aca550",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
