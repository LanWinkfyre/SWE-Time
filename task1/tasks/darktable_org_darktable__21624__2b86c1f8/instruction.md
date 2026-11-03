# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
### Is there an existing issue for this?

- [x] I checked and did not find my issue in the already reported ones

### Describe the bug



### Steps to reproduce

1. either try to scroll in lighttable the thumbnails with mousewheel or go to darkroom and try to scroll wheel to zoom an image or try to scroll the filmstrip. For a moment it works but than stalls.

### Expected behavior

scrolling should work smoothly as before this commit

### Logfile | Screenshot | Screencast

bisect gave me:




### Commit



### Where did you obtain darktable from?

darktable.org / GitHub release

### darktable version



### What OS are you using?

Linux

### What is the version of your OS?

Gentoo

### Describe your system


* OS                : Linux - kernel 6.18.38-gentoo
* Distro            : Gentoo Base System release 2.18
* Processor         : Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz
* Memory            : 32 GB (4 x 8 GB) + 5GB Swap
* Graphics card0    : NVIDIA GeForce GTX 1060 6GB
* Graphics card1    : NVIDIA GeForce RTX 2070 SUPER
* Graphics driver   : nvidia-drivers-535.309.01
* OpenCL installed  : Yes (opencl-headers-2024.10.24)
* OpenCL activated  : Yes
* Xorg              : xorg-server-21.1.24
* Desktop           : KDE 6
* GTK+              : gtk+-3.24.52
* gcc               : 14.3.1_p20260604
* cflags            : CMAKE_FLAGS="-march=native-O2-mtune=native-pipe"
* CMAKE_BUILD_TYPE  : "Release"


### Are you using OpenCL GPU in darktable?

Yes

### If yes, what is the GPU card and driver?

* Graphics card0    : NVIDIA GeForce GTX 1060 6GB * Graphics card1    : NVIDIA GeForce RTX 2070 SUPER * Graphics driver   : nvidia-drivers-535.309.01

### Please provide additional context if applicable. You can attach files too, but might need to rename to .txt or .zip

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `73b039cfe145463525c1f286470f3d000563712b` and the full history behind it is present.
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
