# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Parsing 7z archive (with multiple roms) results in: EXDEV: cross-device link not permitted

### Paste the command

```
igir move extract test --dat "Atari - Atari Lynx (LNX) (Parent-Clone) (20241112-103004).dat" --input "./test7z/" "./lynx/" --output "./lynx/" --dir-dat-name -vvv
```

### Describe the bug

`extract` on 7z file (either with `move` or `copy`) results in `EXDEV: cross-device link not permitted`:

```
 EXDEV: cross-device link not permitted, rename '/tmp/igir/20250310-110529/7z/6GygSw/Atari Lynx/4 Homebrew/SiIas Adventure (PD) KK & Altair         
2019.lnx' -> 'lynx/Atari - Atari Lynx (LNX)/Silas Adventure (World) (Aftermarket) (Unl).lnx.1cr9k1j'              
```

Error applies to apparently all matched roms.

After completing the igir command, no files are present in the output directory.

### Expected behavior

Files within 7z archive should be extracted (to cache dir) and (after that) moved (or copied) to the output directory.

### Debug logs

```console
[11:05:30.052] TRACE: Parsing CLI arguments: move extract test --dat "Atari - Atari Lynx (LNX) (Parent-Clone) (20241112-103004).dat" --input ./test7z/ ./lynx/ 
--output ./lynx/ --dir-dat-name -vvv                                                                                                                           
[11:05:30.054] TRACE: Parsed CLI options: {"_":["move","extract","test"],"input":["./test7z/","./lynx/"],"inputExclude":[],"inputChecksumQuick":false,"inputChe
cksumMin":"CRC32","inputChecksumArchives":"auto","dat":["Atari - Atari Lynx (LNX) (Parent-Clone) (20241112-103004).dat"],"datExclude":[],"datNameRegex":"","dat
NameRegexExclude":"","datDescriptionRegex":"","datDescriptionRegexExclude":"","datCombine":false,"datIgnoreParentClone":false,"patch":[],"patchExclude":[],"out
put":"./lynx/","dirMirror":false,"dirDatName":true,"dirDatDescription":false,"dirLetter":false,"dirLetterCount":1,"dirLetterLimit":0,"dirLetterGroup":false,"di
rGameSubdir":"multiple","fixExtension":"auto","overwrite":false,"overwriteInvalid":false,"cleanExclude":[],"cleanDryRun":false,"zipExclude":"","zipDatName":fal
se,"symlink":false,"symlinkRelative":false,"header":"","mergeRoms":"fullnonmerged","excludeDisks":false,"allowExcessSets":false,"allowIncompleteSets":false,"fi
lterRegex":"","filterRegexExclude":"","filterLanguage":[],"filterRegion":[],"noBios":false,"onlyBios":false,"noDevice":false,"onlyDevice":false,"noUnlicensed":false,"onlyUnlicensed":false,"onlyRetail":false,"noDebug":false,"onlyDebug":false,"noDemo":false,"onlyDemo":false,"noBeta":false,"onlyBeta":false,"noSample":false,"onlySample":false,"noPrototype":false,"onlyPrototype":false,"noProgram":false,"onlyProgram":false,"noAftermarket":false,"onlyAftermarket":false,"noHomebrew":false,"onlyHomebrew":false,"noUnverified":false,"onlyUnverified":false,"noBad":false,"onlyBad":false,"single":false,"preferGameRegex":"","preferRomRegex":"","preferVerified":false,"preferGood":false,"preferLanguage":[],"preferRegion":[],"preferRetail":false,"preferParent":false,"reportOutput":"./igir_%YYYY-%MM-%DD
T%HH:%mm:%ss.csv","datThreads":3,"readerThreads":8,"writerThreads":4,"writeRetry":2,"tempDir":"/tmp/igir/20250310-110529","disableCache":false,"verbose":3,"hel
p":false,"d":["Atari - Atari Lynx (LNX) (Parent-Clone) (20241112-103004).dat"],"i":["./test7z/","./lynx/"],"o":"./lynx/","dir-dat-name":true,"D":true,"v":3,"in
put-checksum-min":"CRC32","input-checksum-archives":"auto","dir-letter-count":1,"dir-game-subdir":"multiple","fix-extension":"auto","merge-roms":"fullnonmerged
","report-output":"./igir_%YYYY-%MM-%DDT%HH:%mm:%ss.csv","dat-threads":3,"reader-threads":8,"writer-threads":4,"write-retry":2,"$0":"igir"}
...
[11:09:53.806] ERROR: CandidateWriter: Atari - Atari Lynx (LNX): Silas Adventure (World) (Aftermarket) (Unl): failed to extract file 'test7z/@Atari Lynx       
2021-03-17.7z|Atari Lynx/4 Homebrew/SiIas Adventure (PD) KK & Altair 2019.lnx' → 'lynx/Atari - Atari Lynx (LNX)/Silas Adventure (World) (Aftermarket)          
(Unl).lnx': EXDEV: cross-device link not permitted, rename '/tmp/igir/20250310-110529/7z/6GygSw/Atari Lynx/4 Homebrew/SiIas Adventure (PD) KK & Altair         
2019.lnx' -> 'lynx/Atari - Atari Lynx (LNX)/Silas Adventure (World) (Aftermarket) (Unl).lnx.1cr9k1j'                                                           
[11:09:53.806] INFO:  CandidateWriter: Atari - Atari Lynx (LNX): Silly Blaster (World) (Aftermarket) (Unl): extracting file 'test7z/@Atari Lynx                
2021-03-17.7z|Atari Lynx/4 Homebrew/Silly Blaster (PD) Fadest 2019.lnx' (256.1KB) → 'lynx/Atari - Atari Lynx (LNX)/Silly Blaster (World) (Aftermarket)         
(Unl).lnx'                                                                                                                                                     
[11:09:53.810] TRACE: CandidateWriter: Atari - Atari Lynx (LNX): Silas Adventure (World) (Aftermarket) (Unl) (parent): done writing 1 candidate
...

```

### DAT(s) used

No-Intro Atari Lynx (LNX)

### igir version

v3.1.0

### Node.js version

v22.13.1

### Operating system

Almalinux 9.5

### Additional context

Trace logs do not provide much helpful info to me. It appears the extracted file is renamed to another directory, which does not work when the output dir is on another file system. My `/tmp` and output directory are indeed not on the same filesystem.

I'd expect that igir expects /tmp to be on another file system, so unless this is a new bug, it might have something to do with my system configuration. If so, I'm not sure what's happening under the hood to debug this further.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `26927b6a073cd3054d4af610d4bdb63460c12359`.  There
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
{"case_id": "emmercm_igir__1479__26927b6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
