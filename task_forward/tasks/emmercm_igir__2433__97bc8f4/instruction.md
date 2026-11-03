# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Wrong report and log filename generated

### Paste the command

bunx igir@latest \
    copy \
    zip \
    test \
    report \
    --cache-path "${IGIR_CACHE_PWD}" \
    --dat "${DATS_PWD}" \
    --input "${SETS_PWD}" \
    --input "${NEWS_PWD}" \
    --input-checksum-max CRC32 \
    --input-checksum-archives never \
    --output "${SETS_PWD}" \
    --fix-extension always \
    --overwrite-invalid \
    --dir-dat-mirror \
    --merge-roms split \
    --debug-log

### Describe the bug

Wrong report / log filename generated / created, filename contains ; characters

> ✓ MAME » 4,783/5,291 games, 4,468/4,962 retail releases written
> ✓ Generating report » igir_2026-08-20T23;25;16.csv
> igir_2026-08-20T23;19;48.log

### Expected behavior

As state the --help: `[default: "igir_%YYYY-%MM-%DDT%HH:%mm:%ss.csv"]`

### Debug log

[igir_2026-08-20T23;19;48.tar.gz](https://github.com/user-attachments/files/31282191/igir_2026-08-20T23.19.48.tar.gz)
[MAME 0.37b5.xml](https://github.com/user-attachments/files/31282362/MAME.0.37b5.xml)
[mame2003-plus.xml](https://github.com/user-attachments/files/31282374/mame2003-plus.xml)

### DAT(s) used

_No response_

### Additional context

As you would notice in the attached log file, there are plenty of false positive errors, so many that i don't know how to report them to you:

- The log is hard to read, both MAME dat files reporting name 'MAME' it's really difficult to understand which one it speak about every time
- **[23:19:57.863] TRACE: CandidateGenerator: MAME: arkatour: found 5 files, missing 1 file:**
- Would be much easier if the dat file name would be used instead.

- Input archives contains all needed roms, but they are somehow rejected
- Created torrent zip files from igir are then told invalid and igir keep trying to recreate them everytime i start it

I would be happy to discuss this more with you if you want, jsut ask info.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `97bc8f40f6176a316e3ec942ccff282932e179ee`.  There
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
{"case_id": "emmercm_igir__2433__97bc8f4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
