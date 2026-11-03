# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Build fails with `./configure --enable-shared --disable-static` on Windows



### I did this

```bash
# using gcc/clang + mingw-w64
autoreconf -vfi
./configure --enable-shared --disable-static --with-schannel
make -j
```

```bash
libtool: compile:  windres -I../include -DCURL_EMBED_MANIFEST -i curl.rc  -DDLL_EXPORT -DPIC -o .libs/curl.o
  CCLD     curl.exe
C:/msys64/ucrt64/bin/../lib/gcc/x86_64-w64-mingw32/12.2.0/../../../../x86_64-w64-mingw32/bin/ld.exe: cannot find curl.o: No such file or directory
collect2.exe: error: ld returned 1 exit status
```





### I expected the following

it to build

### curl/libcurl version

7.86.0

### operating system

Windows 11
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `811c799f2db1bbcf22e7ceee1e8c2c21525274de` and the full history behind it is present.
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
