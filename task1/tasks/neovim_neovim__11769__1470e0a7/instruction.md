# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Crash with ``%s/\n\n/^M/g``

<!-- Before reporting: search existing issues and check the FAQ. -->


- `vim -u DEFAULTS` (version: ) behaves differently? yes, it doesn't crash
- Operating system/version: openSUSE/Tumbleweed as of today
- Terminal name/version: gnome-terminal-3.34.2-2.1.x86_64
- `$TERM`: xterm-256color

### Steps to reproduce using `nvim -u NORC`

Reproduction is unreliable so I don't know what it means, I haven't mean be able to reproduce with ``-u NORC``.

Otherwise I just open a Python file to edit, and when I try command ``%s/\n\n/
/`` nvim crashes. I am not 100% sure whether it crashes already when writing the command (when writing ``\n``), or when I actually run the command.

### Actual behaviour

The stderr contains:


and the attached gdb shows:


### Expected behaviour
Of course, no crash.
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `6f073ccbf464e2f2cd6d6855aa3f27ee1adcc20d` and the full history behind it is present.
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
