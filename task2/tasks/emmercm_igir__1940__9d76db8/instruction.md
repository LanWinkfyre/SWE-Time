# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Add CLI option to disable detecting trimmed roms

### Is your feature request related to a problem?

Whenever I process new dumps for IBM PC, I get an additional two and a half minutes of waiting because igir tries to check if all the cuefiles are trimmed. I can guarantee that they aren't, so there's no need for this. Is there any option to disable detecting rom trimming? I only see an option to disable it in archives, where it's already disabled by default anyways.

If also worth noting- even when reusing the same cache, igir still also takes a built in 2 and a half minutes to re-scan all of the cuefiles. Not sure if I'm doing something wrong, or if there's just nothing I can do about that.

### Describe the solution you'd like

A commandline option to disable detection of rom trimming.

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9d76db816100f028b018f5637f01ec670c52b6ea`.  There
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
{"case_id": "emmercm_igir__1940__9d76db8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
