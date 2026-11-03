# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Linux] cpu_freq() fallback is wrong on ppc and s390x

`_cpu_get_cpuinfo_freq()` matches lines starting with `"cpu MHz"`, which is fine on x86. 
`ppc` archs reports this as `"clock"` and not `"cpu MHz"`, so we return nothing. 

```
$ python3 -c "import psutil; print(psutil.cpu_freq())"
None
$ grep -m1 clock /proc/cpuinfo
clock         : 2750.000000MHz
```

Also s390x archs prints two lines per CPU (source):

```
"cpu MHz dynamic : %d\n"
"cpu MHz static  : %d\n"
```

...so the returned values are wrong (double counted).

Related:
- #2750
- #2557 
- #1197
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5e68c49180724d070d04f8455c9eb8378c0ced75`.  There
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
{"case_id": "giampaolo_psutil__2967__5e68c49",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
