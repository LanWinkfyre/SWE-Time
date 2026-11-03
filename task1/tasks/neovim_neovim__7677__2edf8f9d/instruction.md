# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
shada error: invalid line number after `nvim -u NORC +term`

<!-- Before reporting: search existing issues and check the FAQ. -->

- `nvim --version`: NVIM v0.2.2
- Vim (version: ) behaves differently? irrelevant
- Operating system/version: Arch Linux
- Terminal name/version: GNOME Terminal 3.26.2 Using VTE version 0.50.2 +GNUTLS or TTY
- `$TERM`: xterm-256color or linux

### Steps to reproduce using `nvim -u NORC`
With:
- shell: zsh with or without `.zshrc` or sh
- ~/.local/share/nvim/shada/main.shada existing or not exiting.

```
nvim -u NORC +term
:q
nvim

```
### Actual behaviour
Cause output error:
```
E575: Error while reading ShaDa file: mark entry at position [number] has invalid line number
Press ENTER or type command to continue
```
### Expected behaviour
This error should not be displayed

\[note: should not be the same as https://github.com/neovim/neovim/issues/4100 \]
\[note: this error not occur if in the vimrc there is `autocmd BufWinEnter,WinEnter * startinsert` as I've explained in https://github.com/neovim/neovim/issues/7678 \]

Hi
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `27a577586eace687c47e7398845178208cae524a` and the full history behind it is present.
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
