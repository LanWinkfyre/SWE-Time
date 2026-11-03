# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
HLR green artifacts with OpenCL

I just recompiled master this morning (Feb 13) and noticed that HLR inpaint-opposed and segmented are giving me subtle green artifacts on lots of photos that I don't remember having such artifacts before. I compile dt from master pretty frequently so I'm positive this is a fairly recent change (probably within the last week or two). The problem seems to  disappear with opencl disabled.

This is a pristine image with only dt's default initial processing (and opencl enabled)
![hlr_green](https://user-images.githubusercontent.com/10678620/218550148-01675bb1-27bd-49fc-b9cc-7f9cad32ee8e.png)



copyright (c) 2009-2023 johannes hanika
https://github.com/darktable-org/darktable/issues/new/choose

compile options:
  bit depth is 64 bit
  normal build
  SSE2 optimized codepath enabled
  OpenMP support enabled
  OpenCL support enabled
  Lua support enabled, API version 9.0.0
  Colord support enabled
  gPhoto2 support enabled
  GraphicsMagick support enabled
  ImageMagick support disabled
  libavif support enabled
  libheif support enabled
  libjxl support enabled
  OpenJPEG support enabled
  OpenEXR support enabled
  WebP support enabled

* OS                : Archlinux (up-to-date)
* Graphics card     : Intel 530
* OpenCL installed  :  NEO
* OpenCL activated  : yes


Could you share the raw file please?
Any chance you updated the CL driver recently?

I can share a similar file that exhibits the same issue (and to much more severe degree). Where would be the best place to share? About 30MB (which exceeds the 25MB file size limit on github).

The last update to intel opencl packages was back on Jan 18, 2023. It is possible that this opencl update could be responsible. However, when I try downgrading opencl packages to test, I keep getting a segfault inside intel-opencl-runtime. However, when downgrading darktable to a previously compiled package made in early Feb, I get the same green artifacts with the newer opencl runtime.

Just any sharing service to pick from is fine.

Here is a google drive link:
https://drive.google.com/file/d/1KeWA0TSWtj5bfpBwcIal0m_ejNHCJpBM/view?usp=share_link

Included in the file are the raw and an exported jpg.

This was the latest update to intel opencl packages

```
89806:[2023-01-18T10:22:35-0600] [ALPM] upgraded intel-opencl-clang (14.0.0.r3+g5dd5031-1 -> 15.0.0-1)
89807:[2023-01-18T10:22:36-0600] [ALPM] upgraded intel-graphics-compiler (1:1.0.11485-8 -> 1:1.0.12812.4-1)
89808:[2023-01-18T10:22:36-0600] [ALPM] upgraded intel-compute-runtime (22.30.23789-1 -> 22.43.24595.30-1)
```



Some of the interesting commits during bisect.
 I see this as a good commit.

 Strange purple artifacts.

 Purple is gone and green artifacts are there.
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `4be1794967b781942a8bb3abf3b1cd331bddbed4` and the full history behind it is present.
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
