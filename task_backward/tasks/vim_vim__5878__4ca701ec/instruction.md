# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[VIM 8.2.500] function getbufvar() with empty varname returns variables from wrong buffer

**Describe the bug**
Calling `getbufvar(1,'varname')` currently returns the variable 'varname' from buffer 1.

However, calling `getbufvar(1,'')` always returns buffer variables from the current buffer.

**To Reproduce**
Detailed steps to reproduce the behavior:
1. Launch `vim`
2. Split the window into a new buffer `:new`
3. In the top buffer set a buffer local variable `:let b:test = 'upper buffer'`
4. Get top buffer number `:echo bufnr('')` should return `1`
5. Switch to lower buffer.
6. Set lower buffer variable.  `let b:test = 'lower buffer'`
6. Get top buffer variable directly.  `:echo getbufvar(1,'test')`  This should work.
7. Get top buffer variable indirectly.  `:echo getbufvar(1,'').test`.   This returns 'lower buffer'

**Expected behavior**

I would expect `getbufvar(0,'test')` and `getbufvar(0,'').test` to work identically if `test` is set.

**Environment (please complete the following information):**
 - Vim version 8.2.0500 
 - OS: Ubuntu 18.04
 - SSH / tmux / putty






Git bisect suggests


The following command was used to test;
```
TERM=dumb /tmp/build/bin/vim +'let b:test="lower"' +new +'let b:test="upper"' +'wincmd w' +'echo getbufvar(2,"test") getbufvar(2,"").test' '+sleep 2' '+qa'
```
It outputs `upper upper` on a good build, and `upper lower` on a bad build.
Hope any of that helps.
Cheers

FYI - I noticed the problem specifically because the _vim-gitgutter_ plugin started failing.
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `3cca299520a4980fd1b124564bd67782ca977c15` and the full history behind it is present.
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
