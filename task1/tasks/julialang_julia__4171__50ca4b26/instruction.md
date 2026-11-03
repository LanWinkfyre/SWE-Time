# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
SegFault during build on Fedora19 (64-bit)

I've had no problems building on Fedora17/18 in the past, but now I'm getting this error on Fedora19. Am I missing something?

```
    CC ui/repl.o
    CC ui/repl-basic.o
    LINK usr/bin/julia-release-basic
    CC ui/repl-readline.o
    LINK usr/bin/julia-release-readline
osutils.jl
/bin/sh: line 1: 29536 Segmentation fault      (core dumped) /home/bs/julia/usr/bin/julia-release-readline -bf sysimg.jl
make[1]: *** [/home/bs/julia/usr/lib/julia/sys0.ji] Error 139
make: *** [release] Error 2
```

Using Linux kernel  3.10.9-200.fc19.x86_64


Here is the output at the end, where at each step of git bisect I ran `make cleanall; make USECLANG=1`:



 I also tried installing llvm and clang using apt-get, rather than using the ones I installed from source, but to no avail. Perhaps it'd be worth asking @vtjnash for potential ideas?
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `5c312fd73afd985796201d83a3f26a3835c88b2e` and the full history behind it is present.
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
