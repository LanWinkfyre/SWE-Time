# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Building: Yet another GCC vs CLANG compile problem (bisected)

**Describe the bug**
darktable, latest master, fails to build when using gcc.

```
[ 98%] Building C object bin/chart/CMakeFiles/darktable-chart.dir/deltaE.c.o
[ 98%] Building C object bin/chart/CMakeFiles/darktable-chart.dir/pfm.c.o
[ 98%] Linking C shared module libpiwigo.so
/home/jade/.local/git/darktable/src/chart/main.c: In function 'get_xyz_sample_from_image':
/home/jade/.local/git/darktable/src/chart/main.c:1534:9: error: 'delta_x_top' is predetermined 'shared' for 'shared'
   shared(corners, x_start, y_start, x_end, y_end, delta_x_top, delta_y_top, \
         ^
compilation terminated due to -Wfatal-errors.
make[2]: *** [bin/chart/CMakeFiles/darktable-chart.dir/build.make:63: bin/chart/CMakeFiles/darktable-chart.dir/main.c.o] Error 1
make[2]: *** Waiting for unfinished jobs....
```

It does build when using clang instead.

**To Reproduce**
1. Clone/Pull darktable
2. Start building process (using gcc)

**Expected behaviour**
Build cleanly.

**Bisect**



Not entirely sure about the outcome of the above bisect. Did it twice though, both came out the same.

Anyway: Pinging @TurboGit 

**Platform**

* OS                : Linux (kernel 5.9.15-1)
* Distro            : Debian Buster (rel. 10.8)
* Graphics driver   : nvidia (460.39)
* OpenCL installed  : Yes (nvidia-opencl-common 460.39-1)
* OpenCL activated  : Yes
* Xorg              : 7.7+19

**Build info**

* Compiler      : gcc 8.3.0
* Cmake         : 3.13.4
* Glib          : 2.58.3-2
* Gtk+          : 3.24.5-1
* Exiv2         : 0.27.99.0
* Sqlite        : 3.27.2
* Optimization  : None
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `b6b4928c568bd1284d09833e5d0c3e695a958c5b` and the full history behind it is present.
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
