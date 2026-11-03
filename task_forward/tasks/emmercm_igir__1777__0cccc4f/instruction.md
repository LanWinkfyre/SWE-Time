# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
WARN: <chd_path>: found no files in path

### Paste the command

```
igir report --dat /dev/shm/mame.xml --input ~/mame/roms --input-checksum-quick --merge-roms merged
```

using the XML file as input generated from ```mame -listxml``` in version 0.278.

### Describe the bug

I'm seeing this warning for a fair number of my CHD's:

```
WARN: <chd_path>: found no files in path
```

It looks to be around 405 of them in total (about half of the CHD's I have).

### Expected behavior

I'm not even clear on what the warning is trying to say.  As far as I know, these are all good CHD images as clrmame has always verified successfully.  Note that this is happening during the initial ROM scan, and not during the ROM trimming detection I just opened a separate issue about.

I thought it might be related to CHD version or some such, but it seems to indicate the same warning for both version 4 and 5 CHD files, so that isn't the common factor.

### Debug logs

Right from the top:

```
[14:32:37.257] TRACE: ROMScanner: scanning ROM files
[14:32:37.396] TRACE: ROMScanner: found 16,229 ROM files
[14:32:40.606] WARN: ROMScanner: /home/nipsy/mame/roms/atronic/atronic.chd: found no files in path
```

There is no additional output beyond the warning.

### DAT(s) used

_No response_

### igir version

4.1.1

### Node.js version

22.17.0

### Operating system

NixOS

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0cccc4f87ee047f16bb36103ddf8a816219dc8db`.  There
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
{"case_id": "emmercm_igir__1777__0cccc4f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
