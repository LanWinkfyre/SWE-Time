# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Mapping <Tab> while not mapping <C-i>, shadows the default key action on <C-i>

### Neovim version (nvim -v)

0.8.0

### Vim (not Nvim) behaves the same?

no, this is a neovim feature only.

### Operating system/version

Manjaro Linux

### Terminal name/version

wezterm, kitty

### $TERM environment variable

xterm-256color

### Installation

system package manager

### How to reproduce the issue

1. Neovim can only distinguish between `<Tab>` and `<C-i>` when using a terminal that supports the "CSI" protocol, such as kitty or wezterm (with option enable_csi_u_key_encoding set to true). To reproduce this problem, you have to use a terminal that supports this.

2. Start neovim with no config and map the tab key from the command line.

```nvim -Nu NONE +'nno <Tab> :echom "Tab was pressed"<cr>'```

3. Press control i. This will print the message "Tab was pressed"

### Expected behavior

The expected result is that pressing tab will print the message, but pressing control-i will not. Instead, control-i should execute the default action (go forward in the jump list) associated to that key. This used to be the behavior in 0.7.2.

### Actual behavior

This is a regression that I noticed when I upgraded to nvim 0.8.0, coming from 0.7.2. In 0.7.2, it used to work as described in the expected behavior section. I could map tab and still use the jump list. The somewhat strange thing is that 0.8.0 does handle the difference between the two keys, when both are mapped.

```nvim -Nu NONE +'nno <C-i> :echom "C-i was pressed"<cr>' +'nno <tab> :echom "Tab was pressed"<cr>'```

This works fine. It only seems to conflate the bindings when one is mapped and the other is not.

I went ahead and did a git bisect.
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `4d896be681d9b93ebe34cce38a5e787cd0332261` and the full history behind it is present.
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
