# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wrong incsearch highlighting when redrawing from timer in cmdline


- `vim -u DEFAULTS` (version: ) behaves differently? Yes
- Operating system/version: Windows 10 WSL
- Terminal name/version: wintty
- `$TERM`: xterm-256color

### Steps to reproduce using `nvim -u NORC`

```
nvim -u NORC

autocmd CmdlineChanged * call timer_start(0, {-> execute('redraw')})
```
1. `:h<CR>` to open help file
2. `/with<CR>` search for text
3. `/Bar<CR>` search for another text

### Actual behaviour
When searching for `with`, the `incsearch` highlighting is missing.
When searching for `Bar`, `incsearch` highlights `with` instead of `Bar`.

### Expected behaviour
`incsearch` highlight works as expected.
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `3fbff98cfd48941ceac086543dd7d6bcdbfb18ab` and the full history behind it is present.
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
