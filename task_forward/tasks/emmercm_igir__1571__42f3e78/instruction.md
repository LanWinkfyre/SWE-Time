# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Handling trimmed rom dumps

### Is your feature request related to a problem?

Yes, I can't handle my (trimmed) 3DS dumps with igir. 

### Describe the solution you'd like

I'd like igir to handle trimmed rom dumps, as are common for 3DS emulators. This can either be done by content (when a 3DS file is found, also check the untrimmed size), or (this may be better) via a new command line parameter. Further description below.

### Additional context

None of the known working 3DS emulators nowadays accept any way of (additional) compression (not even ZIP) for compatible rom dumps, trimming is the only way to save some storage space. However, checking these files via datfiles is not possible, as we'd need the missing data to calculate the correct checksum.

Properly checking trimmed dumps, in theory is easy. Just use the data from the rom dump (minus any additional headers, but those don't apply to typical trimmed formats anyway), and then pretend there are zeroes until a full size of a power of 2 is reached. This will lead to additional processing time (we can't use the checksum stored in a ZIP, for example, and will need to unzip and process), so either this should be only done for known candidates (.gba, .nds, .3ds, .cci, ...), or - via a new command line parameter - for all files, but the user should be made aware that this is better only done where needed (ie. in a separate igir run).

By the way: hope I'm not flooding you with those. I'm only having that many ideas because I really, really like your work.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `42f3e787facf13badd5750e13aab869b5c9c2f93`.  There
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
{"case_id": "emmercm_igir__1571__42f3e78",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
