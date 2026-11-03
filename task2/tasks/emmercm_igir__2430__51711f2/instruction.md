# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
scanner copying correct files to output folder but reports showing the games as missing and unused

### Paste the command

igir report --dat /run/media/hkr/Games/rom management/dats/UGA_RA_DATs/DATs/RetroAchievements (No Subfolders)//RA - Arcade.dat -i /run/media/hkr/media/roms//Arcade/RetroAchievements --report-output /run/media/hkr/Games/rom management/reports//RA - Arcade.csv --temp-dir /run/media/hkr/Games/rom management/temp/ --cache-path arcade.cache --debug-log


### Describe the bug

When building a romset using the retroachievement arcade dats, igir will scan the input folders and correctly copy 100% of the roms identified in the dat into the output directory, but report 9 missing games. Then, when a report is built against the output directory, it reports 9 games missing, but all 9 games and their files are marked as unused. The file hashes match the dat. For example, azumanga.zip is in the dat as:

> <game name="azumanga">

>		<category>Retail</category>
>		<source>mamesl</source>
>		<description>Azumanga Daioh Puzzle Bobble (GDL-0018)</description>
>		<release name="azumanga" region="World"/>
>		<year>2002</year>
>		<manufacturer>MOSS (Taito license)</manufacturer>
>		<biosset name="bios0" description="epr-21576e (Japan)"/>
>		<biosset name="bios1" description="epr-21576g (Japan)"/>
>		<biosset name="bios2" description="epr-21576h (Japan)"/>
>		<biosset name="bios3" description="epr-21578h (Export)"/>
>		<biosset name="bios4" description="epr-21578g (Export)"/>
>		<biosset name="bios5" description="epr-21578e (Export)"/>
>		<biosset name="bios6" description="epr-21577h (USA)"/>
>		<biosset name="bios7" description="epr-21577g (USA)"/>
>		<biosset name="bios8" description="epr-21577e (USA)"/>
>		<rom name="317-5091-jpn.pic" size="16384" crc="b71ede16" sha1="0c27f335d4b81b0413301477813651c4cbba9981"/>
>		<rom name="epr-21576e.ic27" size="2097152" crc="08c0add7" sha1="e7c1a7673cb2ccb21748ef44105e46d1bad7266d"/>
>		<rom name="epr-21576g.ic27" size="2097152" crc="d2a1c6bf" sha1="6d27d71aec4dfba98f66316ae74a1426d567698a"/>
>		<rom name="epr-21576h.ic27" size="2097152" crc="d4895685" sha1="91424d481ff99a8d3f4c45cea6d3f0eada049a6d"/>
>		<rom name="epr-21577e.ic27" size="2097152" crc="cf36e97b" sha1="b085305982e7572e58b03a9d35f17ae319c3bbc6"/>
>		<rom name="epr-21577g.ic27" size="2097152" crc="25f64af7" sha1="99f9e6cc0642319bd2da492611220540add573e8"/>
>		<rom name="epr-21577h.ic27" size="2097152" crc="fdf17452" sha1="5f3e4b677f0046ce690a4f096b0481e5dd8bb6e6"/>
>		<rom name="epr-21578e.ic27" size="2097152" crc="087f09a3" sha1="0418eb2cf9766f0b1b874a4e92528779e22c0a4a"/>
>		<rom name="epr-21578g.ic27" size="2097152" crc="55413214" sha1="bd2748365a9fc1821c9369aa7155d7c41c4df43e"/>
>		<rom name="epr-21578h.ic27" size="2097152" crc="7b452946" sha1="8e9f153bbada24b37066dc45b64a7bf0d4f26a9b"/>
>		<rom name="main_eeprom.bin" size="128" crc="fea29cbb" sha1="4099f1747aafa07db34f6e072cd9bfaa83bae10e"/>
>		<rom name="x76f100_eeprom.bin" size="132" crc="3ea24b6a" sha1="3a730ebcf56e0060fef6b1b02eb2eb7cfb7e61dc"/>
>		<disk name="gdl-0018" sha1="749a56dd64ab697f17470d8ae797f7e20e9eb646" region="gdrom"/>
>		<device_ref name="sh7091"/>
>		<device_ref name="timer"/>
>		<device_ref name="dc_g2if"/>
>		<device_ref name="arm7_le"/>
>		<device_ref name="maple_dc"/>
>		<device_ref name="screen"/>
>		<device_ref name="powervr2"/>
>		<device_ref name="speaker"/>
>		<device_ref name="aica"/>
>		<device_ref name="aicartc"/>
>		<device_ref name="93c46_16"/>
>		<device_ref name="mie"/>
>		<device_ref name="z80"/>
>		<device_ref name="mie_jvs"/>
>		<device_ref name="jvs13551"/>
>		<device_ref name="tmp90ph44"/>
>		<device_ref name="93c46_8"/>
>		<device_ref name="x76f100"/>
>		<device_ref name="m3comm"/>
>		<device_ref name="m68000"/>
>		<device_ref name="ram"/>
>		<device_ref name="nvram"/>
>		<device_ref name="segadimm"/>
>		<device_ref name="sh7091"/>
>		<device_ref name="pci_root"/>
>		<device_ref name="sega315_6154"/>
>		<device_ref name="ide_gdrom"/>
>		<device_ref name="idectrl32bm"/>
>		<device_ref name="ata_slot"/>
>		<device_ref name="gdrom"/>
>		<device_ref name="gdrom_image"/>
>		<device_ref name="cdda"/>
>		<device_ref name="ata_slot"/>
>		<device_ref name="pic16c622"/>
>		<device_ref name="24c01"/>
>		<device_ref name="24c01"/>
>		<device_ref name="93c46_8"/>
>		<driver status="preliminary"/>
>		<ra_hash>6274e432cf34c2164e9ffe997ffa14c8</ra_hash>
>		<url>https://retroachievements.org/game/24395/hashes</url>
>	</game>

The contents of the zip match with the correct crc and sha1 hashes.

When running igir with the debug command, it reports the following when scanning azumanga.zip:

>[18:12:21.201] TRACE: CandidateGenerator: RA - Arcade: azumanga: cannot use '/run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip' as an input file, it has the excess entries:
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21576e.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21576g.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21576h.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21577e.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21577g.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21577h.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21578e.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21578g.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|epr-21578h.ic27
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|main_eeprom.bin
>[18:12:21.201] TRACE: CandidateGenerator:   /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip|x76f100_eeprom.bin

As far as I can tell, the scanner thinks the file `317-5091-jpn.pic` is the excess file, despite it being defined in the dat `<rom name="317-5091-jpn.pic" size="16384" crc="b71ede16" `



### Expected behavior

Since at some point igir correctly identified that the files matched the dat and copied them to the output folder, the report should show that the files are found instead of missing or unused.

### Debug log

[igir_2026-08-17T18;12;15.log](https://github.com/user-attachments/files/31162076/igir_2026-08-17T18.12.15.log)

### DAT(s) used

https://github.com/UltraGodAzgorath/UGA_RA_DATs/blob/main/DATs/RetroAchievements%20(No%20Subfolders)/RA%20-%20Arcade.dat

### Additional context

The list of files not found:




RA - Arcade | azumanga | MISSING |  
-- | -- | -- | --
RA - Arcade | beachspi | MISSING |  
RA - Arcade | cvs2 | MISSING |  
RA - Arcade | ggxxac | MISSING |  
RA - Arcade | ggxxsla | MISSING |  
RA - Arcade | initdv2e | MISSING |  
RA - Arcade | initdv3e | MISSING |  
RA - Arcade | monkeyba | MISSING |  
RA - Arcade | progear | MISSING |  
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga.zip
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/azumanga/gdl-0018.chd
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/beachspi.zip
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/beachspi/gds-0014.chd
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/cvs2.zip
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/cvs2/gdl-0008.chd
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/ggxxac.zip
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/ggxxac/gdl-0041.chd
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/ggxxsla.zip
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/ggxxsla/gdl-0033a.chd
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/initdv2e.zip
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/initdv2e/gds-0027.chd
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/initdv3e.zip
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/initdv3e/gds-0033.chd
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/monkeyba.zip
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/monkeyba/gds-0008.chd
  |   | UNUSED | /run/media/hkr/media/roms/Arcade/RetroAchievements/progear.zip


</body>
</html>
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `51711f29b7671299095607201dfbbb43b0efd5cc`.  There
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
{"case_id": "emmercm_igir__2430__51711f2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
