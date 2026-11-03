# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Half-page scrolling does not scroll when a single line fills the entire window

### Steps to reproduce

1. Open Vim 9.1.0404 to a buffer where the first line is 10000 characters and the second line is 1 character: `git checkout v9.1.0404 && make -j && make install DESTDIR=$HOME/myvim && ~/myvim/usr/local/bin/vim --clean -u NONE -U NONE +10new +'norm 10000a.' +'norm o,' +'norm gg'
2. Press CTRL-D to scroll down



### Expected behaviour

Vim scrolls to the second line

Actual behavior: No scrolling happens when CTRL-D is pressed

### Version of Vim

9.1.0380

### Environment

Arch Linux, GNOME Terminal

### Logs and stack traces
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `06bdac158072b90560915f8e664ee6d9bdab2f9b` and the full history behind it is present.
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
