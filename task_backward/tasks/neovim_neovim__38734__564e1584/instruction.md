# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`--api-info` lost container types such as `ArrayOf`

### Problem

`--api-info`/api metadata has lost all `ArrayOf` types.



### Steps to reproduce

`nvim --api-info | strings | grep -i arrayof`

### Expected behavior

Previous `ArrayOf` etc. types are present.

### Nvim version (nvim -v)

NVIM v0.12.0

### Vim (not Nvim) behaves the same?

no

### Operating system/version

Popos

### Terminal name/version

Any

### $TERM environment variable

Any

### Installation

build from repo
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `333e3178eca0760019b1a759f67ac0b96cab50bd` and the full history behind it is present.
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
