# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Minor Cache Improvement - Cache the checksum info of ROMs in the output directory

### Is your feature request related to a problem?

Short answer: Yes.

Long answer:
A lot of the script setups I've seen and even what's suggested in the Maintainers Usage part of the guide, typically uses multiple calls to igir. First, it will incorporate any new ROMs into a "sorted / archival" collection, then it will copy subsets of the ROMs to various other locations (SD cards, external drives, etc.). My current setup is similar to this and its what a lot of users will go through as part of their first time setting up. This can be a pretty long process depending on how many ROMs are in the collection. I've had it take days when dealing with lots of games and large wii files.

### Describe the solution you'd like

Something that is intended to help speed up subsequent calls to igir, is the **cache!** So given that igir saves all the metadata of those difficult to checksum ROMs in the cache, it would make perfect sense if it would save that data for the output directory as well. Now immediately after creating your "sorted / archive" folder, you'll get quick speeds copying over subsets of the collection.

Now perhaps this already how its intended to work, in that case we can discuss something similar to #1593 where this may be a bug instead of an enhancement.

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7abf26a9c2ac7a04ce946af2c24d47709618d333`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "emmercm_igir__1808__7abf26a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
