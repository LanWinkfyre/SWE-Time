# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Crash with Segmentation fault in ClassDefImpl::mergeMembers

**Describe the bug**
The creation of the `VHDL` documentation of the [w11 project](https://github.com/wfjm/w11) crashes for 1.9.2 and 1.9.3 with
```
.....
Creating members for template instances...
Building page list...
Search for main page...
Computing page relations...
Determining the scope of groups...
Sorting lists...
Determining which enums are documented
Computing member relations...
Building full member lists recursively...
Segmentation fault (core dumped)
```
More details are described under _Stack Trace_.

**Expected behavior**
Works fine with 1.9.1 and previous versions

**To Reproduce**
The `VHDL` source tree is in [w11 project](https://github.com/wfjm/w11).  
The `Doxyfile` is attached.  
A full reproducer script can be provided upon request. 

**Version**
Using Ubuntu 2020.04 LTS. Both 1.9.2 and 1.9.3 crash. 1.9.1 works.

**Stack trace**
I've build 1.9.2 with debug
```
git checkout tags/Release_1_9_2
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Debug -G "Unix Makefiles" ..
```
and got the backtrace
```
#0  0x0000557d3ad3d390 in ClassDefImpl::mergeMembers (this=0x557d521fd100)
      at /mnt/data/opt/github/doxygen/src/classdef.cpp:3441
#1  0x0000557d3a7cd61c in buildCompleteMemberLists ()
      at /mnt/data/opt/github/doxygen/src/doxygen.cpp:7772
#2  0x0000557d3a7e4b8c in parseInput ()
      at /mnt/data/opt/github/doxygen/src/doxygen.cpp:11739
#3  0x0000557d3a79c5b1 in main (argc=2, argv=0x7ffd7a959578)
      at /mnt/data/opt/github/doxygen/src/main.cpp:37
```
The code around `classdef.cpp:3441` is
```
    3439        const ClassDef *dstCd = dstMd->getClassDef();
    3440        /...
    3441        if (srcCd==dstCd || dstCd->isBaseClass(srcCd,TRUE))
```
An `info locals` gives
```
dstCd = 0x0
srcCd = 0x557d50f138f8
```
The problems is that
- `srcCd` is not equal `dstCd`
- that's why `dstCd->isBaseClass(srcCd,TRUE)` is executed
- dstCd is `nullptr` --> **Segmentation fault**

**Additional context**
The `Doxyfile` (with .txt suffix added) and the output of `info local` are attached.
[w11_vhd_all.Doxyfile.txt](https://github.com/doxygen/doxygen/files/8355222/w11_vhd_all.Doxyfile.txt)
[doxy_crash_info_local.txt](https://github.com/doxygen/doxygen/files/8355223/doxy_crash_info_local.txt)



A git bisect gave me:


@doxygen how to proceed?
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `91095fb62f0bc2c624b0e8e49d9316f51be76559` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
