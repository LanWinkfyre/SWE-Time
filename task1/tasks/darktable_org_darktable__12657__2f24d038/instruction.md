# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
top view: rating filter overlaps the operator

**Did you buy darktable from an application store ?**
No

**Describe the bug/issue**
The rating filter on top of main view is crippled. The stars are overlapping the operator, such like = or >

If I chose language DE, the operator is even totally invisible...

**To Reproduce**
See screenshot "bad example"

**Expected behavior**
See screenshot "good example"

**Screenshots**
bad example:
![Screenshot_20221017_210429](https://user-images.githubusercontent.com/49004103/196265467-a6946c13-3a35-4cea-8711-9bf634b1a572.png)

good example:
![Screenshot_20221017_213222](https://user-images.githubusercontent.com/49004103/196266210-7d0e38de-f437-4712-b060-f05890758cd8.png)


**Which commit introduced the error**
_If possible, please try using `git bisect` to determine which commit introduced the issue and place the result here._

Bisect gave me (I did two runs with same result):

@dterrahe  may I ping you here?

**Platform**
_Please fill as much information as possible in the list given below. Please state "unknown" where you do not know the answer and remove any sections that are not applicable _


* OS                : Linux - kernel 5.19.12-gentoo
* Distro            : Gentoo Base System release 2.8
* Processor         : Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz
* Memory            : 32 GB (4 x 8 GB) + 5GB Swap
* Graphics card0    : NVIDIA GeForce GTX 1060 6GB
* Graphics card1    : NVIDIA GeForce RTX 2070 SUPER
* Graphics driver   : nvidia-drivers-520.56.06
* OpenCL installed  : Yes (opencl-headers-2022.01.04)
* OpenCL activated  : Yes
* Xorg              : xorg-server-21.1.4
* Desktop           : KDE 5
* GTK+              : gtk+-3.24.34-r1
* gcc               : x86_64-pc-linux-gnu-11.3.0
* cflags            : CMAKE_FLAGS="-march=native-O2-mtune=native-pipe"
* CMAKE_BUILD_TYPE  : "Release"

**Additional context**
_Please provide any additional information you think may be useful, for example:_

 - Is the issue still present using an empty/new config-dir (e.g. start darktable with --configdir "/tmp")? **yes**
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `afb0ac5c003544bfa239ecaf6f93b0cc7d82e171` and the full history behind it is present.
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
