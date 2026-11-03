# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Hardware Target Game Database SMDB ignore file extension (missing files when used with bin/cue)

### Paste the command

igir copy/move/link report --dat https://github.com/frederic-mahe/Hardware-Target-Game-Database/raw/refs/heads/master/EverDrive%20Pack%20SMDBs/PlayStation%20Redump%20Supplement.txt [...]

### Describe the bug

Igir seems to ignore file extensions when handling Hardware Target Game Database SMDBs resulting in missing files for any rom containing multiple files with the same name, but different file extensions. Notably this is the case with disc-based systems, where e.g. there is both a `.bin` file and a `.cue` file with the same name.

Example lines from HTGDB repo
```
92a24502b4f2c1758307a126176d1a2610b4b38481fe04e941f7d139dd8a36f6	PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1].bin	d828a7eed6a4cc90c2837d61e0f4766e191ac8f3	ff911668c363132913f5d06f31780340	f533768f
13de7e5e418782079ac3d31ccc1a1d440d2b60d342d4ceca6f7b8822e78b1d79	PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1].cue	3e6887c80f058dbd9f746a7395c7fc9282c6e0a4	da672f6dcf641e680921b109120b1738	b51d3336
```

Results in only one file being detected by Igir. In this case the `.bin` file, I assume simply due to alphabetical ordering. Igir reports no missing files for this particular title.

Igir report:
```
PlayStation Redump Supplement.txt,PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1],FOUND,dest/PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1].bin,false,false,true,false,false,false,false,false,false,false,false,false,false
```



### Expected behavior

All lines in source SMDB files are parsed, including files with identical names but different file extensions. A SMDB with both .bin and .cue files of the same name should result in all of these files being present in Igir output directory.

### Debug logs

```
[11:37:27.610] TRACE: Parsing CLI arguments: link test clean report --dat https://raw.githubusercontent.com/frederic-mahe/Hardware-Target-Game-Database/refs/heads/master/EverDrive%20Pack%20SMDBs/PlayStation%20Redump%20Supplement.txt --input source/ --output dest/ --overwrite-invalid -vvv
[11:37:27.611] TRACE: Parsed CLI options: {"_":["link","test","clean","report"],"input":["source/"],"inputExclude":[],"inputChecksumQuick":false,"inputChecksumMin":"CRC32","inputChecksumArchives":"auto","dat":["https://raw.githubusercontent.com/frederic-mahe/Hardware-Target-Game-Database/refs/heads/master/EverDrive%20Pack%20SMDBs/PlayStation%20Redump%20Supplement.txt"],"datExclude":[],"datCombine":false,"datIgnoreParentClone":false,"patch":[],"patchExclude":[],"output":"dest/","dirMirror":false,"dirDatName":false,"dirDatDescription":false,"dirLetter":false,"dirLetterCount":1,"dirLetterLimit":0,"dirLetterGroup":false,"dirGameSubdir":"multiple","fixExtension":"auto","overwrite":false,"overwriteInvalid":true,"cleanExclude":[],"cleanDryRun":false,"zipExclude":"","zipDatName":false,"symlink":false,"symlinkRelative":false,"header":"","mergeRoms":"fullnonmerged","mergeDiscs":false,"excludeDisks":false,"allowExcessSets":false,"allowIncompleteSets":false,"filterLanguage":[],"filterRegion":[],"noBios":false,"onlyBios":false,"noDevice":false,"onlyDevice":false,"noUnlicensed":false,"onlyUnlicensed":false,"onlyRetail":false,"noDebug":false,"onlyDebug":false,"noDemo":false,"onlyDemo":false,"noBeta":false,"onlyBeta":false,"noSample":false,"onlySample":false,"noPrototype":false,"onlyPrototype":false,"noProgram":false,"onlyProgram":false,"noAftermarket":false,"onlyAftermarket":false,"noHomebrew":false,"onlyHomebrew":false,"noUnverified":false,"onlyUnverified":false,"noBad":false,"onlyBad":false,"single":false,"preferVerified":false,"preferGood":false,"preferLanguage":[],"preferRegion":[],"preferRetail":false,"preferParent":false,"playlistExtensions":[".cue",".gdi",".mdf",".chd"],"reportOutput":"./igir_%YYYY-%MM-%DDT%HH:%mm:%ss.csv","datThreads":3,"readerThreads":8,"writerThreads":4,"writeRetry":2,"tempDir":"/tmp/igir/20250424-113727","disableCache":false,"verbose":3,"help":false,"d":["https://raw.githubusercontent.com/frederic-mahe/Hardware-Target-Game-Database/refs/heads/master/EverDrive%20Pack%20SMDBs/PlayStation%20Redump%20Supplement.txt"],"i":["source/"],"o":"dest/","overwrite-invalid":true,"v":3,"input-checksum-min":"CRC32","input-checksum-archives":"auto","dir-letter-count":1,"dir-game-subdir":"multiple","fix-extension":"auto","merge-roms":"fullnonmerged","playlist-extensions":[".cue",".gdi",".mdf",".chd"],"report-output":"./igir_%YYYY-%MM-%DDT%HH:%mm:%ss.csv","dat-threads":3,"reader-threads":8,"writer-threads":4,"write-retry":2,"$0":"igir"}
[11:37:27.647] TRACE: loading the file cache at '/home/bobosabisu/igir.cache'
[11:37:52.688] TRACE: DATScanner: scanning DAT files
[11:37:52.734] TRACE: DATScanner: found 1 DAT file
[11:37:52.735] TRACE: DATScanner: enumerating DAT archives
[11:37:52.747] TRACE: DATScanner: downloading 1 DAT from URL
[11:37:52.748] TRACE: DATScanner: https://raw.githubusercontent.com/frederic-mahe/Hardware-Target-Game-Database/refs/heads/master/EverDrive%20Pack%20SMDBs/PlayStation%20Redump%20Supplement.txt: downloading
[11:37:52.976] TRACE: DATScanner: https://raw.githubusercontent.com/frederic-mahe/Hardware-Target-Game-Database/refs/heads/master/EverDrive%20Pack%20SMDBs/PlayStation%20Redump%20Supplement.txt: downloaded to '/tmp/igir/20250424-113727/PlayStation Redump Supplement.txt.jtizcj'
[11:37:52.992] TRACE: DATScanner: parsing 1 DAT file
[11:37:52.994] TRACE: DATScanner: /tmp/igir/20250424-113727/PlayStation Redump Supplement.txt.jtizcj: attempting to parse 101.2KB of XML
[11:37:52.997] TRACE: DATScanner: /tmp/igir/20250424-113727/PlayStation Redump Supplement.txt.jtizcj: parsed XML, deserializing to DAT
[11:37:52.998] TRACE: DATScanner: /tmp/igir/20250424-113727/PlayStation Redump Supplement.txt.jtizcj: parsed XML, but failed to find a known DAT root
[11:37:52.998] TRACE: DATScanner: /tmp/igir/20250424-113727/PlayStation Redump Supplement.txt.jtizcj: attempting to parse SMDB
[11:37:53.016] TRACE: DATScanner: /tmp/igir/20250424-113727/PlayStation Redump Supplement.txt.jtizcj: parsed SMDB, deserializing to DAT
[11:37:53.019] TRACE: DATScanner: /tmp/igir/20250424-113727/PlayStation Redump Supplement.txt.jtizcj: 6.5GB of 338 games, 220 parents parsed
[11:37:53.025] TRACE: DATScanner: done scanning DAT files
Scanning for DATs ... 1 DAT found
[11:37:53.029] TRACE: PlayStation Redump Supplement.txt: needs MD5 file checksums for ROMs, enabling
[11:37:53.033] TRACE: ROMScanner: scanning ROM files
[11:37:53.035] TRACE: ROMScanner: found 6 ROM files
[11:37:53.080] TRACE: ROMScanner: done scanning ROM files
[11:37:53.081] TRACE: ROMHeaderProcessor: no ROMs need their header processed
[11:37:53.081] TRACE: ROMIndexer: indexing 8 files
[11:37:53.082] TRACE: ROMIndexer: found 8 unique files
[11:37:53.082] TRACE: ROMIndexer: done indexing files
Scanning for ROMs ... 8 files found
[11:37:53.083] TRACE: processing 1 DAT
[11:37:53.083] TRACE: DATParentInferrer: PlayStation Redump Supplement.txt: DAT has parent/clone info, skipping
[11:37:53.084] TRACE: DATMergerSplitter: PlayStation Redump Supplement.txt: merging & splitting 338 games
[11:37:53.086] TRACE: DATMergerSplitter: PlayStation Redump Supplement.txt: merged/split to 220 games
[11:37:53.086] TRACE: DATMergerSplitter: PlayStation Redump Supplement.txt: done merging & splitting
[11:37:53.087] TRACE: DATDiscMerger: PlayStation Redump Supplement.txt: not merging discs
[11:37:53.087] TRACE: DATFilter: PlayStation Redump Supplement.txt: filtering DAT
[11:37:53.089] TRACE: DATFilter: PlayStation Redump Supplement.txt: filtered to 220/220 games (6.1GB)
[11:37:53.089] TRACE: DATFilter: PlayStation Redump Supplement.txt: done filtering DAT
[11:37:53.089] TRACE: DATPreferer: PlayStation Redump Supplement.txt: not running in single/1G1R mode, not preferring games
[11:37:53.090] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: generating candidates

[...]

[11:37:53.115] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1]: found 1 candidate
[11:37:53.115] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1] (parent): found 1 candidate
[11:37:53.116] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 1): found 1 candidate
[11:37:53.116] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 1) (parent): found 1 candidate
[11:37:53.116] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 2): found 1 candidate
[11:37:53.116] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 2) (parent): found 1 candidate
[11:37:53.116] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met: found 1 candidate
[11:37:53.116] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (parent): found 1 candidate
[11:37:53.116] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: generated 0B of 4 candidates for 220 parents
[11:37:53.116] TRACE: CandidateGenerator: PlayStation Redump Supplement.txt: done generating candidates
[11:37:53.116] TRACE: CandidatePatchGenerator: PlayStation Redump Supplement.txt: generating patched candidates
[11:37:53.225] TRACE: CandidatePatchGenerator: PlayStation Redump Supplement.txt: 0 unique patches found
[11:37:53.225] TRACE: CandidatePatchGenerator: PlayStation Redump Supplement.txt: done generating patched candidates
[11:37:53.226] TRACE: CandidateExtensionCorrector: PlayStation Redump Supplement.txt: no output files need their extension corrected
[11:37:53.226] TRACE: CandidateArchiveFileHasher: PlayStation Redump Supplement.txt: no ArchiveFiles to hash
[11:37:53.226] TRACE: CandidatePostProcessor: PlayStation Redump Supplement.txt: processing candidates
[11:37:53.229] TRACE: CandidatePostProcessor: PlayStation Redump Supplement.txt: done processing candidates
[11:37:53.229] TRACE: CandidateValidator: PlayStation Redump Supplement.txt: validating candidates
[11:37:53.230] TRACE: CandidateValidator: PlayStation Redump Supplement.txt: done validating candidates
[11:37:53.230] TRACE: CandidateMergeSplitValidator: PlayStation Redump Supplement.txt: validating merged & split ROM sets
[11:37:53.230] TRACE: CandidateMergeSplitValidator: PlayStation Redump Supplement.txt: done validating merged & split ROM sets
[11:37:53.232] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: writing 4 candidates
[11:37:53.233] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1] (parent): writing 1 candidate
[11:37:53.233] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 1) (parent): writing 1 candidate
[11:37:53.233] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 2) (parent): writing 1 candidate
[11:37:53.233] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (parent): writing 1 candidate
[11:37:53.235] INFO:  CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1]: creating hard link 'source/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1].bin' → 'dest/PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1].bin'
[11:37:53.243] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1] (parent): done writing 1 candidate
[11:37:53.244] INFO:  CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 1): creating hard link 'source/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 1).bin' → 'dest/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 1).bin'
[11:37:53.244] INFO:  CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 2): creating hard link 'source/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 2).bin' → 'dest/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 2).bin'
[11:37:53.244] INFO:  CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met: creating hard link 'source/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met.cue' → 'dest/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met.cue'
[11:37:53.249] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 1) (parent): done writing 1 candidate
[11:37:53.253] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 2) (parent): done writing 1 candidate
[11:37:53.258] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (parent): done writing 1 candidate
[11:37:53.258] TRACE: CandidateWriter: PlayStation Redump Supplement.txt: done writing 4 candidates
[11:37:53.259] TRACE: StatusGenerator: PlayStation Redump Supplement.txt: generating ROM statuses
[11:37:53.262] TRACE: StatusGenerator: PlayStation Redump Supplement.txt: done generating ROM statuses
PlayStation Redump Supplement.txt ... 4/220 games, 4/114 retail releases written
[11:37:53.277] TRACE: done processing 1 DAT
[11:37:53.278] TRACE: DirectoryCleaner: cleaning files in output
[11:37:53.282] TRACE: DirectoryCleaner: cleaning 4 files
[11:37:53.282] INFO:  DirectoryCleaner: recycling cleaned paths:
[11:37:53.282] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper/Alundra (USA) [Un-Worked Design v1].bin
[11:37:53.282] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 1).bin
[11:37:53.282] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met (Track 2).bin
[11:37:53.282] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met/Castlevania - Symphony of the Night [Quality Hack] v1.3 paul_met.cue
[11:37:54.837] TRACE: DirectoryCleaner: cleaning 2 empty directories
[11:37:54.837] INFO:  DirectoryCleaner: recycling cleaned paths:
[11:37:54.837] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper
[11:37:54.837] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met
[11:37:54.865] WARN:  DirectoryCleaner: failed to recycle 2 paths: EISDIR: illegal operation on a directory, copyfile '/srv/samba/downloads/htgdb-test/dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met' -> '/mnt/totoro/downloads/.Trash-1000/files/5166104a-3d2c-4916-951b-5b691dc4df8e'
[11:37:54.866] INFO:  DirectoryCleaner: deleting cleaned paths:
[11:37:54.866] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Alundra Un-Worked Design (U) v1 Supper
[11:37:54.866] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations/Castlevania - SOTN Improvement (U) v1.3 paul_met
[11:37:54.869] TRACE: DirectoryCleaner: cleaning 1 empty directory
[11:37:54.869] INFO:  DirectoryCleaner: recycling cleaned path:
[11:37:54.869] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations
[11:37:54.897] WARN:  DirectoryCleaner: failed to recycle 1 path: EISDIR: illegal operation on a directory, copyfile '/srv/samba/downloads/htgdb-test/dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations' -> '/mnt/totoro/downloads/.Trash-1000/files/1f960ed3-36fa-406b-99d3-fb4ed7888674'
[11:37:54.897] INFO:  DirectoryCleaner: deleting cleaned path:
[11:37:54.897] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement/@Improvements & Restorations
[11:37:54.898] TRACE: DirectoryCleaner: cleaning 1 empty directory
[11:37:54.899] INFO:  DirectoryCleaner: recycling cleaned path:
[11:37:54.899] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement
[11:37:54.925] WARN:  DirectoryCleaner: failed to recycle 1 path: EISDIR: illegal operation on a directory, copyfile '/srv/samba/downloads/htgdb-test/dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement' -> '/mnt/totoro/downloads/.Trash-1000/files/88059c31-ccb3-4df0-a11c-521ba37aeef8'
[11:37:54.925] INFO:  DirectoryCleaner: deleting cleaned path:
[11:37:54.925] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt/PlayStation Redump Supplement
[11:37:54.927] TRACE: DirectoryCleaner: cleaning 1 empty directory
[11:37:54.927] INFO:  DirectoryCleaner: recycling cleaned path:
[11:37:54.927] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt
[11:37:54.955] WARN:  DirectoryCleaner: failed to recycle 1 path: EISDIR: illegal operation on a directory, copyfile '/srv/samba/downloads/htgdb-test/dest/PlayStation Redump Supplement.txt' -> '/mnt/totoro/downloads/.Trash-1000/files/b3f92d91-b002-453d-9201-be3444666227'
[11:37:54.956] INFO:  DirectoryCleaner: deleting cleaned path:
[11:37:54.956] INFO:  DirectoryCleaner:   dest/PlayStation Redump Supplement.txt
[11:37:54.957] TRACE: DirectoryCleaner: done cleaning files in output
Cleaning output directory ... 4 files recycled
[11:37:54.959] TRACE: ReportGenerator: generating report
[11:37:54.973] INFO:  ReportGenerator: writing report './igir_2025-04-24T11;37;54.csv'
[11:37:55.258] TRACE: ReportGenerator: wrote 1 CSV row: ./igir_2025-04-24T11;37;54.csv
[11:37:55.258] TRACE: ReportGenerator: done generating report
Generating report ... ./igir_2025-04-24T11;37;54.csv
```

### DAT(s) used

https://github.com/frederic-mahe/Hardware-Target-Game-Database/raw/refs/heads/master/EverDrive%20Pack%20SMDBs/PlayStation%20Redump%20Supplement.txt

### igir version

v3.3.0

### Node.js version

v22.13.1

### Operating system

Almalinux 9.5

### Additional context

Haven't had time to update Igir to latest version yet, but release notes seemingly don't include any fixes for this issue.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4001461732c228ea7814c64837b4e426bababaf8`.  There
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
{"case_id": "emmercm_igir__1554__4001461",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
