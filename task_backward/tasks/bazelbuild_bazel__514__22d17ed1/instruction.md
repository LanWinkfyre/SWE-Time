# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[bisected] bazel binary crashes when invoked

Version 0.1.0 is fine, version 0.1.1 compiles without problems. Invoking the binary afterwards leads to

```
(git)-[tags/0.1.1|bisect] % ./output/bazel build scripts:bazel-complete.bash     
[1]    14607 killed     ./output/bazel build scripts:bazel-complete.bash
./output/bazel build scripts:bazel-complete.bash  1,53s user 6,32s system 98% cpu 7,983 total
```

even ./output/bazel leads to this crash.


log:



System:
Archlinux
Kernel 4.1.10-2-lts
gcc-Version 5.2.0 (GCC) 


 You can see that it is the master branch, up to October 8th, and then two commits: a cherry pick of @philwo's sandboxing fix and the release notes.  (If you look on https://github.com/bazelbuild/bazel/tree/release-0.1.2, GitHub describes the branch as 2 commits ahead, 190 commits behind master.) 

  Thus, the bug does not exist in the release and thus it did not have to be patched.

Does that make sense?
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `97eaf9136abad30827cf1a060cc32e786745923d` and the full history behind it is present.
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
