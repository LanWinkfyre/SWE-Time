# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Certain TorrentZip files failing to validate during clean

### Paste the command

```
./igir move zip test clean report --dat C:\DATs\No-Intro --input C:\ROMs-New --input C:\ROMs\No-Intro --output C:\ROMs\No-Intro --dir-dat-name --overwrite-invalid
```

### Describe the bug

I was using v5.0.2 until recently when I upgraded to the latest v5.4.0. I saw the note about issue #2326 so I added `--overwrite-invalid` to the command I was running igir with. Now I am seeing that some files are being rewritten every time, similar to the aforementioned issue. The output files seem to be correctly TorrentZipped so I'm not sure why these particular archives fail to verify. The affected archives are not over 4 GB in size, but they do contain more files than their peers.

So far I have noticed this occurring with the following DAT files:

- Nintendo - Nintendo DS (Download Play)
- Nintendo - Game Boy Advance (e-Reader)

Here is the output during a test run against the first set:

```
   @@@@@@   @@@@@@     @@@@@@    @@@@@@@@
 @@      @@  @@      @@      @@         @@
 @@      @@  @@      @@      @@         @@   ROM collection manager
   @@@@@@   @@         @@@@@@   @@@@@@@@@    https://igir.io/
          @@@     @@@@        @@@
     @@   @@        @@   @@   @@       @@    v5.4.0 (Bun v1.3.14)
     @@   @@        @@   @@   @@       @@
     @@   @@@@@@@@@@@@   @@   @@       @@

NOTICE: Writing debug log to: igir_2026-07-29T18;00;06.log
WARN: --dir-dat-name is most helpful when processing multiple DATs, only one DAT was found

 ✓ Parsing DATs » 1 DAT found
 ✓ Scanning for ROMs » 1,557 files found

WARN: Nintendo - Nintendo DS (Download Play): Mystery Case Files - MillionHeir (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Mystery Case Files - MillionHeir (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Rhythm Heaven (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Rhythm Heaven (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Pokemon Ranger - Guardian Signs (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Pokemon Ranger - Guardian Signs (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Mystery Case Files - MillionHeir (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Mystery Case Files - MillionHeir (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Rhythm Heaven (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Rhythm Heaven (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Pokemon Ranger - Guardian Signs (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Pokemon Ranger - Guardian Signs (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file, retrying
ERROR: Nintendo - Nintendo DS (Download Play): Mystery Case Files - MillionHeir (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Mystery Case Files - MillionHeir (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file
ERROR: Nintendo - Nintendo DS (Download Play): Rhythm Heaven (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Rhythm Heaven (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file
ERROR: Nintendo - Nintendo DS (Download Play): Pokemon Ranger - Guardian Signs (USA, Europe, Australia) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Pokemon Ranger - Guardian Signs (USA, Europe, Australia) (Demo).zip: written zip is not a valid TorrentZip file
WARN: Nintendo - Nintendo DS (Download Play): Art Academy - Demo Lesson (Europe, Australia) (En,Fr,De,Es,It) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Art Academy - Demo Lesson (Europe, Australia) (En,Fr,De,Es,It) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Cooking Mama World - Hobbies & Fun (Europe, Australia) (En,Fr,De,Es,It) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Cooking Mama World - Hobbies & Fun (Europe, Australia) (En,Fr,De,Es,It) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Art Academy - Demo Lesson (Europe, Australia) (En,Fr,De,Es,It) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Art Academy - Demo Lesson (Europe, Australia) (En,Fr,De,Es,It) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Cooking Mama World - Outdoor Adventures - Trial Version (Europe, Australia) (En,Fr,De,Es,It) (Rev 1) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Cooking Mama World - Outdoor Adventures - Trial Version (Europe, Australia) (En,Fr,De,Es,It) (Rev 1) (Demo).zip: written zip is not a valid TorrentZip file, retrying
ERROR: Nintendo - Nintendo DS (Download Play): Art Academy - Demo Lesson (Europe, Australia) (En,Fr,De,Es,It) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Art Academy - Demo Lesson (Europe, Australia) (En,Fr,De,Es,It) (Demo).zip: written zip is not a valid TorrentZip file
WARN: Nintendo - Nintendo DS (Download Play): Cooking Mama World - Hobbies & Fun (Europe, Australia) (En,Fr,De,Es,It) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Cooking Mama World - Hobbies & Fun (Europe, Australia) (En,Fr,De,Es,It) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Cooking Mama World - Outdoor Adventures - Trial Version (Europe, Australia) (En,Fr,De,Es,It) (Rev 1) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Cooking Mama World - Outdoor Adventures - Trial Version (Europe, Australia) (En,Fr,De,Es,It) (Rev 1) (Demo).zip: written zip is not a valid TorrentZip file, retrying
ERROR: Nintendo - Nintendo DS (Download Play): Cooking Mama World - Hobbies & Fun (Europe, Australia) (En,Fr,De,Es,It) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Cooking Mama World - Hobbies & Fun (Europe, Australia) (En,Fr,De,Es,It) (Demo).zip: written zip is not a valid TorrentZip file
ERROR: Nintendo - Nintendo DS (Download Play): Cooking Mama World - Outdoor Adventures - Trial Version (Europe, Australia) (En,Fr,De,Es,It) (Rev 1) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Cooking Mama World - Outdoor Adventures - Trial Version (Europe, Australia) (En,Fr,De,Es,It) (Rev 1) (Demo).zip: written zip is not a valid TorrentZip file
WARN: Nintendo - Nintendo DS (Download Play): Imagine - Teacher - School Trip (Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Imagine - Teacher - School Trip (Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Dr Kawashima's Brain Training - How Old Is Your Brain - Quick Play (USA, Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo) (Nintendo Channel): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Dr Kawashima's Brain Training - How Old Is Your Brain - Quick Play (USA, Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo) (Nintendo Channel).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Imagine - Teacher - School Trip (Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Imagine - Teacher - School Trip (Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo).zip: written zip is not a valid TorrentZip file, retrying
WARN: Nintendo - Nintendo DS (Download Play): Dr Kawashima's Brain Training - How Old Is Your Brain - Quick Play (USA, Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo) (Nintendo Channel): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Dr Kawashima's Brain Training - How Old Is Your Brain - Quick Play (USA, Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo) (Nintendo Channel).zip: written zip is not a valid TorrentZip file, retrying
ERROR: Nintendo - Nintendo DS (Download Play): Imagine - Teacher - School Trip (Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Imagine - Teacher - School Trip (Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo).zip: written zip is not a valid TorrentZip file
ERROR: Nintendo - Nintendo DS (Download Play): Dr Kawashima's Brain Training - How Old Is Your Brain - Quick Play (USA, Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo) (Nintendo Channel): C:\ROMs\No-Intro\Nintendo - Nintendo DS (Download Play)\Dr Kawashima's Brain Training - How Old Is Your Brain - Quick Play (USA, Europe, Australia) (En,Fr,De,Es,It,Nl) (Demo) (Nintendo Channel).zip: written zip is not a valid TorrentZip file

 ✓ Nintendo - Nintendo DS (Download Play) » 699/699 games, 228/228 retail releases written
 ✓ Cleaning output directory » 0 files recycled
 ✓ Generating report » igir_2026-07-29T18;00;23.csv
```

### Expected behavior

No errors or warnings during verification since the input files were created by igir itself.

### Debug log

[igir_2026-07-29T18;00;06.log](https://github.com/user-attachments/files/30525461/igir_2026-07-29T18.00.06.log)

### DAT(s) used

_No response_

### Additional context

Possibly related to issue #2326 and the changes made in v5.2.1.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a714680694f41a9a7355fd177d6d0ec02f2ce5b3`.  There
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
{"case_id": "emmercm_igir__2411__a714680",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
