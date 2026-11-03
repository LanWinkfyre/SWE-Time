# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
System.dat unable to be processed

### Paste the command

igir copy extract test clean --input /input/BIOS --dat "https://raw.githubusercontent.com/libretro/libretro-database/master/dat/System.dat" --output /output/bios --clean-backup /cleaned --cache-path /igir.cache

### Describe the bug

Trying to process libretro's System.dat file doesn't work, even though it's the same files (md5 is the same for both systems). No files get outputted.

```
...
comment "Magnavox - Odyssey2"
	rom ( name o2rom.bin size 1024 crc 8016A315 md5 562d5ebf9e030a40d6fabfc2f33139fd sha1 b2e1955d957a475de2411770452eff4ea19f4cee )
	rom ( name c52.bin md5 f1071cdb0b6b10dde94d3bc8a6146387 )
	rom ( name g7400.bin md5 c500ff71236068e0dc0d0603d265ae76 )
	rom ( name jopac.bin md5 279008e4a0db2dc5f1c048853b033828 )
...

	comment "Phillips - Videopac+"
	rom ( name c52.bin size 1024 crc A318E8D6 md5 f1071cdb0b6b10dde94d3bc8a6146387 sha1 a6120aed50831c9c0d95dbdf707820f601d9452e )
	rom ( name g7400.bin size 1024 crc E20A9F41 md5 c500ff71236068e0dc0d0603d265ae76 sha1 5130243429b40b01a14e1304d0394b8459a6fbae )
	rom ( name jopac.bin size 1024 crc 11647CA5 md5 279008e4a0db2dc5f1c048853b033828 sha1 54b8d2c1317628de51a85fc1c424423a986775e4 )
...
```

### Expected behavior

The /bios folder is exported correctly according to System.dat

### Debug logs

```sh
[13:55:03.182] TRACE: CandidateGenerator: System: generated 370.0MiB of 331 candidates
[13:55:03.182] TRACE: CandidateGenerator: System: done generating candidates
[13:55:03.182] TRACE: CandidatePatchGenerator: System: no patches to make patched candidates for
[13:55:03.185] TRACE: CandidateExtensionCorrector: System: no output files need their extension corrected
[13:55:03.186] TRACE: CandidateArchiveFileHasher: System: no ArchiveFiles to hash
[13:55:03.186] TRACE: CandidatePostProcessor: System: processing candidates
[13:55:03.258] TRACE: CandidatePostProcessor: System: done processing candidates
[13:55:03.259] TRACE: CandidateValidator: System: validating candidates
[13:55:03.260] ERROR: CandidateValidator: System: multiple games writing to the same output path: /output/bios/c52.bin
[13:55:03.260] ERROR: CandidateValidator:   c52
[13:55:03.260] ERROR: CandidateValidator:   c52
[13:55:03.260] ERROR: CandidateValidator: System: multiple games writing to the same output path: /output/bios/g7400.bin
[13:55:03.260] ERROR: CandidateValidator:   g7400
[13:55:03.260] ERROR: CandidateValidator:   g7400
[13:55:03.260] ERROR: CandidateValidator: System: multiple games writing to the same output path: /output/bios/jopac.bin
[13:55:03.260] ERROR: CandidateValidator:   jopac
[13:55:03.260] ERROR: CandidateValidator:   jopac
[13:55:03.261] TRACE: CandidateMergeSplitValidator: System: no candidates to validate merged & split ROM sets for
[13:55:03.262] TRACE: StatusGenerator: System: generating ROM statuses
[13:55:03.272] TRACE: StatusGenerator: System: done generating ROM statuses
[13:55:03.273] TRACE: done processing 1 DAT

```

### DAT(s) used

https://raw.githubusercontent.com/libretro/libretro-database/master/dat/System.dat

### igir version

4.0.2

### Node.js version

22

### Operating system

linux

### Additional context

System.dat is also tough because there are .zip files included and because of the duplicated files. Is there best practices for storing and exporting the System.dat file?
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `06d5cb773ef558287e730b27904ab8ee34413e3c`.  There
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
{"case_id": "emmercm_igir__1680__06d5cb7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
