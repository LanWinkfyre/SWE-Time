# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
--overwrite doesn't overwrite broken symlinks

### Paste the command

```
igir link test --symlink --overwrite --dat=$DAT_PATH/ --input=$BACKUPS/OSCR/ --output=$HOME/ROMs/{es}/
```

### Describe the bug

I had a few bad dumps that were symlinked into my `ROMs` folder without DAT verification. I deleted the source file, placing the symlinks in a broken state. I redumped the games, placing the new dumps in a different location than the originals. I ran the above command and received errors. The broken symlinks were left behind.

### Expected behavior

I expected the broken symlinks to be removed and replaced with ones pointing to the files matched by `igir`.

### Debug logs

```
[14:41:28.587] INFO:  CandidateWriter: Nintendo - Nintendo Entertainment System (Headered): Ninja Gaiden (USA): creating symlink '/Users/dirn/Backups/OSCR/nes/Ninja Gaiden (USA).nes' →
'/Users/dirn/ROMs/nes/Ninja Gaiden (USA).nes'
[14:41:28.588] ERROR: CandidateWriter: Nintendo - Nintendo Entertainment System (Headered): Ninja Gaiden (USA): /Users/dirn/ROMs/nes/Ninja Gaiden (USA).nes: failed to link from
/Users/dirn/Backups/OSCR/nes/Ninja Gaiden (USA).nes: EEXIST: file already exists, symlink '/Users/dirn/Backups/OSCR/nes/Ninja Gaiden (USA).nes' ->
'/Users/dirn/ROMs/nes/Ninja Gaiden (USA).nes'
```

### DAT(s) used

_No response_

### igir version

3.0.1

### Node.js version

N/A

### Operating system

macOS 15.2

### Additional context

I only receive the errors for games that have broken symlinks. If I manually remove those, new ones are created. And subsequent runs don't error.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2ab09d3a25125a3c32d27a94083e846acc3fb9db`.  There
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
{"case_id": "emmercm_igir__1406__2ab09d3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
