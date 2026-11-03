# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
>4GB torrentzips fail to validate during clean

### Paste the command

```
npx --yes igir@latest move zip clean -v --dat "/Users/pcm/Downloads/nointro/*.zip" --dat-name-regex-exclude "/encrypted|source code/i" --input-checksum-archives never --input-checksum-max CRC32 --overwrite-invalid --dat-threads 4 --reader-threads 4 --writer-threads 1 --no-bios --no-debug --single --prefer-language EN --prefer-region USA,WORLD,EUR,JPN --prefer-revision newer --prefer-retail --prefer-good --prefer-verified   --prefer-game-regex="Welcome Amiibo"   --filter-region="USA,WORLD,EUR"  --zip-exclude "*.{chd,iso}" --clean-backup /Users/pcm/Downloads/nointro/RECYCLE \
        --dat-name-regex "Nintendo - Nintendo 3DS \(Digital\) \(CDN\)" \
        --input "/Users/pcm/Downloads/nointro/Nintendo - Nintendo 3DS (Digital) (CDN)" \
        --output "/Users/pcm/Downloads/nointro/Nintendo - Nintendo 3DS (Digital) (CDN)"
```

### Describe the bug

igir gets stuck in a loop trying to fix large torrent zips. This seems to happen when zip is >4GB.

Which generates output:

```
INFO: Nintendo - Nintendo 3DS (Digital) (CDN): Xenoblade Chronicles 3D (USA) (New 3DS): creating zip archive '/Users/pcm/Downloads/nointro/Nintendo - Nintendo 3DS (Digital) (CDN)/Xenoblade Chronicles 3D (USA) (New 3DS).zip' with the entries:
INFO:   '00000000' (3.52GiB) → '00000000' (rewriting)
INFO:   '00000001' (1.85MiB) → '00000001' (rewriting)
INFO:   '00000002' (3.52GiB) → '00000002' (rewriting)
INFO:   'tmd.0' (4.60KiB) → 'tmd.0' (rewriting)
INFO:   'tmd.2080' (4.60KiB) → 'tmd.2080' (rewriting)
INFO: Nintendo - Nintendo 3DS (Digital) (CDN): Hatsune Miku - Project Mirai DX (USA): creating zip archive '/Users/pcm/Downloads/nointro/Nintendo - Nintendo 3DS (Digital) (CDN)/Hatsune Miku - Project Mirai DX (USA).zip' with the entries:
INFO:   '00000000' (2.17GiB) → '00000000' (rewriting)
INFO:   '00000001' (2.90MiB) → '00000001' (rewriting)
INFO:   '00000002' (2.17GiB) → '00000002' (rewriting)
INFO:   '00000003' (2.90MiB) → '00000003' (rewriting)
INFO:   'tmd.0' (4.60KiB) → 'tmd.0' (rewriting)
INFO:   'tmd.16' (4.60KiB) → 'tmd.16' (rewriting)
```

### Expected behavior

The clean command causes these two zips to be rewritten every time. But the zip should be correct after the first clean (or copy, even)

### Debug log

[igir_2026-06-22T20:20:45.log](https://github.com/user-attachments/files/29232318/igir_2026-06-22T20.20.45.log)

### DAT(s) used

Nintendo - Nintendo 3DS (Digital) (CDN) (20260306-063611)

### igir version

latest

### Node.js version

v26.3.0

### Operating system

MacOS 15.7.7 

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9e00ab2e0a5d3951b0f66b6d61ff143dbfcea269`.  There
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
{"case_id": "emmercm_igir__2326__9e00ab2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
