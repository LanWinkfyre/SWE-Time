# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
[MAME] ERROR: multiple games writing to the same output path:

### Paste the command

[Igir v5.0.2](https://github.com/emmercm/igir/releases/download/v5.0.2/igir-5.0.2-Linux-amd64.tar.gz)
```
$ igir move report test zip \
 --temp-dir "$HOME/.local/share/igir/temp/" \
 --cache-path "$HOME/.local/share/igir/cache/igir.cache" \
 --merge-roms fullnonmerged \
 --overwrite-invalid \
 --zip-format torrentzip \
 --input-checksum-quick \
 --input-checksum-archives never \
 --dat "$HOME/mame0288.xml" \
 --input "/path/to/input/rompack_A/" \
 --input "/path/to/input/rompack_B/" \
 --output "/path/to/romsets/MAME (fallback)/roms/" \
 --verbose
```

### Describe the bug

```
✓ Scanning for ROMs » 383,135 files found

ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-jjk-3
ERROR:   jojo
ERROR:   jojoa
ERROR:   jojoj
ERROR:   jojou
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-jjk-2
ERROR:   jojoar1
ERROR:   jojojr1
ERROR:   jojor1
ERROR:   jojour1
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-jjk000
ERROR:   jojoar2
ERROR:   jojojr2
ERROR:   jojor2
ERROR:   jojour2
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-jjm-1
ERROR:   jojobajr1
ERROR:   jojobar1
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-jjm-0
ERROR:   jojobajr2
ERROR:   jojobar2
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-wzd-5
ERROR:   redearth
ERROR:   warzard
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-wzd-3
ERROR:   redearthr1
ERROR:   warzardr1
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-sf3-3
ERROR:   sfiii
ERROR:   sfiiia
ERROR:   sfiiih
ERROR:   sfiiij
ERROR:   sfiiiu
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-3ga000
ERROR:   sfiii2
ERROR:   sfiii2h
ERROR:   sfiii2j
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-33s-2
ERROR:   sfiii3
ERROR:   sfiii3j
ERROR:   sfiii3u
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/cap-33s-1
ERROR:   sfiii3jr1
ERROR:   sfiii3r1
ERROR:   sfiii3ur1
ERROR: 0.288 (mame0288): multiple games writing to the same output path: /path/to/romsets/MAME (fallback)/roms/uarctict
ERROR:   ultarctc
ERROR:   ultarctcup
```



### Expected behavior

In MAME each *setname* is unique, different, so - when dealing with MAME's *set*s which have `.chd` file - each *setname*'s folder should contains its `.chd` files (one or more, according to MAME's DAT `.xml`).  
  

I tried adding `--dir-game-subdir always`: the error is gone, but now **every** *set* is inside its own *setname*'s subfolder, even the `.zip`-only sets!! 😅
  
  
Here's a quick example of the wanted\expected layout for a `fullnonmerged` MAME romset:  
  
  
```
A=archive
C=chd
F=folder
N=setname
O=romof
P=parent
S=clone
Y=root
_=placeholder



FY_: mame/

NP_:  machine name="redearth"
AP_:  redearth.zip
FP_:  redearth/
CP_:   cap-wzd-5

NOS:  machine name="warzard"
AOS:  warzard.zip
FOS:  warzard/
COS:   cap-wzd-5

NOS:  machine name="redearthr1"
AOS:  redearthr1.zip
FOS:  redearthr1/
COS:   cap-wzd-3

NOS:  machine name="warzardr1"
AOS:  warzardr1.zip
FOS:  warzardr1/
COS:   cap-wzd-3
```
  
  

### Debug log

[igir_debug_log.zip](https://github.com/user-attachments/files/28445876/igir_debug_log.zip)

### DAT(s) used

https://github.com/mamedev/mame/releases/download/mame0288/mame0288lx.zip

### igir version

5.0.2

### Node.js version

none

### Operating system

*Linux (latest tests were done on *Arch Linux*)

### Additional context

Maybe that's what *Igir* is expected to do, when declaring `--merge-roms fullnonmerged` ?
But... I don't feel it should work like that! 🤪 😁
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5c47d3de0f00e650a507a722a8838b189c5518e5`.  There
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
{"case_id": "emmercm_igir__2271__5c47d3d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
