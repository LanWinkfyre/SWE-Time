# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`execute('syn list vimComment')` lacks newline between matches


 - Vim (version:  8.1 Included patches: 1-1661) behaves differently? Yes
 - Operating system:     Ubuntu 16.04.6 LTS
 - Terminal emulator:    st 0.8.2
 - Terminal multiplexer: tmux next-3.1
 - `$TERM`:                tmux-256color
 - Shell:                zsh 5.7.1 (x86_64-pc-linux-gnu)

### Steps to reproduce using `nvim -u NORC`

Consider this shell command:

    $ nvim -Nu NONE --cmd 'syntax enable' +"echo execute('syn list vimComment')" /tmp/vim.vim

### Actual behaviour

It outputs the definition of the syntax group `vimComment` on a single line.

### Expected behaviour

I would expect the output to be on multiple lines, because:

 1. the output of the same command is on multiple lines in Vim
 2. the output of the same command without `execute()` (i.e. `:syn list vimComment`) is on multiple lines in Nvim
 3. it's harder to detect when the definition of an item ends when they are all on the same line


---

I'm relying on the output of `execute('syn list someSyntaxGroup')` to override the definition of some syntax groups, and other things (like highlight groups).
The more consistent the output of `execute()` is with Vim and with the command it's running, the easier it is to parse it.
Although it's probably a bad idea to parse the output of `execute()` considering all the issues I faced with it so far, I don't know how else I can get the definition of a syntax group or highlight group in a Vim script.

If you don't consider this as an issue, feel free to close it.
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `777cc6f98aa08ca4597658d0fb8b612a1c7c4c77` and the full history behind it is present.
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
