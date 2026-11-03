# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
JSON boolean/serialization - LSP Go to References

### Neovim version (nvim -v)



### Vim (not Nvim) behaves the same?

no

### Operating system/version

debian 11

### Terminal name/version

kitty

### $TERM environment variable

xterm-256color

### Installation

build from repo

### How to reproduce the issue

install go LSP / or any other - mark a word and do `gd`  or `:lua vim.lsp.buf.references()`




### Expected behavior

jump to defninition - in `v0.5.0`  it does - on master it doesnt

### Actual behavior

errors 

<img width="1485" alt="Bildschirmfoto 2021-09-27 um 08 26 10" src="https://user-images.githubusercontent.com/2891702/134855261-35397587-a5ab-4fbf-b938-a8501f3ad80f.png">


bisecting, v0.5.0 to master revealed this "bad" commit.

`
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `bec7f47cee8b69fbaa3452762745c9d0e8ea4256` and the full history behind it is present.
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
