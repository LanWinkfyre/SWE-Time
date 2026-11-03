# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[masks] drawn mask, path cannot be removed anymore and also opacity says 0% where it is actually 100%

**Describe the bug/issue**
Current Master:
An applied drawn path cannot be removed anymore with right mouse click. At the same time, the mask opacity in Toas Message says 0% where actually it is 100%

[edit] not only path is affected, also gradient, I assume all...

**To Reproduce**
_Please amend or remove, what is/isn't applicable_
1. Go to Exposure
2. Create a drawn path and 
3. make mask indicator visible
4. Try to adjust opacity by ctrl+scroll and try to remove the mask with right click
5. see error

**Expected behavior**
former behaviour e.g. of 3.4.0

**Screenshots**
![Screenshot_20210110_224349](https://user-images.githubusercontent.com/49004103/104136754-5fa95780-5398-11eb-81ab-6e1624069400.png)

**Which commit intruduced the error**

@da-phil may I ping you here!?

**Platform**

* OS                : Linux - kernel 5.10.2-gentoo
* Distro            : Gentoo Base System release 2.7
* Processor         : Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz
* Memory            : 32 GB (4 x 8 GB) + 5GB Swap
* Graphics card0    : GeForce GTX 1060 6GB
* Graphics card1    : GeForce RTX 2070 SUPER
* Graphics driver   : nvidia-drivers-460.27.04
* OpenCL installed  : Yes (opencl-headers-2020.06.16)
* OpenCL activated  : Yes
* Xorg              : xorg-server-1.20.10
* Desktop           : KDE 5
* GTK+              : gtk+-3.24.22
* gcc               : x86_64-pc-linux-gnu-9.3.0
* cflags            : CMAKE_FLAGS="-march=native-O2-mtune=native-pipe"
* CMAKE_BUILD_TYPE  : "RelWithDebInfo"     

**Additional context**
 - Can you reproduce with another Darktable version(s)? **bisected, so several versions**
 - Can you reproduce with a RAW or Jpeg or both? **RAW**
 - Is the issue still present using an empty/new config-dir (e.g. start darktable with --configdir "/tmp")? **yes**
 - [edit] opencl on/off does not matter
 - (edit] complete empty history stack does not matter
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `54e7e09eb172aa76faa870afbf238c45d7b77b96` and the full history behind it is present.
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
