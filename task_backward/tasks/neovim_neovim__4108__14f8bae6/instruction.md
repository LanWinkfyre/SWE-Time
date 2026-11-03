# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
E576: Failed to parse ShaDa file: incomplete msgpack string at position 85

When I open neovim, I am met with the title error message. When I close neovim, I am met with a different error message claiming that "~/.local/share/nvim/shada/main.shada" is not a valid shada file.



It is consistent between builds, but does not happen the very first time I run nvim after the build:
$ git checkout master
$ git clean -xdf
$ rm -rf ~/.local/share/nvim
$ make -j CMAKE_BUILD_TYPE=Release install
$ nvim # No error
:q
$ nvim # error
E576: Failed to parse ShaDa file: incomplete msgpack string at position 85
Press ENTER or type command to continue


Using the following bisect script,

```
#!/bin/sh
git clean -xdf
make -j CMAKE_BUILD_TYPE=Release
./build/bin/nvim -u NONE -e -s -c ":q"
```

I got
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `9b0b3a0883ab6c9d9f57fcf65d5bc951f40dff3c` and the full history behind it is present.
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
