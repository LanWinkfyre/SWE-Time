# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Weird characters appearing right after starting neovim or when editing lines

- `nvim --version`: NVIM v0.3.2-dev

- Operating system/version: Ubuntu 14.04.5 LTS
- Terminal name/version: GNOME Terminal 3.6.2
- `$TERM`: `xterm-256color`
- `$VTE_VERSION`: `3409`

### Original Report

https://www.reddit.com/r/neovim/comments/9la6mu/weird_characters_when_opening_nvim_with_u_norc/

### Steps to reproduce using `nvim -u NORC`

```
nvim -u NORC
```

### Actual behaviour

![image](https://user-images.githubusercontent.com/135535/46539756-64ac0200-c885-11e8-94c7-e54ba85dd4bf.png)

### Expected behaviour

![image](https://user-images.githubusercontent.com/135535/46539632-067f1f00-c885-11e8-9714-3fde1423f438.png)



I hope you don't mind @MichaHoffmann, but I ended up doing a bisect as well.
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `39ad99b594aa68b6c3024dd9bfa3f7e31c14dff9` and the full history behind it is present.
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
