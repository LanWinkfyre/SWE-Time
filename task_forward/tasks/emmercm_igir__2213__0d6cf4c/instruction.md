# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
multiple games writing to the same output path

### Paste the command

npx igir@latest move --input "/in/pcengine" --output "/out/pcengine" --input checksum-archives never --input checksum-quick

### Describe the bug

When using igir to copy or move .chd files from one folder to another without a dat, igir errors out with a handful of "multiple games writing to the same output path" errors. 

> ERROR: NEC - PC Engine CD: multiple games writing to the same output path: /out/pcengine CD/J. B.chd
ERROR:   J. B. Harold Murder Club (USA) (En,Ja)
ERROR:   J. B. Harold Series 1 - Murder Club (Japan)
ERROR: NEC - PC Engine CD: multiple games writing to the same output path: /out/pcengine CD/Laser Soft Visual Collection Vol.chd
ERROR:   Laser Soft Visual Collection Vol. 1 - Cosmic Fantasy Visual-shuu (Japan)
ERROR:   Laser Soft Visual Collection Vol. 2 - Valis Visual-shuu (Japan)
ERROR: NEC - PC Engine CD: multiple games writing to the same output path: /out/pcengine CD/Psychic Detective Series Vol.chd
ERROR:   Psychic Detective Series Vol. 3 - Aya (Japan)
ERROR:   Psychic Detective Series Vol. 4 - Orgel (Japan)
ERROR:   Psychic Detective Series Vol. 3 - Aya (Japan) (Demo)
ERROR: NEC - PC Engine CD: multiple games writing to the same output path: /out/pcengine CD/Top o Nerae! GunBuster Vol.chd
ERROR:   Top o Nerae! GunBuster Vol. 1 (Japan)
ERROR:   Top o Nerae! GunBuster Vol. 2 (Japan)
ERROR: NEC - PC Engine CD: multiple games writing to the same output path: /out/pcengine CD/Bishoujo Senshi Sailor Moon (Japan) [T-En by Supper & TheMajinZenki v1.chd
ERROR:   Bishoujo Senshi Sailor Moon (Japan) [T-En by Supper & TheMajinZenki v1.1] [Honorifics]
ERROR:   Bishoujo Senshi Sailor Moon (Japan) [T-En by Supper & TheMajinZenki v1.1]
ERROR: NEC - PC Engine CD: multiple games writing to the same output path: /out/pcengine CD/Castlevania - Rondo of Blood (Japan) [T-En by Burnt Lasagna & Cubanraul v1.chd
ERROR:   Castlevania - Rondo of Blood (Japan) [T-En by Burnt Lasagna & Cubanraul v1.01] [n]
ERROR:   Castlevania - Rondo of Blood (Japan) [T-En by Burnt Lasagna & Cubanraul v1.03] [n]
ERROR: NEC - PC Engine CD: multiple games writing to the same output path: /out/pcengine CD/Tengai Makyou - Ziria (Japan) (Rev 7) (En) (v1.chd
ERROR:   Tengai Makyou - Ziria (Japan) (Rev 7) (En) (v1.0) (LIPEMCO! Translations)
ERROR:   Tengai Makyou - Ziria (Japan) (Rev 7) (En) (v1.2) (LIPEMCO! Translations)

There seems to be some issue with .chd files having periods in their file name. Here is another set of games from the 3DO:

> ERROR: Panasonic - 3DO: multiple games writing to the same output path: /out/3DO/Emit Vol.chd
ERROR:   Emit Vol. 1 - Toki no Maigo (Japan)
ERROR:   Emit Vol. 2 - Inochigake no Tabi (Japan)
ERROR:   Emit Vol. 3 - Watashi ni Sayonara o (Japan)
ERROR: Panasonic - 3DO: multiple games writing to the same output path: /out/3DO/Grimm Meisaku Gekijou Vol.chd
ERROR:   Grimm Meisaku Gekijou Vol. 1 - Bremen no Ongakutai (Japan)
ERROR:   Grimm Meisaku Gekijou Vol. 2 - Hansel to Gretel (Japan)
ERROR:   Grimm Meisaku Gekijou Vol. 3 - Akazukin (Japan)
ERROR: Panasonic - 3DO: multiple games writing to the same output path: /out/3DO/J. B.chd
ERROR:   J. B. Harold - Blue Chicago Blues (Japan) (Disc 1)
ERROR:   J. B. Harold - Blue Chicago Blues (Japan) (Disc 2)
ERROR: Panasonic - 3DO: multiple games writing to the same output path: /out/3DO/J.chd
ERROR:   J.League Virtual Stadium '95 (Japan)
ERROR:   J.League Virtual Stadium (Japan)
ERROR: Panasonic - 3DO: multiple games writing to the same output path: /out/3DO/Doctor Hauzer (Japan) [T-En by ArcaneAria v1.2.chd
ERROR:   Doctor Hauzer (Japan) [T-En by ArcaneAria v1.2.1] [Custom Music Edition]
ERROR:   Doctor Hauzer (Japan) [T-En by ArcaneAria v1.2.1]
ERROR: Panasonic - 3DO: multiple games writing to the same output path: /out/3DO/_Panasonic - 3DO Interactive Multiplayer [T-En] Docs.zip
ERROR:   _Panasonic - 3DO Interactive Multiplayer [T-En] Docs
ERROR:   _Panasonic - 3DO Interactive Multiplayer [T-En] Docs



### Expected behavior

I am using copy without dat's to merge several rom collections into one. I have successfully completed these commands with cartridge based roms in zip files.

### Debug log

[log.txt](https://github.com/user-attachments/files/27069804/log.txt)

### DAT(s) used

_No response_

### igir version

5.0.1

### Node.js version

_No response_

### Operating system

cachyOS

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0d6cf4c33c8748af5f83cf3d94b98a9595dcae79`.  There
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
{"case_id": "emmercm_igir__2213__0d6cf4c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
