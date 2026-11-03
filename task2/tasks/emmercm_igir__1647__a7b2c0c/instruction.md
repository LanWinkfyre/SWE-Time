# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
ROMs incorrectly marked as INCOMPLETE

### Paste the command

bin/igir move zip test clean report -vvv --dat ../platforms/triforce/dats/*.dat --input ../platforms/triforce/import/ --input ../platforms/triforce/output/ --output ../platforms/triforce/output/ --report-output ../platforms/triforce/report.csv --clean-backup ../platforms/triforce/backup/ --single --only-retail --no-unlicensed --no-device --no-bios --prefer-revision newer --prefer-region USA,WORLD,EUR,JPN

### Describe the bug

It seems like the latest version of Igir marks roms as INCOMPLETE even though they seem to be complete (they are moved to the output directory). Furthermore it shouldn't move them to the output directory if that statement is true

![Image](https://github.com/user-attachments/assets/03d2902c-f4d8-4910-ab9e-672e3b3117b0)

### Expected behavior

I expect Igir to not move INCOMPLETE roms unless `--allow-incomplete-sets` is set. If they are complete I expect them to be marked as FOUND/COMPLETE.

Report:
```
DAT Name,Game Name,Status,ROM Files,Patched,BIOS,Retail Release,Unlicensed,Debug,Demo,Beta,Sample,Prototype,Program,Aftermarket,Homebrew,Bad
Arcade - Namco - Sega - Nintendo - Triforce,Avalon no Kagi (Main) (Japan) (Rev G),INCOMPLETE,../platforms/triforce/output/Avalon no Kagi (Main) (Japan) (Rev G).zip,false,false,true,false,false,false,false,false,false,false,false,false,false
Arcade - Namco - Sega - Nintendo - Triforce,Avalon no Kagi (Satellite) (Japan) (Rev F),INCOMPLETE,../platforms/triforce/output/Avalon no Kagi (Satellite) (Japan) (Rev F).zip,false,false,true,false,false,false,false,false,false,false,false,false,false
Arcade - Namco - Sega - Nintendo - Triforce,Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A),INCOMPLETE,../platforms/triforce/output/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip,false,false,true,false,false,false,false,false,false,false,false,false,false
Arcade - Namco - Sega - Nintendo - Triforce,Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B),INCOMPLETE,../platforms/triforce/output/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip,false,false,true,false,false,false,false,false,false,false,false,false,false
Arcade - Namco - Sega - Nintendo - Triforce,Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C),INCOMPLETE,../platforms/triforce/output/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip,false,false,true,false,false,false,false,false,false,false,false,false,false
Arcade - Namco - Sega - Nintendo - Triforce,Virtua Striker 2002 (World),INCOMPLETE,../platforms/triforce/output/Virtua Striker 2002 (World).zip,false,false,true,false,false,false,false,false,false,false,false,false,false
Arcade - Namco - Sega - Nintendo - Triforce,Virtua Striker 4 (World),INCOMPLETE,../platforms/triforce/output/Virtua Striker 4 (World).zip,false,false,true,false,false,false,false,false,false,false,false,false,false
Arcade - Namco - Sega - Nintendo - Triforce,Virtua Striker 4 Ver. 2006 (Japan) (Rev D),INCOMPLETE,../platforms/triforce/output/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip,false,false,true,false,false,false,false,false,false,false,false,false,false
```

### Debug logs

```
[10:15:43.008] TRACE: Parsing CLI arguments: move zip test clean report -vvv --dat ../platforms/triforce/dats/*.dat --input ../platforms/triforce/import/ --input ../platforms/triforce/output/ --output ../platforms/triforce/output/ --report-output ../platforms/triforce/report.csv --clean-backup ../platforms/triforce/backup/ --single --only-retail --no-unlicensed --no-device --no-bios --prefer-revision newer --prefer-region USA,WORLD,EUR,JPN
[10:15:43.009] TRACE: Parsed CLI options: {"_":["move","zip","test","clean","report"],"input":["../platforms/triforce/import/","../platforms/triforce/output/"],"inputExclude":[],"inputChecksumQuick":false,"inputChecksumMin":"CRC32","inputChecksumArchives":"auto","dat":["../platforms/triforce/dats/*.dat"],"datExclude":[],"datCombine":false,"datIgnoreParentClone":false,"patch":[],"patchExclude":[],"output":"../platforms/triforce/output/","dirMirror":false,"dirDatMirror":false,"dirDatName":false,"dirDatDescription":false,"dirLetter":false,"dirLetterCount":1,"dirLetterLimit":0,"dirLetterGroup":false,"dirGameSubdir":"multiple","fixExtension":"auto","overwrite":false,"overwriteInvalid":false,"moveDeleteDirs":"auto","cleanExclude":[],"cleanBackup":"../platforms/triforce/backup/","cleanDryRun":false,"zipFormat":"torrentzip","zipExclude":"","zipDatName":false,"linkMode":"hardlink","symlinkRelative":false,"header":"","mergeRoms":"fullnonmerged","mergeDiscs":false,"excludeDisks":false,"allowExcessSets":false,"allowIncompleteSets":false,"filterLanguage":[],"filterRegion":[],"noBios":true,"onlyBios":false,"noDevice":true,"onlyDevice":false,"noUnlicensed":true,"onlyUnlicensed":false,"onlyRetail":true,"noDebug":false,"onlyDebug":false,"noDemo":false,"onlyDemo":false,"noBeta":false,"onlyBeta":false,"noSample":false,"onlySample":false,"noPrototype":false,"onlyPrototype":false,"noProgram":false,"onlyProgram":false,"noAftermarket":false,"onlyAftermarket":false,"noHomebrew":false,"onlyHomebrew":false,"noUnverified":false,"onlyUnverified":false,"noBad":false,"onlyBad":false,"single":true,"preferVerified":false,"preferGood":false,"preferLanguage":[],"preferRegion":["USA","WORLD","EUR","JPN"],"preferRevision":"newer","preferRetail":false,"preferParent":false,"playlistExtensions":[".cue",".gdi",".mdf",".chd"],"reportOutput":"../platforms/triforce/report.csv","datThreads":2,"readerThreads":8,"writerThreads":4,"writeRetry":2,"tempDir":"/tmp/igir/20250626-101542","disableCache":false,"verbose":3,"help":false,"v":3,"d":["../platforms/triforce/dats/*.dat"],"i":["../platforms/triforce/import/","../platforms/triforce/output/"],"o":"../platforms/triforce/output/","report-output":"../platforms/triforce/report.csv","clean-backup":"../platforms/triforce/backup/","s":true,"only-retail":true,"no-unlicensed":true,"no-device":true,"no-bios":true,"prefer-revision":"newer","prefer-region":["USA","WORLD","EUR","JPN"],"r":["USA","WORLD","EUR","JPN"],"input-checksum-min":"CRC32","input-checksum-archives":"auto","dir-letter-count":1,"dir-game-subdir":"multiple","fix-extension":"auto","move-delete-dirs":"auto","zip-format":"torrentzip","link-mode":"hardlink","merge-roms":"fullnonmerged","playlist-extensions":[".cue",".gdi",".mdf",".chd"],"dat-threads":2,"reader-threads":8,"writer-threads":4,"write-retry":2,"$0":"igir"}
[10:15:43.043] TRACE: loading the file cache at '/root/igir.cache'
[10:15:43.044] TRACE: _DATScanner: scanning DAT files
[10:15:43.068] TRACE: _DATScanner: found 1 DAT file
[10:15:43.068] TRACE: _DATScanner: enumerating DAT archives
[10:15:43.086] TRACE: _DATScanner: parsing 1 DAT file
[10:15:43.087] TRACE: _DATScanner: ../platforms/triforce/dats/Arcade - Namco - Sega - Nintendo - Triforce - Datfile (22) (2024-03-27 18-54-01).dat: attempting to get ListXML from MAME executable
[10:15:43.092] TRACE: _DATScanner: ../platforms/triforce/dats/Arcade - Namco - Sega - Nintendo - Triforce - Datfile (22) (2024-03-27 18-54-01).dat: failed to get ListXML from MAME executable: exit code 2
[10:15:43.094] TRACE: _DATScanner: ../platforms/triforce/dats/Arcade - Namco - Sega - Nintendo - Triforce - Datfile (22) (2024-03-27 18-54-01).dat: attempting to parse 20.4KiB of XML
[10:15:43.098] TRACE: _DATScanner: ../platforms/triforce/dats/Arcade - Namco - Sega - Nintendo - Triforce - Datfile (22) (2024-03-27 18-54-01).dat: parsed XML, deserializing to DAT
[10:15:43.104] TRACE: _DATScanner: ../platforms/triforce/dats/Arcade - Namco - Sega - Nintendo - Triforce - Datfile (22) (2024-03-27 18-54-01).dat: NaNundefined of 22 games, 22 parents parsed
[10:15:43.107] TRACE: _DATScanner: done scanning DAT files

 ✓ Scanning for DATs » 1 DAT found

[10:15:43.109] TRACE: _ROMScanner: scanning ROM files
[10:15:43.112] TRACE: _ROMScanner: found 8 ROM files
[10:15:43.181] TRACE: _ROMScanner: done scanning ROM files
[10:15:43.182] TRACE: _ROMHeaderProcessor: no ROMs need their header processed
[10:15:43.183] TRACE: _ROMIndexer: indexing 32 files
[10:15:43.183] TRACE: _ROMIndexer: found 32 unique files
[10:15:43.183] TRACE: _ROMIndexer: done indexing files

 ✓ Scanning for ROMs » 32 files found

[10:15:43.183] TRACE: processing 1 DAT
[10:15:43.184] TRACE: _DATParentInferrer: Arcade - Namco - Sega - Nintendo - Triforce: inferring parents for 22 games
[10:15:43.190] TRACE: _DATParentInferrer: Arcade - Namco - Sega - Nintendo - Triforce: grouped to 9 parents
[10:15:43.190] TRACE: _DATParentInferrer: done inferring parents
[10:15:43.190] TRACE: _DATMergerSplitter: Arcade - Namco - Sega - Nintendo - Triforce: merging & splitting 22 games
[10:15:43.191] TRACE: _DATMergerSplitter: Arcade - Namco - Sega - Nintendo - Triforce: merged/split to 22 games
[10:15:43.191] TRACE: _DATMergerSplitter: Arcade - Namco - Sega - Nintendo - Triforce: done merging & splitting
[10:15:43.191] TRACE: _DATDiscMerger: Arcade - Namco - Sega - Nintendo - Triforce: not merging discs
[10:15:43.191] TRACE: _DATFilter: Arcade - Namco - Sega - Nintendo - Triforce: filtering DAT
[10:15:43.192] TRACE: _DATFilter: Arcade - Namco - Sega - Nintendo - Triforce: filtered to 21/22 games (NaNundefined)
[10:15:43.192] TRACE: _DATFilter: Arcade - Namco - Sega - Nintendo - Triforce: done filtering DAT
[10:15:43.192] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: preferring DAT games
[10:15:43.192] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev A) (parent): 5 games before preferring
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev A) (parent): 3 games before preferring
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A) (parent): 1 game before preferring
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev A) (parent): 2 games before preferring
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C) (parent): 2 games before preferring
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (Japan) (parent): 2 games before preferring
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World) (parent): 4 games before preferring
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev B) (parent): 2 games before preferring
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: preferred to 8/21 games (77.0undefined)
[10:15:43.194] TRACE: _DATPreferer: Arcade - Namco - Sega - Nintendo - Triforce: done preferring DAT games
[10:15:43.194] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: generating candidates
[10:15:43.195] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi (Main) (Japan) (Rev G).zip
[10:15:43.195] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi (Main) (Japan) (Rev G).zip
[10:15:43.195] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi (Main) (Japan) (Rev G).zip
[10:15:43.195] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi (Main) (Japan) (Rev G).zip
[10:15:43.200] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi (Satellite) (Japan) (Rev F).zip
[10:15:43.200] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi (Satellite) (Japan) (Rev F).zip
[10:15:43.200] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi (Satellite) (Japan) (Rev F).zip
[10:15:43.200] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi (Satellite) (Japan) (Rev F).zip
[10:15:43.201] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip
[10:15:43.201] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip
[10:15:43.201] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip
[10:15:43.201] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip
[10:15:43.202] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip
[10:15:43.202] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip
[10:15:43.202] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip
[10:15:43.202] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): preferring input archive that contains every ROM: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip
[10:15:43.203] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): preferring input archive that contains every ROM: ../platforms/triforce/import/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip
[10:15:43.203] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): preferring input archive that contains every ROM: ../platforms/triforce/import/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip
[10:15:43.203] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): preferring input archive that contains every ROM: ../platforms/triforce/import/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip
[10:15:43.203] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): preferring input archive that contains every ROM: ../platforms/triforce/import/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip
[10:15:43.204] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 2002 (World).zip
[10:15:43.204] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 2002 (World).zip
[10:15:43.204] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 2002 (World).zip
[10:15:43.204] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 2002 (World).zip
[10:15:43.204] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 4 (World).zip
[10:15:43.204] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 4 (World).zip
[10:15:43.205] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 4 (World).zip
[10:15:43.205] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 4 (World).zip
[10:15:43.205] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip
[10:15:43.205] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip
[10:15:43.205] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip
[10:15:43.205] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): preferring input archive that contains every ROM: ../platforms/triforce/import/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip
[10:15:43.219] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): found candidate: ../platforms/triforce/import/Avalon no Kagi (Satellite) (Japan) (Rev F).zip
[10:15:43.219] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): found candidate: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip
[10:15:43.219] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): found candidate: ../platforms/triforce/import/Avalon no Kagi (Main) (Japan) (Rev G).zip
[10:15:43.219] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): found candidate: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip
[10:15:43.222] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): found candidate: ../platforms/triforce/import/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip
[10:15:43.222] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): found candidate: ../platforms/triforce/import/Virtua Striker 4 (World).zip
[10:15:43.222] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): found candidate: ../platforms/triforce/import/Virtua Striker 2002 (World).zip
[10:15:43.223] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): found candidate: ../platforms/triforce/import/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip
[10:15:43.223] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: generated 356.1ZiB of 8 candidates
[10:15:43.223] TRACE: _CandidateGenerator: Arcade - Namco - Sega - Nintendo - Triforce: done generating candidates
[10:15:43.223] TRACE: _CandidatePatchGenerator: Arcade - Namco - Sega - Nintendo - Triforce: no patches to make patched candidates for
[10:15:43.223] TRACE: _CandidateExtensionCorrector: Arcade - Namco - Sega - Nintendo - Triforce: no output files need their extension corrected
[10:15:43.223] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: generating 8 hashed ArchiveFile candidates
[10:15:43.223] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: done generating hashed ArchiveFile candidates
[10:15:43.223] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): calculating checksums for: ../platforms/triforce/import/Avalon no Kagi (Satellite) (Japan) (Rev F).zip
[10:15:43.693] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): calculating checksums for: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip
[10:15:44.669] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): calculating checksums for: ../platforms/triforce/import/Avalon no Kagi (Main) (Japan) (Rev G).zip
[10:15:45.064] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): calculating checksums for: ../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip
[10:15:45.835] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): calculating checksums for: ../platforms/triforce/import/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip
[10:15:46.360] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): calculating checksums for: ../platforms/triforce/import/Virtua Striker 4 (World).zip
[10:15:46.360] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): calculating checksums for: ../platforms/triforce/import/Virtua Striker 2002 (World).zip
[10:15:46.785] TRACE: _CandidateArchiveFileHasher: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): calculating checksums for: ../platforms/triforce/import/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip
[10:15:47.373] TRACE: _CandidatePostProcessor: Arcade - Namco - Sega - Nintendo - Triforce: processing candidates
[10:15:47.375] TRACE: _CandidatePostProcessor: Arcade - Namco - Sega - Nintendo - Triforce: done processing candidates
[10:15:47.375] TRACE: _CandidateValidator: Arcade - Namco - Sega - Nintendo - Triforce: validating candidates
[10:15:47.375] TRACE: _CandidateValidator: Arcade - Namco - Sega - Nintendo - Triforce: done validating candidates
[10:15:47.375] TRACE: _CandidateMergeSplitValidator: Arcade - Namco - Sega - Nintendo - Triforce: validating merged & split ROM sets
[10:15:47.375] TRACE: _CandidateMergeSplitValidator: Arcade - Namco - Sega - Nintendo - Triforce: done validating merged & split ROM sets
[10:15:47.377] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: writing 8 candidates
[10:15:47.377] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): writing candidate
[10:15:47.377] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): no zip archives to write
[10:15:47.378] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): writing 358.7MiB of 1 file
[10:15:47.378] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): writing candidate
[10:15:47.378] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): no zip archives to write
[10:15:47.378] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): writing 335.1MiB of 1 file
[10:15:47.380] INFO: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): moving file '../platforms/triforce/import/Avalon no Kagi (Satellite) (Japan) (Rev F).zip' (335.1MiB) → '../platforms/triforce/output/Avalon no Kagi (Satellite) (Japan) (Rev F).zip'
[10:15:47.381] INFO: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): moving file '../platforms/triforce/import/Avalon no Kagi (Main) (Japan) (Rev G).zip' (358.7MiB) → '../platforms/triforce/output/Avalon no Kagi (Main) (Japan) (Rev G).zip'
[10:15:47.383] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Satellite) (Japan) (Rev F): done writing candidate
[10:15:47.387] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi (Main) (Japan) (Rev G): done writing candidate
[10:15:47.393] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): writing candidate
[10:15:47.394] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): no zip archives to write
[10:15:47.394] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): writing 714.7MiB of 1 file
[10:15:47.395] INFO: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): moving file '../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip' (714.7MiB) → '../platforms/triforce/output/Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A).zip'
[10:15:47.396] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Main) (Japan) (Rev A): done writing candidate
[10:15:47.401] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): writing candidate
[10:15:47.401] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): no zip archives to write
[10:15:47.401] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): writing 721.8MiB of 1 file
[10:15:47.402] INFO: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): moving file '../platforms/triforce/import/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip' (721.8MiB) → '../platforms/triforce/output/Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B).zip'
[10:15:47.403] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Avalon no Kagi Ni - Kagi Seisen (Satellite) (Japan) (Rev B): done writing candidate
[10:15:47.408] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): writing candidate
[10:15:47.408] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): no zip archives to write
[10:15:47.408] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): writing 468.7MiB of 1 file
[10:15:47.409] INFO: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): moving file '../platforms/triforce/import/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip' (468.7MiB) → '../platforms/triforce/output/Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C).zip'
[10:15:47.411] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Gekitou Pro Yakyuu - Mizushima Shinji All Stars vs. Pro Yakyuu (Japan) (Rev C): done writing candidate
[10:15:47.416] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): writing candidate
[10:15:47.416] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): no zip archives to write
[10:15:47.416] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): writing candidate
[10:15:47.416] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): no zip archives to write
[10:15:47.416] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): writing 264.4MiB of 1 file
[10:15:47.416] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): writing 342.2MiB of 1 file
[10:15:47.417] INFO: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): moving file '../platforms/triforce/import/Virtua Striker 2002 (World).zip' (264.4MiB) → '../platforms/triforce/output/Virtua Striker 2002 (World).zip'
[10:15:47.417] INFO: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): moving file '../platforms/triforce/import/Virtua Striker 4 (World).zip' (342.2MiB) → '../platforms/triforce/output/Virtua Striker 4 (World).zip'
[10:15:47.418] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 (World): done writing candidate
[10:15:47.420] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): writing candidate
[10:15:47.420] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): no zip archives to write
[10:15:47.420] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): writing 421.9MiB of 1 file
[10:15:47.420] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 2002 (World): done writing candidate
[10:15:47.422] INFO: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): moving file '../platforms/triforce/import/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip' (421.9MiB) → '../platforms/triforce/output/Virtua Striker 4 Ver. 2006 (Japan) (Rev D).zip'
[10:15:47.424] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: Virtua Striker 4 Ver. 2006 (Japan) (Rev D): done writing candidate
[10:15:47.428] TRACE: _CandidateWriter: Arcade - Namco - Sega - Nintendo - Triforce: done writing 8 candidates
[10:15:47.428] TRACE: _StatusGenerator: Arcade - Namco - Sega - Nintendo - Triforce: generating ROM statuses
[10:15:47.429] TRACE: _StatusGenerator: Arcade - Namco - Sega - Nintendo - Triforce: done generating ROM statuses

 ✓ Arcade - Namco - Sega - Nintendo - Triforce » 0/8 retail releases written

[10:15:47.429] TRACE: done processing 1 DAT
[10:15:47.430] TRACE: _DirectoryCleaner: cleaning files in output
[10:15:47.431] DEBUG: _DirectoryCleaner: no files to clean

 ✓ Cleaning output directory » 0 files recycled

[10:15:47.431] TRACE: _ReportGenerator: generating report
[10:15:47.435] INFO: _ReportGenerator: writing report '../platforms/triforce/report.csv'
[10:15:47.483] TRACE: _ReportGenerator: wrote 1 CSV row: ../platforms/triforce/report.csv
[10:15:47.483] TRACE: _ReportGenerator: done generating report

 ✓ Generating report » ../platforms/triforce/report.csv
```

### DAT(s) used

Arcade - Namco - Sega - Nintendo - Triforce - Datfile (22) (2024-03-27 18-54-01).dat

### igir version

NIGHTLY (ebf7398)

### Node.js version

N/A

### Operating system

Linux/Unraid

### Additional context

_No response_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a7b2c0ce26e31ebf3903765189c12c1ab03fcd9f`.  There
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
{"case_id": "emmercm_igir__1647__a7b2c0c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
