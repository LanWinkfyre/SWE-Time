# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
E909: Cannot index a special variable for const dict<any>

### Steps to reproduce

1. prepare the following files:
s.vim:
```vim
vim9script

export def V(): dict<any>
  return {a: [1, 2], b: 1}
enddef
```
t.vim:
```vim
vim9script

import './s.vim' as s

def Test()
  const v = s.V()
  var b = v.a[1]
enddef

Test()
```
2. source t.vim

### Expected behaviour

It runs without errors.

If the function `V` is defined in the same module, or if `const` is replaced by `var`, it runs fine.



This causes errors with [vim9-stargate](https://github.com/monkoose/vim9-stargate).

### Version of Vim

9.0.695+

### Environment

Arch Linux, GNOME Terminal / GVIM.

### Logs and stack traces

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `3f0092c141824356b55b11cd3985baaf4df65334` and the full history behind it is present.
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
