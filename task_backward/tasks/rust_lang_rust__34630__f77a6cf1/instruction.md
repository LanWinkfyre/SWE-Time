# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Nightly Compile Time Regression (06/23 to 07/01)

I noticed a pretty huge compile time regression from 


``` diff
- time: 7.904; rss: 120MB   expansion
+ time: 84.063; rss: 121MB  expansion
```

Compiling the same project, results in a pretty big increase in expansion time.
I could notice similar (**about 11x**) slow-downs on my windows installation and
reproduced it on a fresh ubuntu.

**All instructions used can be found here**: https://gist.github.com/steffengy/ab3660ec9d6eecb0fc38e7d536d9e7ef
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `da099c2322c63144831f8585dee461e3a02e339a` and the full history behind it is present.
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
