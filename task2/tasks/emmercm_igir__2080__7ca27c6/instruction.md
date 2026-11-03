# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
With "move": Remove matches in input folders if they already exist in the output folder

### Is your feature request related to a problem?

Yes, because I'd like to keep my storage tidy, and I'd like matched files to be removed from my add folders.

The problem is the follwing:
Assume we have a matched game in the output folder, let's just call it "My Game (USA)". Assume the exact same game - "My Game (USA)" is also in one of the input folders. Now, when I process my folders using "move", both copies of the file (in the output and the input folder) stay.

### Describe the solution you'd like

In the described scenario, I would have expected the copy from the input folder to be automatically deleted. The file is is a duplicate, and I instructed igir to "move". Also, I somewhat remember that was the default handling in igir a few versions ago, possibly?

By the way: I can add "--overwrite" to the command line parameters. That, in conjunction with "move", makes sure I end up with only one copy, as I wanted it. But, I don't know what exactly "--overwrite" does (what will it do with multi-file arcade roms?), and at the very least it would mean unneccessary writing to the file system (I don't need to overwrite a file with an identical copy, right?).

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7ca27c6ef07d9fcd830c28cef5630d7f3b0498a1`.  There
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
{"case_id": "emmercm_igir__2080__7ca27c6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
