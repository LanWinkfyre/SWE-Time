# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
[3DS, possibly other systems] Trimming is not correctly recognized

### Paste the command

(from my .sh script)

eval "$IGIR $igir_command_options \
        --dat \"$dats_path\"/*.dat \
        --input \"$roms_path\" \
        move zip test clean report \
        --output \"$roms_path\"/{es} \
        --clean-backup \"$BACKUP_PATH\" \
        --input-checksum-max CRC32 \
        --input-checksum-archives never \
        --overwrite-invalid \
        --cache-path \"$CACHE_PATH\" \
        --report-output \"$log_file\""

### Describe the bug

I see that trimming recognition is built in now, but it does not work for any of my 3DS images (48 images tested). I checked one and noticed the padding was 0xFF (trimmed size 91,917,824 byte, full size 134,217,728 byte). The last few bytes in the checked rom were all 0x00 (contrary to the correct padding, so that's where the error may come from).

### Expected behavior

igir should try both, 0x00 and 0xFF to pad to the next power of 2, and use both checksums for checking.

### Debug logs

As this is somewhat of a followup-bug, and as I'm still struggling with the caching issue (#1596, meaning one complete run with my script takes hours), I'm taking the freedom of not providing this right away. Let me know if you really need it, I can add it at a later point.

### DAT(s) used

Nintendo - Nintendo 3DS (Decrypted) (20250803-001242).dat

### igir version

4.1.2

### Node.js version

22.17.0

### Operating system

Linux Mint

### Additional context

On another note and also completely unrelated here, the *file extension* is very important for 3DS dumps. Alhazar uses .CCI and nothing else, while the dat has all .3DS. I think there is already some command line option for that (i.e. keeping the original extension) buried inside igir, but I'm not completely sure.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f8d9f332547f16fdb33e752539eb9a73e6b5f05b`.  There
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
{"case_id": "emmercm_igir__1800__f8d9f33",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
