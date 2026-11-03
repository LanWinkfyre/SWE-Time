# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
[TOSEC;Sega Dreamcast - Games - Dev Builds - [ISO] (TOSEC-v2025-01-18)] `.iso: failed to parse file: FILE_ENDED`

### Paste the command

```
$ igir report --dat /path/to/dreamcast/indices/tosec/*.dat --input /path/to/dreamcast/contents/tosec/ --input-checksum-min SHA1 --input-checksum-max SHA1
```

Version: https://github.com/emmercm/igir/releases/download/v3.3.1/igir-3.3.1-Linux-amd64.tar.gz

### Describe the bug

```
ERROR: /path/to/dreamcast/contents/tosec/Sega Dreamcast - Games - Dev Builds - [ISO] (TOSEC-v2025-01-18)/Slave Zero v0.800 (1999-08-14)(Infogrames - Sega)(NTSC-PAL)(alpha)[GD-R]/track05.iso: failed to parse file: FILE_ENDED
ERROR: /path/to/dreamcast/contents/tosec/Sega Dreamcast - Games - Dev Builds - [ISO] (TOSEC-v2025-01-18)/Slave Zero v0.800 (1999-11-22)(Infogrames)(NTSC-PAL)(M5)(beta)[GD-R, Review Copy 5.51 8-12-99 label]/track05.iso: failed to
 parse file: FILE_ENDED
```

### Expected behavior

parsing these two **specific** `.iso` files

### Debug logs

```
[13:02:16.357] ERROR: ROMScanner: /path/to/dreamcast/contents/tosec/Sega Dreamcast - Games - Dev Builds - [ISO] (TOSEC-v2025-01-18)/Slave Zero v0.800 (1999-08-14)(Infogrames - Sega)(NTSC-PAL)(alpha)[GD-R]/track05.iso: failed to parse file: FILE_ENDED
[13:02:16.397] ERROR: ROMScanner: /path/to/dreamcast/contents/tosec/Sega Dreamcast - Games - Dev Builds - [ISO] (TOSEC-v2025-01-18)/Slave Zero v0.800 (1999-11-22)(Infogrames)(NTSC-PAL)(M5)(beta)[GD-R, Review Copy 5.51 8-12-99 label]/track05.iso: failed to parse file: FILE_ENDED
[13:03:41.923] TRACE: CandidateGenerator: Sega Dreamcast - Games - Dev Builds - [ISO]: Slave Zero v0.800 (1999-08-14)(Infogrames - Sega)(NTSC-PAL)(alpha)[GD-R]: found 5 files, missing 1 file
[13:03:41.923] TRACE: CandidateGenerator: Sega Dreamcast - Games - Dev Builds - [ISO]: Slave Zero v0.800 (1999-11-22)(Infogrames)(NTSC-PAL)(M5)(beta)[GD-R, Review Copy 5.51 8-12-99 label]: found 5 files, missing 1 file
```

</br>

```
[13:03:40.629] TRACE: DATParentInferrer: Sega Dreamcast - Games - Dev Builds - [ISO]: inferring parents for 56 games
[13:03:40.636] TRACE: DATParentInferrer: Sega Dreamcast - Games - Dev Builds - [ISO]: grouped to 56 parents
[13:03:40.636] TRACE: DATMergerSplitter: Sega Dreamcast - Games - Dev Builds - [ISO]: DAT doesn't have parent/clone info, doing nothing
[13:03:40.636] TRACE: DATDiscMerger: Sega Dreamcast - Games - Dev Builds - [ISO]: not merging discs
[13:03:40.636] TRACE: DATFilter: Sega Dreamcast - Games - Dev Builds - [ISO]: filtering DAT
[13:03:40.637] TRACE: DATFilter: Sega Dreamcast - Games - Dev Builds - [ISO]: filtered to 56/56 games (54.5GB)
[13:03:40.637] TRACE: DATFilter: Sega Dreamcast - Games - Dev Builds - [ISO]: done filtering DAT
[13:03:40.637] TRACE: DATPreferer: Sega Dreamcast - Games - Dev Builds - [ISO]: not running in single/1G1R mode, not preferring games
[13:03:40.637] TRACE: CandidateGenerator: Sega Dreamcast - Games - Dev Builds - [ISO]: generating candidates
```

</br>

```
[13:03:42.191] TRACE: CandidateGenerator: Sega Dreamcast - Games - Dev Builds - [ISO]: generated 52.6GB of 54 candidates
[13:03:42.191] TRACE: CandidateGenerator: Sega Dreamcast - Games - Dev Builds - [ISO]: done generating candidates
[13:03:42.192] TRACE: CandidatePatchGenerator: Sega Dreamcast - Games - Dev Builds - [ISO]: no patches to make patched candidates for
[13:03:42.193] TRACE: CandidateExtensionCorrector: Sega Dreamcast - Games - Dev Builds - [ISO]: no output files need their extension corrected
[13:03:42.193] TRACE: CandidateArchiveFileHasher: Sega Dreamcast - Games - Dev Builds - [ISO]: not testing or overwriting invalid files, no need
[13:03:42.193] TRACE: CandidatePostProcessor: Sega Dreamcast - Games - Dev Builds - [ISO]: processing candidates
[13:03:42.362] TRACE: CandidatePostProcessor: Sega Dreamcast - Games - Dev Builds - [ISO]: done processing candidates
[13:03:42.363] TRACE: CandidateValidator: Sega Dreamcast - Games - Dev Builds - [ISO]: validating candidates
[13:03:42.370] TRACE: CandidateValidator: Sega Dreamcast - Games - Dev Builds - [ISO]: done validating candidates
[13:03:42.371] TRACE: CandidateMergeSplitValidator: Sega Dreamcast - Games - Dev Builds - [ISO]: validating merged & split ROM sets
[13:03:42.376] TRACE: CandidateMergeSplitValidator: Sega Dreamcast - Games - Dev Builds - [ISO]: done validating merged & split ROM sets
[13:03:42.400] TRACE: StatusGenerator: Sega Dreamcast - Games - Dev Builds - [ISO]: generating ROM statuses
[13:03:42.401] TRACE: StatusGenerator: Sega Dreamcast - Games - Dev Builds - [ISO]: done generating ROM statuses
```

### DAT(s) used

https://www.tosecdev.org/downloads/category/59-2025-03-13?download=117:tosec-dat-pack-complete-4743-tosec-v2025-03-13

### igir version

3.3.1

### Node.js version

N/A

### Operating system

ArchLinux

### Additional context

```
$ grep $(sha1sum Slave\ Zero\ v0.800\ \(1999-08-14\)\(Infogrames\ -\ Sega\)\(NTSC-PAL\)\(alpha\)\[GD-R\]/track05.iso | cut -d' ' -f1) '/path/to/dreamcast/indices/Sega Dreamcast - Games - Dev Builds - [ISO] (TOSEC-v2025-01-18_CM).dat'
	<rom name="track05.iso" size="212600832" crc="30609ca8" md5="9069d5768e072425f8a446d67f8d9ff7" sha1="4b0cc43ccd6393b31224a83d02473dfcb8aef292"/>
```

```
$ grep $(sha1sum Slave\ Zero\ v0.800\ \(1999-11-22\)\(Infogrames\)\(NTSC-PAL\)\(M5\)\(beta\)\[GD-R\,\ Review\ Copy\ 5.51\ 8-12-99\ label\]/track05.iso | cut -d' ' -f1) '/path/to/dreamcast/indices/Sega Dreamcast - Games - Dev Builds - [ISO] (TOSEC-v2025-01-18_CM).dat'
	<rom name="track05.iso" size="423278592" crc="98958718" sha1="b0bc2b2812e462e659f006282a3f2aaacb1f5c36" md5="666b450dac04823c4ae6395ad35825af"/>
```


</br>


Perhaps these two **specific** `.iso` files were created incorrectly or had some internal quirk, I don't know.
In any case, I still decided to report this bug (?) because of the fact that their *sha1* fingerprint is indeed calculated correctly (see above), and also because other auditing tools parse said files without problems, reporting them as valid.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3fea6e2fe47e6cce5564cd7b4125accf9d13e9bc`.  There
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
{"case_id": "emmercm_igir__1544__3fea6e2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
