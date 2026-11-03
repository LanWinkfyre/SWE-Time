# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
CHD Re-scan after --input-checksum-quick finds no files in archive

### Paste the command

```
igir link clean playlist \
  --dat "/mnt/synology/isos_roms_and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat" \
  --input "/mnt/synology/isos_roms_and_saves/test/Sonic CD (USA).chd" \
  --output "/home/dusty/test" \
  --link-mode symlink \
  --clean-exclude "/home/dusty/ROMs/**/*.(txt|sh)" \
  --no-bios \
  --single \
  --prefer-language EN,JA \
  --prefer-region USA,WORLD,EUR,JPN \
  --prefer-revision newer \
  --prefer-retail
```

### Describe the bug

I've been experimenting with scanning/filtering CHDs. I'm doing this so that I can store my collection in a compressed way, but still be able to play games without decompressing and taking up lots of extra space. For CHDs that were manually created from bin/cue using `chdman createcd -i <cue_file> -o <chd_file>`, when scanning with the option `--input-checksum-quick`, it fails with the error `didn't find any files in the archive`, because no checksums in the CHD headers match the supplied DAT. That is annoying, but not the bug. The bug is that when I then re-scan WITHOUT the `--input-checksum-quick` option, the file is being read from the cache, igir sees that no matching files were found originally, and skips the CHD entirely with the same error as before, `didn't find any files in the archive`.

### Expected behavior

I would expect that if a scan does not show any files when scanning with `--input-checksum-quick`, then nothing would be added to the cache. This way, when re-scanning without that option, full decompression happens. Or, add a flag in the cache that nothing was found last scan with --input-checksum-quick, and it should be re-scanned next time.

### Debug logs

   @@@@@@   @@@@@@     @@@@@@    @@@@@@@@
 @@      @@  @@      @@      @@         @@
 @@      @@  @@      @@      @@         @@   ROM collection manager
   @@@@@@   @@         @@@@@@   @@@@@@@@@    https://igir.io/
          @@@     @@@@        @@@
     @@   @@        @@   @@   @@       @@    v4.2.0
     @@   @@        @@   @@   @@       @@
     @@   @@@@@@@@@@@@   @@   @@       @@

[10:53:51.569] TRACE: Parsing CLI arguments: link clean playlist --dat "/mnt/synology/isos_roms_and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat" --inpu
t "/mnt/synology/isos_roms_and_saves/test/Sonic CD (USA).chd" --output /home/dusty/test --link-mode symlink --clean-exclude /home/dusty/ROMs/**/*.(txt|sh) --no-bios --single --prefer-language 
EN,JA --prefer-region USA,WORLD,EUR,JPN --prefer-revision newer --prefer-retail -vvv
[10:53:51.570] TRACE: Parsed CLI options: {"_":["link","clean","playlist"],"input":["/mnt/synology/isos_roms_and_saves/test/Sonic CD (USA).chd"],"inputExclude":[],"inputChecksumQuick":false,"i
nputChecksumMin":"CRC32","inputChecksumArchives":"auto","dat":["/mnt/synology/isos_roms_and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat"],"datExclude":
[],"datCombine":false,"datIgnoreParentClone":false,"patch":[],"patchExclude":[],"output":"/home/dusty/test","dirMirror":false,"dirDatMirror":false,"dirDatName":false,"dirDatDescription":false,
"dirLetter":false,"dirLetterCount":1,"dirLetterLimit":0,"dirLetterGroup":false,"dirGameSubdir":"multiple","fixExtension":"auto","overwrite":false,"overwriteInvalid":false,"moveDeleteDirs":"aut
o","cleanExclude":["/home/dusty/ROMs/**/*.(txt|sh)"],"cleanDryRun":false,"zipFormat":"torrentzip","zipExclude":"","zipDatName":false,"linkMode":"symlink","symlinkRelative":false,"trimScanArchi
ves":false,"mergeRoms":"fullnonmerged","mergeDiscs":false,"excludeDisks":false,"allowExcessSets":false,"allowIncompleteSets":false,"filterLanguage":[],"filterRegion":[],"noBios":true,"onlyBios
":false,"noDevice":false,"onlyDevice":false,"noUnlicensed":false,"onlyUnlicensed":false,"onlyRetail":false,"noDebug":false,"onlyDebug":false,"noDemo":false,"onlyDemo":false,"noBeta":false,"onl
yBeta":false,"noSample":false,"onlySample":false,"noPrototype":false,"onlyPrototype":false,"noProgram":false,"onlyProgram":false,"noAftermarket":false,"onlyAftermarket":false,"noHomebrew":fals
e,"onlyHomebrew":false,"noUnverified":false,"onlyUnverified":false,"noBad":false,"onlyBad":false,"single":true,"preferVerified":false,"preferGood":false,"preferLanguage":["EN","JA"],"preferReg
ion":["USA","WORLD","EUR","JPN"],"preferRevision":"newer","preferRetail":true,"preferParent":false,"playlistExtensions":[".cue",".gdi",".mdf",".chd"],"reportOutput":"./igir_%YYYY-%MM-%DDT%HH:%
mm:%ss.csv","datThreads":2,"readerThreads":8,"writerThreads":4,"writeRetry":2,"tempDir":"/tmp/igir/20260114-105351","disableCache":false,"verbose":3,"help":false,"d":["/mnt/synology/isos_roms_
and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat"],"i":["/mnt/synology/isos_roms_and_saves/test/Sonic CD (USA).chd"],"o":"/home/dusty/test","link-mode":
"symlink","clean-exclude":["/home/dusty/ROMs/**/*.(txt|sh)"],"C":["/home/dusty/ROMs/**/*.(txt|sh)"],"no-bios":true,"s":true,"prefer-language":["EN","JA"],"l":["EN","JA"],"prefer-region":["USA"
,"WORLD","EUR","JPN"],"r":["USA","WORLD","EUR","JPN"],"prefer-revision":"newer","prefer-retail":true,"v":3,"input-checksum-min":"CRC32","input-checksum-archives":"auto","dir-letter-count":1,"d
ir-game-subdir":"multiple","fix-extension":"auto","move-delete-dirs":"auto","zip-format":"torrentzip","merge-roms":"fullnonmerged","playlist-extensions":[".cue",".gdi",".mdf",".chd"],"report-o
utput":"./igir_%YYYY-%MM-%DDT%HH:%mm:%ss.csv","dat-threads":2,"reader-threads":8,"writer-threads":4,"write-retry":2,"$0":"igir"}
[10:53:51.590] TRACE: _DATScanner: scanning DAT files
[10:53:51.607] TRACE: _DATScanner: found 1 DAT file
[10:53:51.607] TRACE: _DATScanner: enumerating DAT archives
[10:53:51.615] TRACE: _DATScanner: parsing 1 DAT file
[10:53:51.616] TRACE: _DATScanner: /mnt/synology/isos_roms_and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat: attempting to get ListXML from MAME executa
ble
[10:53:51.625] TRACE: _DATScanner: /mnt/synology/isos_roms_and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat: failed to get ListXML from MAME executable:
 exit code 2
[10:53:51.630] TRACE: _DATScanner: /mnt/synology/isos_roms_and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat: attempting to parse 1.5MiB of XML
[10:53:51.732] TRACE: _DATScanner: /mnt/synology/isos_roms_and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat: parsed XML, deserializing to DAT
[10:53:51.842] TRACE: _DATScanner: /mnt/synology/isos_roms_and_saves/dats/Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat: NaNundefined of 545 games, 545 parents pars
ed
[10:53:51.845] TRACE: _DATScanner: done scanning DAT files

 ✓ Scanning for DATs » 1 DAT found

[10:53:51.882] TRACE: _ROMScanner: scanning ROM files
[10:53:51.883] TRACE: _ROMScanner: found 1 ROM file
[10:53:51.884] WARN: _ROMScanner: /mnt/synology/isos_roms_and_saves/test/Sonic CD (USA).chd: didn't find any files in the archive
[10:53:51.888] TRACE: _ROMScanner: done scanning ROM files
[10:53:51.888] TRACE: _ROMIndexer: indexing 0 files
[10:53:51.888] TRACE: _ROMIndexer: found 0 unique files
[10:53:51.888] TRACE: _ROMIndexer: done indexing files

 ✓ Scanning for ROMs » 0 files found

[10:53:51.889] TRACE: processing 1 DAT
[10:53:51.889] TRACE: _DATParentInferrer: Sega - Mega CD & Sega CD: inferring parents for 545 games
[10:53:51.923] TRACE: _DATParentInferrer: Sega - Mega CD & Sega CD: grouped to 307 parents
[10:53:51.923] TRACE: _DATParentInferrer: done inferring parents
[10:53:51.924] TRACE: _DATMergerSplitter: Sega - Mega CD & Sega CD: merging & splitting 545 games
[10:53:51.930] TRACE: _DATMergerSplitter: Sega - Mega CD & Sega CD: merged/split to 545 games
[10:53:51.930] TRACE: _DATMergerSplitter: Sega - Mega CD & Sega CD: done merging & splitting
[10:53:51.930] TRACE: _DATDiscMerger: Sega - Mega CD & Sega CD: not merging discs
[10:53:51.930] TRACE: _DATFilter: Sega - Mega CD & Sega CD: filtering DAT
[10:53:51.934] TRACE: _DATFilter: Sega - Mega CD & Sega CD: filtered to 545/545 games (NaNundefined)
[10:53:51.934] TRACE: _DATFilter: Sega - Mega CD & Sega CD: done filtering DAT
[10:53:51.934] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: preferring DAT games
[10:53:51.934] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: 3 Ninjas Kick Back (USA) (parent): 1 game before preferring
[10:53:51.934] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: A-Rank Thunder - Tanjou-hen (Japan) (parent): 1 game before preferring
[10:53:51.934] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: A-X-101 (USA) (RE) (parent): 1 game before preferring
[10:53:51.934] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Adventures of Batman and Robin, The (USA) (parent): 2 games before preferring
[10:53:51.935] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Adventures of Willy Beamish, The (USA) (parent): 2 games before preferring
[10:53:51.936] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: After Armageddon Gaiden - Majuu Toushouden Eclipse (Japan) (parent): 1 game before preferring
[10:53:51.936] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: After Burner III (Japan) (parent): 3 games before preferring
[10:53:51.936] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: AH3 - Thunderstrike (USA) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Aisle Lord (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Alshark (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Amazing Spider-Man vs. The Kingpin, The (Europe) (parent): 3 games before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Android Assault - The Revenge of Bari-Arm (USA) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Annett Futatabi (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Aoki Ookami to Shiroki Mejika - Genchou Hishi (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Arcus I, II, III (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Arslan Senki (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: AX-101 (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Bakuden - The Unbalanced Zone (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Bari-Arm (Japan) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Batman Returns (Europe) (parent): 4 games before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Battle Fantasy (Japan) (Rev A) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Battle Frenzy (USA) (Unl) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Battlecorps (Europe) (En,Fr,De,Es) (parent): 4 games before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: BattleTech - Gray Death Legion (USA) (Unl) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: BC Racers (Europe) (En,Fr,De) (parent): 2 games before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: BC Racers (Europe) (Demo) (Green Disc) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: BC Racers (Europe) (Demo) (Yellow Disc) (parent): 1 game before preferring
[10:53:51.937] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Beast II (Europe) (parent): 2 games before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Bill Walsh College Football (USA) (parent): 2 games before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Black Hole Assault (Japan) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Blackhole Assault (Europe) (parent): 3 games before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Bloodshot (Europe) (En,Fr,De,Es) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Bouncers (USA) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Bram Stoker's Dracula (USA) (parent): 4 games before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Brutal - Paws of Fury (USA) (parent): 2 games before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Bug Blasters - The Exterminators (USA) (Unl) (Rerelease) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Burai - Yatsudama no Yuushi Densetsu (Japan) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Burning Fists - Force Striker (USA) (Unl) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Cadillacs and Dinosaurs - The Second Cataclysm (USA, Brazil) (RE) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Captain Tsubasa (Japan) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: CD Sonic the Hedgehog (Japan) (Beta) (1992-12-04) (parent): 3 games before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Championship Soccer '94 (USA) (En,Fr,De,It) (parent): 1 game before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Chuck Rock (USA) (parent): 2 games before preferring
[10:53:51.938] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Chuck Rock II - Son of Chuck (USA) (parent): 2 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Citizen X (USA) (Unl) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Cliffhanger (USA) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Cobra Command (USA) (parent): 2 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Colors of Modern Rock, The (USA) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Compton's Interactive Encyclopedia (USA) (Version 2.01R) (parent): 4 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Corpse Killer (Europe) (parent): 2 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Corpse Killer (Europe) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Corpse Killer (USA) (Sega CD 32X) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Cosmic Fantasy Stories (Japan) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Crime Patrol (USA) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Cyborg 009 (Japan) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Daihoushinden (Japan) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dark Wizard (USA) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dark Wizard - Yomigaerishi Yami no Madoushi (Japan) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Death Bringer (Japan) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Demolition Man (USA) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dennin Aleste - Nobunaga and His Ninja Force (Japan) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Detonator Orgun (Japan) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Devastator (Japan) (parent): 1 game before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Double Switch (USA) (parent): 3 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dracula Unleashed (USA) (Disc 1) (parent): 3 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dracula Unleashed (USA) (Disc 2) (parent): 3 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dragon's Lair (Japan) (En,Ja,Fr,De,It) (parent): 4 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dune (Europe) (En,Fr,De,Es,It) (parent): 2 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dungeon Explorer (USA) (parent): 2 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dungeon Master II - Skullkeep (Japan) (parent): 3 games before preferring
[10:53:51.939] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Dynamic Country Club (Japan) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Earnest Evans (Japan) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Earthworm Jim - Special Edition (Europe) (parent): 2 games before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ecco - The Tides of Time (USA) (parent): 3 games before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ecco the Dolphin (Europe) (parent): 4 games before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ecco the Dolphin CD (Japan) (Disc 1) (Ecco the Dolphin) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ecco the Dolphin CD (Japan) (Disc 2) (Ecco the Dolphin II) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Egawa Suguru no Super League CD (Japan) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: ESPN Baseball Tonight (USA) (parent): 2 games before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: ESPN National Hockey Night (USA) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: ESPN NBA Hangtime '95 (USA) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: ESPN Sunday Night NFL (USA) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Eternal Champions - Challenge from the Dark Side (USA) (parent): 5 games before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Eye of the Beholder (Japan) (parent): 3 games before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: F1 Circus CD (Japan) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Fahrenheit (Europe) (parent): 3 games before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Fahrenheit (USA) (Disc 1) (Key Disc) (Sega CD) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Fahrenheit (USA) (Disc 2) (32X CD) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Fatal Fury Special (Europe) (parent): 4 games before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: FIFA International Soccer (USA) (En,Fr,De,Es) (parent): 1 game before preferring
[10:53:51.940] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: FIFA International Soccer - Championship Edition (Europe) (En,Fr,De,Es) (parent): 3 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Final Fight CD (Japan) (parent): 6 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Flashback (Europe) (Demo) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Flashback - The Quest for Identity (USA) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Flink (Europe) (En,Fr,De,Es,Nl) (parent): 2 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Formula One World Championship - Beyond the Limit (USA) (parent): 2 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Fresh Cleaner (Japan) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Game no Kandume Vol. 1 (Japan) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Game no Kandume Vol. 2 (Japan) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Garou Densetsu Special (Japan) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Gen'ei Toshi - Illusion City (Japan) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ground Zero Texas (Europe) (Disc 1) (parent): 2 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ground Zero Texas (Europe) (Disc 2) (parent): 3 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Gyuwambler Jiko Chuushinha 2 - Gekitou! Tokyo Mahjongland-hen (Japan) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Heart of the Alien - Out of This World Parts I and II (USA) (RE) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Heavenly Symphony - Formula One World Championship 1993 (Japan) (parent): 2 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Heavy Nova (Japan) (parent): 2 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Heimdall (Japan) (parent): 2 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Hook (USA) (parent): 3 games before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: IIIrd World War, The (Japan) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Iron Helix (USA) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ishii Hisaichi no Daiseikai (Japan) (parent): 1 game before preferring
[10:53:51.941] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Jaguar XJ220 (Europe) (En,Ja) (parent): 3 games before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Jangou World Cup (Japan) (parent): 1 game before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Jeopardy! (USA) (parent): 1 game before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Joe Montana's NFL Football (USA) (parent): 1 game before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Jurassic Park (Japan) (parent): 7 games before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Kamen Rider ZO (Japan) (parent): 1 game before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Keio Flying Squadron (Europe) (parent): 3 games before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Keiou Yuugekitai (Japan) (parent): 2 games before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Kids on Site (USA) (parent): 2 games before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Lawnmower Man, The (Europe) (parent): 3 games before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Lethal Enforcers (USA) (parent): 4 games before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Lethal Enforcers II - Gun Fighters (Europe) (parent): 4 games before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Lethal Enforcers II - The Western (Japan) (parent): 1 game before preferring
[10:53:51.942] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Links - The Challenge of Golf (USA) (parent): 2 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Loadstar - The Legend of Tully Bodine (USA, Brazil) (parent): 2 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Lords of Thunder (USA) (parent): 2 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Lunar - Eternal Blue (Japan) (parent): 4 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Lunar - The Silver Star (Japan) (parent): 3 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mad Dog II - The Lost Gold (USA) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mad Dog McCree (USA) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mahou no Shoujo - Silky Lip (Japan) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Make My Video - INXS (Europe) (parent): 3 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Make My Video - Kris Kross (Europe) (parent): 2 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Make My Video - Marky Mark and the Funky Bunch (USA) (parent): 2 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mansion of Hidden Souls (USA) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Marko (USA) (Unl) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Marko's Magic Football (Europe) (En,Fr,De,Es) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mary Shelley's Frankenstein (USA) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Masked Rider, The - Kamen Rider ZO (USA) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mega Schwarzschild (Japan) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: MegaRace (USA) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mickey Mania (Europe) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mickey Mania - The Timeless Adventures of Mickey Mouse (USA) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mickey Mania (Europe) (Demo) (Mega Power, Sega Pro) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mickey Mania (Europe) (Demo) (Mega Sega) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Microcosm (Japan) (parent): 5 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Midnight Raiders (USA) (parent): 2 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Might and Magic III - Isles of Terra (Japan) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mighty Mighty Missile (USA) (Unl) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mighty Morphin Power Rangers (USA) (parent): 2 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mortal Kombat (USA) (parent): 2 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Mortal Kombat Kanzenban (Japan) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: My Paint (USA) (parent): 1 game before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: NBA Jam (Europe) (parent): 3 games before preferring
[10:53:51.943] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: NFL Football Trivia Challenge (USA) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: NFL's Greatest - San Francisco vs. Dallas 1978-1993 (USA) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: NHL '94 (USA) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: NHL Hockey '94 (Europe) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Night Striker (Japan, Korea) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Night Trap (Japan) (Demo) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Night Trap (Japan) (Disc 1) (parent): 7 games before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Night Trap (Europe) (Disc 1) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Night Trap (USA) (Disc 1) (Sega CD 32X) (RE-1) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Night Trap (Japan) (Disc 2) (parent): 6 games before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Night Trap (Europe) (Disc 2) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Night Trap (USA) (Disc 2) (Sega CD 32X) (RE-1) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ninja Warriors, The (Japan) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Nobunaga no Yabou - Haouden (Japan) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Nostalgia 1907 - In North Atlantic Sea (Japan) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Note! Color Mechanica (USA) (Unl) (parent): 2 games before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Novastorm (Europe) (parent): 3 games before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Panic! (USA) (RE) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Pier Solar and the Great Architects - The Definitive Original Soundtrack (Europe) (Disc 4) (Enhanced Soundtrack Disc) (parent): 1 
game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Pier Solar and the Great Architects Enhanced Soundtrack Disc (USA) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Pitfall - The Mayan Adventure (USA) (parent): 3 games before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Popful Mail (USA) (RE) (parent): 1 game before preferring
[10:53:51.944] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: PopfulMail (Japan) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Power Factory (Europe) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Power Monger (USA) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: PowerMonger (Europe) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Prince of Persia (Japan) (parent): 3 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Prize Fighter (Japan) (Disc 1) (parent): 4 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Prize Fighter (Japan) (Disc 2) (parent): 3 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Pro Yakyuu Super League CD (Japan) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Psychic Detective Series Vol. 3 - Aya (Japan) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Psychic Detective Series Vol. 4 - Orgel (Japan) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Psygnosis Christmas Sampler (Europe) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Puggsy (USA) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Quiz Scramble Special (Japan) (Rev B) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Quiz Tonosama no Yabou (Japan) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Racing Aces (USA) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Radical Rex (USA) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ranma 1-2 - Byakuranaika (Japan) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: RDF - Global Conflict (USA) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Record of Lodoss War (Japan) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Revenge of the Ninja (USA) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Revengers of Vengeance (USA) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Rise of the Dragon (USA) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Rise of the Dragon - A Blade Hunter Mystery (Japan) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Road Avenger (Europe) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Road Blaster FX (Japan) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Road Rash (USA) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Robo Aleste (Europe) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Samurai Shodown (Europe) (parent): 3 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: San Diego Zoo Presents... The Animals!, The (Europe) (parent): 2 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sangokushi III (Japan) (parent): 1 game before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Secret of Monkey Island, The (Japan) (parent): 3 games before preferring
[10:53:51.945] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sega CD Demo (Japan) (Proto) (1992-05-29) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sega Classic Arcade Collection - Limited Edition (Japan) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sega Classics Arcade Collection - Limited Edition (Europe) (Rev A) (parent): 2 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sega Classics Arcade Collection (USA) (4-in-1) (RE) (parent): 2 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sega Classics Arcade Collection (USA) (5-in-1) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Seima Densetsu 3x3 Eyes (Japan, Korea) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Seirei Shinseiki - Fhey Area (Japan) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sengoku Denshou (Japan) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sensible Soccer (Europe) (En,Fr,De,It) (parent): 2 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sewer Shark (Europe) (parent): 6 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Shadow of the Beast II (USA) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Shadow of the Beast II - Juushin no Jubaku (Japan) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Shadowrun (Japan) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sherlock Holmes - Consulting Detective (Europe) (parent): 2 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sherlock Holmes - Consulting Detective - Vol. II (USA) (Disc 1) (parent): 2 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sherlock Holmes - Consulting Detective - Vol. II (USA) (Disc 2) (parent): 2 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Shin Megami Tensei (Japan) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Shining Force CD (Japan) (parent): 2 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Shining Force CD (USA) (3R) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Shining Force CD (USA) (5R, 6R) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Silpheed (Japan) (parent): 5 games before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: SimEarth (Japan) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sing!! Sega Game Music Presented by B. B. Queens (Japan) (parent): 1 game before preferring
[10:53:51.946] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (Europe) (Disc 1) (Fingers) (parent): 4 games before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (Europe) (Disc 1) (Fingers) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (USA) (Disc 1) (Fingers) (Sega CD 32X) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (Europe) (Disc 2) (Juice) (parent): 2 games before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (Europe) (Disc 2) (Juice) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (USA) (Disc 2) (Juice) (Sega CD 32X) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (Europe) (Disc 3) (Mad Dog) (parent): 3 games before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (Europe) (Disc 3) (Mad Dog) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (USA) (Disc 3) (Mad Dog) (Sega CD 32X) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (USA, Brazil) (Disc 4) (Smash) (parent): 3 games before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (Europe) (Disc 4) (Smash) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Slam City with Scottie Pippen (USA) (Disc 4) (Smash) (Sega CD 32X) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Smurfs, The (Europe) (En,Fr,De,Es,It) (parent): 1 game before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Snatcher (USA) (parent): 3 games before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Software Toolworks' Star Wars Chess, The (Europe) (parent): 3 games before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sol-Feace (Japan) (parent): 5 games before preferring
[10:53:51.947] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sonic CD (Europe) (parent): 9 games before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sonic MegaMix (USA) (Unl) (parent): 1 game before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Sonic the Hedgehog CD (Japan) (parent): 4 games before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: SoulStar (Europe) (En,Fr,De) (parent): 4 games before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: SoulStar & Battlecorps (Europe) (Demo) (parent): 1 game before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Space Ace (USA) (parent): 2 games before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Space Adventure, The - Cobra - The Legendary Bandit (Europe) (parent): 2 games before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Star Wars - Rebel Assault (Japan) (parent): 4 games before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Star Wars - Rebel Assault (Europe) (Demo) (Mega Power) (parent): 1 game before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Star Wars - Rebel Assault (Europe) (Demo) (Sega Pro) (parent): 1 game before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Starblade (Japan) (parent): 3 games before preferring
[10:53:51.948] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Stellar-Fire (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Super Strike Trilogy (USA) (Unl) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Supreme Warrior (Europe) (Disc 1) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Supreme Warrior (USA) (Disc 1) (Fire & Earth) (parent): 2 games before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Supreme Warrior (USA) (Disc 1) (Fire & Earth) (Sega CD 32X) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Supreme Warrior (Europe) (Disc 1) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Supreme Warrior (Europe) (Disc 2) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Supreme Warrior (Europe) (Disc 2) (Mega-CD 32X) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Supreme Warrior (USA) (Disc 2) (Wind & Fang Tu) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Supreme Warrior (USA) (Disc 2) (Wind & Fang Tu) (Sega CD 32X) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Surgical Strike (Japan) (parent): 4 games before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Surgical Strike (Brazil) (Sega CD 32X) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Switch (Japan) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Syndicate (Europe) (En,Fr,De) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Tenbu Mega CD Special (Japan) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Tenkafubu - Eiyuutachi no Houkou (Japan) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Terminator, The (USA) (parent): 2 games before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Theme Park (Europe) (En,Fr,De,Es) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Third World War (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Thunder Storm FX (Japan) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Thunderhawk (Japan) (parent): 4 games before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Thunderhawk (Europe) (Demo) (Mega Power, Sega Pro) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Time Gal (USA) (parent): 3 games before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: TimeCop (Europe) (Demo) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Tomcat Alley (USA) (parent): 8 games before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Trivial Pursuit (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Ultraverse Prime (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Urusei Yatsura - Dear My Friends (Japan) (parent): 2 games before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Vay (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Vay - Ryuusei no Yoroi (Japan) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Wakusei Woodstock - Funky Horror Band (Japan) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Warau Salesman (Japan) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: What Is X'Eye Multi Entertainment System (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Wheel of Fortune (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Who Shot Johnny Rock (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Wild Woody (USA) (parent): 1 game before preferring
[10:53:51.949] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Wing Commander (Japan) (parent): 2 games before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Winning Post (Japan) (parent): 1 game before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: WireHead (USA) (parent): 2 games before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Wolfchild (Japan) (parent): 3 games before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Wonder Dog (Japan) (parent): 3 games before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: WonderMega Collection (Japan) (Rev 2) (parent): 1 game before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: World Cup USA '94 (USA) (En,Fr,De,Es,It,Nl,Pt,Sv) (parent): 2 games before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: WWF - Rage in the Cage (USA) (parent): 2 games before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: WWF Mania Tour - WWF - Rage in the Cage (Japan) (parent): 1 game before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Yumemi Mystery Mansion (Australia) (parent): 3 games before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Yumemi Yakata no Monogatari (Japan) (parent): 2 games before preferring
[10:53:51.950] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: Yumimi Mix (Japan) (parent): 1 game before preferring
[10:53:51.951] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: preferred to 307/545 games (NaNundefined)
[10:53:51.951] TRACE: _DATPreferer: Sega - Mega CD & Sega CD: done preferring DAT games
[10:53:51.951] TRACE: _CandidateGenerator: Sega - Mega CD & Sega CD: no input ROMs to make candidates from
[10:53:51.951] TRACE: _CandidatePatchGenerator: Sega - Mega CD & Sega CD: no candidates to make patched candidates for
[10:53:51.951] TRACE: _CandidateExtensionCorrector: Sega - Mega CD & Sega CD: no candidates to correct extensions for
[10:53:51.951] TRACE: _CandidateArchiveFileHasher: Sega - Mega CD & Sega CD: no candidates to hash ArchiveFiles for
[10:53:51.951] TRACE: _CandidatePostProcessor: Sega - Mega CD & Sega CD: no candidates to post-process
[10:53:51.951] TRACE: _CandidateValidator: Sega - Mega CD & Sega CD: no candidates to validate
[10:53:51.951] TRACE: _CandidateMergeSplitValidator: Sega - Mega CD & Sega CD: no candidates to validate merged & split ROM sets for
[10:53:51.952] TRACE: _PlaylistCreator: Sega - Mega CD & Sega CD: no candidates to create playlists for
[10:53:51.952] TRACE: _StatusGenerator: Sega - Mega CD & Sega CD: generating ROM statuses
[10:53:51.955] TRACE: _StatusGenerator: Sega - Mega CD & Sega CD: done generating ROM statuses
[10:53:51.955] TRACE: done processing 1 DAT


### DAT(s) used

Redump/Sega - Mega CD & Sega CD - Datfile (545) (2025-11-07 05-10-25).dat

### igir version

4.2.0

### Node.js version

n/a

### Operating system

Arch Linux

### Additional context

My workaround for now is to just `touch` any files that i want to re-scan without --input-checksum-quick, which updates the `updated at` file attribute.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ed47629ab82665028d440514d7be4c3a2b66ed10`.  There
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
{"case_id": "emmercm_igir__1942__ed47629",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
