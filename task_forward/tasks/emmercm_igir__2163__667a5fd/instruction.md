# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Improperly Detected Rom in Zip Archive

### Paste the command

```bash
npx -y igir@latest \
  -vvv link test \
  --dat \
    'dats/Aftermarket/Nintendo - Game Boy Color (Aftermarket) (20260324-160000).dat' \
    'dats/No-Intro/Nintendo - Game Boy Color (20260324-160000).dat' \
    'dats/Source Code/Source Code - Nintendo - Game Boy Color (20250313-191959).dat' \
  --dat-name-regex '/^Nintendo.*Game Boy.*/i' \
  --input \
    'roms-unverified/Nintendo - Game Boy Color/Pokemon Pinball (USA, Australia) (Rumble Version) (SGB Enhanced) (GB Compatible).zip' \
  --input-exclude 'roms-unverified/*@(ube|ii)*' \
  --input-checksum-quick false \
  --input-checksum-min CRC32 \
  --input-checksum-max SHA256 \
  --output='roms/{romm}' \
  --prefer-language EN \
  --prefer-region USA,WORLD,EUR,AUS,JPN \
  --prefer-revision newer \
  --no-bios \
  --single \
  --overwrite-invalid \
  --cache-path=/home/wow/tmp/igir.cache \
  --temp-dir=/mnt/r/igir \
  --merge-roms merged
```

### Describe the bug

I feel I'm going a little crazy trying to understand why igir refuses process some pocket monster roms.


```bash
$ crc32 /mnt/g/roms-unverified/Nintendo\ -\ Game\ Boy\ Color/Pokemon\ Pinball\ \(USA*
3fe43f11        /mnt/g/roms-unverified/Nintendo - Game Boy Color/Pokemon Pinball (USA, Australia) (Rumble Version) (SGB Enhanced) (GB Compatible).zip
```

```bash
$ sha256sum /mnt/g/roms-unverified/Nintendo\ -\ Game\ Boy\ Color/Pokemon\ Pinball\ \(USA*
c9d203463f82bc8cdbf9df254e50a91b8162708695bc5b89efb90b3f23eb9d84  /mnt/g/roms-unverified/Nintendo - Game Boy Color/Pokemon Pinball (USA, Australia) (Rumble Version) (SGB Enhanced) (GB Compatible).zip
```

```bash
$ zipinfo -v /mnt/g/roms-unverified/**/*pokemon*pinball\ \(USA*
Archive:  /mnt/g/roms-unverified/Nintendo - Game Boy Color/Pokemon Pinball (USA, Australia) (Rumble Version) (SGB Enhanced) (GB Compatible).zip
The zipfile comment is 22 bytes long and contains the following text:
======================== zipfile comment begins ==========================
TORRENTZIPPED-0159328E
========================= zipfile comment ends ===========================

End-of-central-directory record:
-------------------------------

  Zip archive file size:                    315157 (000000000004CF15h)
  Actual end-cent-dir record offset:        315113 (000000000004CEE9h)
  Expected end-cent-dir record offset:      315113 (000000000004CEE9h)
  (based on the length of the central directory and its expected offset)

  This zipfile constitutes the sole disk of a single-part archive; its
  central directory contains 1 entry.
  The central directory is 130 (0000000000000082h) bytes long,
  and its (expected) offset in bytes from the beginning of the zipfile
  is 314983 (000000000004CE67h).


Central directory entry #1:
---------------------------

  Pokemon Pinball (USA, Australia) (Rumble Version) (SGB Enhanced) (GB Compatible).gbc

  offset of local header from start of archive:   0
                                                  (0000000000000000h) bytes
  file system or operating system of origin:      MS-DOS, OS/2 or NT FAT
  version of encoding software:                   0.0
  minimum file system compatibility required:     MS-DOS, OS/2 or NT FAT
  minimum software version required to extract:   2.0
  compression method:                             deflated
  compression sub-type (deflation):               maximum
  file security status:                           not encrypted
  extended local header:                          no
  file last modified on (DOS date/time):          1996 Dec 24 23:32:00
  32-bit CRC value (hex):                         03ce8d9a
  compressed size:                                314869 bytes
  uncompressed size:                              1048576 bytes
  length of filename:                             84 characters
  length of extra field:                          0 bytes
  length of file comment:                         0 characters
  disk number on which file begins:               disk 1
  apparent file type:                             binary
  non-MSDOS external file attributes:             000000 hex
  MS-DOS file attributes (00 hex):                none

  There is no file comment
```

### Expected behavior

This is what I expected things to match against: https://datomatic.no-intro.org/index.php?page=show_record&s=47&n=0926

But it absolutely doesn't unless I explicitly extract the `.gbc` file first.

I'm not a node developer. Any pointers would be much appreciated.

### Debug log

[igir.debug.log](https://github.com/user-attachments/files/26619682/igir.debug.log)

### DAT(s) used

_No response_

### igir version

v4.3.2

### Node.js version

v20.20.0

### Operating system

Ubuntu 24.04.04 **(WSL)**

### Additional context

That said, thanks for all your hard work on Igir. It is a delight to use.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `667a5fdad0ebdfe3cea3399f68c549ac08cf5cf3`.  There
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
{"case_id": "emmercm_igir__2163__667a5fd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
