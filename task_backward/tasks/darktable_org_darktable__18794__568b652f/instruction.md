# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Git master : Compile error : error: ‘_get_cache_filename’ defined but not used [-Werror=unused-function]

### Is there an existing issue for this?

- [x] I checked and did not find my issue in the already reported ones

### Describe the bug

When I compile git master I get this compilation error:
```c
In file included from /home/magnus/test/darktable-test/darktable/build/lib/darktable/plugins/introspection_lut3d.c:50:
/home/magnus/test/darktable-test/darktable/src/iop/lut3d.c:452:13: error: ‘_get_cache_filename’ defined but not used [-Werror=unused-function]
  452 | static void _get_cache_filename(const char *const lutname, char *const cache_filename)
      |             ^~~~~~~~~~~~~~~~~~~
compilation terminated due to -Wfatal-errors.
cc1: all warnings being treated as errors
make[2]: *** [lib/darktable/plugins/CMakeFiles/lut3d.dir/build.make:82: lib/darktable/plugins/CMakeFiles/lut3d.dir/introspection_lut3d.c.o] Error 1
make[1]: *** [CMakeFiles/Makefile2:6548: lib/darktable/plugins/CMakeFiles/lut3d.dir/all] Error 2
``` 

### Steps to reproduce

1. Checkout git master. Cd darktable.
2. cmake -DCMAKE_INSTALL_PREFIX=/home/magnus/test/darktable-test/install -DCMAKE_BUILD_TYPE=Release ..
3. make -j32
```c
In file included from /home/magnus/test/darktable-test/darktable/build/lib/darktable/plugins/introspection_lut3d.c:50:
/home/magnus/test/darktable-test/darktable/src/iop/lut3d.c:452:13: error: ‘_get_cache_filename’ defined but not used [-Werror=unused-function]
  452 | static void _get_cache_filename(const char *const lutname, char *const cache_filename)
      |             ^~~~~~~~~~~~~~~~~~~
compilation terminated due to -Wfatal-errors.
cc1: all warnings being treated as errors
make[2]: *** [lib/darktable/plugins/CMakeFiles/lut3d.dir/build.make:82: lib/darktable/plugins/CMakeFiles/lut3d.dir/introspection_lut3d.c.o] Error 1
make[1]: *** [CMakeFiles/Makefile2:6548: lib/darktable/plugins/CMakeFiles/lut3d.dir/all] Error 2
``` 



### Expected behavior

Sucessful build

### Logfile | Screenshot | Screencast

Git bisect result:



### Commit



### Where did you obtain darktable from?

Self compiled.

### darktable version



### What OS are you using?

Linux

### What is the version of your OS?

Debian stable 12.10 Bookworm

### Describe your system

Debian stable 12.10 Bookworm
gcc version 12.2.0 (Debian 12.2.0-14)

### Are you using OpenCL GPU in darktable?

Yes

### If yes, what is the GPU card and driver?

No relevent here.

### Please provide additional context if applicable. You can attach files too, but might need to rename to .txt or .zip

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `11f26a81c48bd3f38f65a4b6819b3aaf02ee6f71` and the full history behind it is present.
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
