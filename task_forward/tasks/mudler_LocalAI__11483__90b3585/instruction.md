# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
WarmEstimateCache fetches > 1 GB every start

**LocalAI version:**
4.8.2 (a633fae08dc3a1f0cdf75235b1a44be098235f52)

**Environment, CPU architecture, OS, and Version:**
Linux 7.1.8-arch1-3 #1 SMP PREEMPT_DYNAMIC Tue, 11 Aug 2026 09:16:08 +0000 x86_64 GNU/Linux

**Describe the bug**
When I start LocalAI, it downloads over a gigabyte of model gallery data/configs to support fast VRAM estimation. It does this every time the service is started, so if there's any caching supposed to happen here, it's not working. It also doesn't look like I can disable this behavior via config. As more models are added, this amount will keep increasing.

I was able to workaround this by only enabling my own custom galleries or disabling galleries entirely.

**To Reproduce**
Start a `local-ai run` service with default gallery config.

**Expected behavior**
LocalAI should cache the gallery data it downloads as best it can whenever possible.

**Logs**
I observed this when the download finished:

```
Aug 12 13:02:25 INFO  gallery caches warmed estimates=299 variants=52 of=300 took=3m4s
```

Yes, my internet connection is pretty slow. LocalAI fully saturates it for just over 3 minutes and I have several instances and restart then a lot for testing. If I remove the built-in model and backend galleries this takes only a few seconds.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `90b35850801e0a26ec29f57ad93d92fa7d7c81b2`.  There
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
{"case_id": "mudler_LocalAI__11483__90b3585",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
