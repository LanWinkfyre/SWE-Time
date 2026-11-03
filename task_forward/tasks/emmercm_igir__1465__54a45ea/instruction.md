# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Multiple DAT URLs results in "1 DAT found"

### Paste the command

```
npx --yes igir@latest link clean report \
  --dat "https://github.com/frederic-mahe/Hardware-Target-Game-Database/raw/refs/heads/master/EverDrive%20Pack%20SMDBs/EverDrive%20N8%20&%20PowerPak%20SMDB.txt" "https://github.com/frederic-mahe/Hardware-Target-Game-Database/raw/refs/heads/master/EverDrive%20Pack%20SMDBs/Famicom%20Disk%20System%20SMDB.txt" "https://raw.githubusercontent.com/frederic-mahe/Hardware-Target-Game-Database/refs/heads/master/EverDrive%20Pack%20SMDBs/NES2.0%20SMDB.txt" "https://github.com/frederic-mahe/Hardware-Target-Game-Database/raw/refs/heads/master/EverDrive%20Pack%20SMDBs/NSF%20Music%20SMDB.txt" \
  --input "./[ROM-LOCATION]/*{Family Computer,Nintendo Entertainment System}*/**/*" \
  --output "../ROMs-Shared/htgdb/{mister}/" \
  --report-output "../ROMs-Shared/igir-reports/igir_%YYYY-%MM-%DDT%HH:%mm:%ss.csv" \
  --reader-threads 4 \
  -vvv
```

### Describe the bug

In the above command, 4 URLs to SMDB files are provided to the `--dat` parameter. Igir should download and process all four DAT files. In stead, it only uses the first DAT file that is proided.

### Expected behavior

For every `n` DAT (or in this case SMDB) URLs, find and process `n` DAT files.

### Debug logs

```
[12:17:01.273] TRACE: DATScanner: scanning DAT files                                                
[12:17:01.314] TRACE: DATScanner: found 4 DAT files                                                 
[12:17:01.315] TRACE: DATScanner: enumerating DAT archives                                          
[12:17:01.347] TRACE: DATScanner: downloading DATs from URLs                                        
[12:17:01.348] TRACE: DATScanner:                                                                   
https://github.com/frederic-mahe/Hardware-Target-Game-Database/raw/refs/heads/master/EverDrive%20Pa:
 downloading
[12:17:03.265] TRACE: DATScanner: 
https://github.com/frederic-mahe/Hardware-Target-Game-Database/raw/refs/heads/master/EverDrive%20Pa:
 downloaded to '/tmp/igir/20250302-121657/dat.ogzl5m'
[12:17:03.277] TRACE: DATScanner: parsing 1 DAT file
[12:17:03.285] TRACE: DATScanner: /tmp/igir/20250302-121657/dat.ogzl5m: attempting to parse 3.2MB of
 XML
[12:17:03.620] TRACE: DATScanner: /tmp/igir/20250302-121657/dat.ogzl5m: parsed XML, deserializing to
 DAT
[12:17:03.620] TRACE: DATScanner: /tmp/igir/20250302-121657/dat.ogzl5m: parsed XML, but failed to 
find a known DAT root
[12:17:03.624] TRACE: DATScanner: /tmp/igir/20250302-121657/dat.ogzl5m: attempting to parse SMDB
[12:17:03.857] TRACE: DATScanner: /tmp/igir/20250302-121657/dat.ogzl5m: parsed SMDB, deserializing 
to DAT
[12:17:03.889] TRACE: DATScanner: /tmp/igir/20250302-121657/dat.ogzl5m: NaNundefined of 13,816 
games, 13,815 parents parsed
[12:17:03.921] TRACE: DATScanner: done scanning DAT files
✓ Scanning for DATs ··············· | 1 DAT found
```

### DAT(s) used

_No response_

### igir version

3.02

### Node.js version

v22.13.1

### Operating system

Almalinux 9.5

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `54a45ea73d5d64e978d9fee4c97f32c72812bbc8`.  There
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
{"case_id": "emmercm_igir__1465__54a45ea",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
