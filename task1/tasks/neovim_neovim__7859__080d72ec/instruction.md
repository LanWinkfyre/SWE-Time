# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
getline() is broken

<!-- Before reporting: search existing issues and check the FAQ. -->


- Vim (version: ) behaves differently?: Yes.  In Vim8, no errors.
- Operating system/version: Ubuntu 16.04, Manjaro Linux
- Terminal name/version: st 0.7
- `$TERM`:

### Steps to reproduce using `nvim -u NORC`

It cannot be reproduced in `nvim -u NORC`.

### Actual behaviour

```
$ build/bin/nvim codecov.yml
Error detected while processing BufReadPost Auto commands for "*":
E691: Can only compare List with List
E15: Invalid expression: getline(1) =~# '\v^#!%(\f*/|/usr/bin/env\s*<)fish>' |     setlocal filetype=fish | endif
Error detected while processing function <SNR>11_DetectJS:
line    1:
E691: Can only compare List with List
E15: Invalid expression: getline(1) =~# '^#!.*/bin/\(env\s\+\)\?node\>'
Press ENTER or type command to continue
```

`getline(0)` returns `[]` when file opening.
It breaks the plugins.

### Expected behaviour

No errors.

### `git bisect` result

I have bisected the problem.
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `c06995b34d604a37f80ee1174fcb3530dbd59206` and the full history behind it is present.
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
