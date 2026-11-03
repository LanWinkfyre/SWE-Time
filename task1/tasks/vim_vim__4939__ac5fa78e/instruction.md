# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
QuickFixLine highlighting does not start from the beginning of a quickfix line

**Describe the bug**

In a quickfix window, the `QuickFixLine` highlighting starts from the end of the text, instead of the beginning of the line.

**To Reproduce**

Run this shell command:

    $ printf 'a\nb\nc' >/tmp/file && vim -Nu NONE --cmd 'syntax on' +'sil vim /./ % | copen' /tmp/file

The `QuickFixLine` highlighting starts after the text `a`.

**Expected behavior**

The `QuickFixLine` highlighting starts from the beginning of the line, which here displays `/tmp/file|1 col 1|`.

**Screenshots**

![gif](https://user-images.githubusercontent.com/8505073/64922048-9da96200-d7ca-11e9-81a4-4a90bce65e80.gif)

**Environment**

 - Vim version: 8.1  Included patches: 1-2032
 - OS: Ubuntu 16.04.6 LTS
 - Terminal: st

**Additional context**

In the past, `QuickFixLine` highlighted the whole current quickfix line.
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `1ac90b4fa63414d56750559506a3e076df6923b0` and the full history behind it is present.
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
