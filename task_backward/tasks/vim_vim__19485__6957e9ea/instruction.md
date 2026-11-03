# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Normal guifg color turns to white on CursorLine when termguicolors is set

### Steps to reproduce

1. `vim --clean`
2. Input some text
3. `:colo blue`. The `Normal` text color changes to an orange one.
4. `:set cursorline termguicolors`
5. Move cursor and you can see the text becomes white on cursor line



### Expected behaviour

The cursor line foreground color doesn't change if not explicitly set, like in GUI or with 'notermguicolors'.

### Version of Vim

9.2.43

### Environment

Arch Linux, GNOME Termal 3.58.1-1 with or without tmux, $TERM = xterm-256color or tmux-256color.

### Logs and stack traces

```shell

```
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `9b16aa34b62d2e477c4ed47cb9df5a0da183e193` and the full history behind it is present.
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
