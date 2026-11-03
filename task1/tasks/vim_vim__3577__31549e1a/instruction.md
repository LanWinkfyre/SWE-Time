# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Test_filter_commands() fails when $LANG=C.UTF-8

I am attempting to compile Vim 8.1.0500 on a Raspberry Pi running Raspbian Jessie. Running `make test` fails with:

```
Found errors in Test_filter_commands():
function RunTheTest[40]..Test_filter_commands line 18: Pattern '^\\s*helplang=\\w*$' does not match '   helplang=C.'
```



In Vim on this machine:
- `:set helplang` returns `   helplang=C.` (note the trailing period)
- `:language messages` gives `Current messages language: "C.UTF-8"`
- `:language` gives `Current language: "LC_CTYPE=C.UTF-8;LC_NUMERIC=C;LC_TIME=C.UTF-8;LC_COLLATE=C.UTF-8;LC_MONETARY=C.UTF-8;LC_MESSAGES=C.UTF-8;LC_PAPER=C.UTF-8;LC_NAME=C.UTF-8;LC_ADDRESS=C.UTF-8;LC_TELEPHONE=C.UTF-8;LC_MEASUREMENT=C.UTF-8;LC_IDENTIFICATION=
C.UTF-8"`
- `$ echo $LANG` prints `C.UTF-8`

From the help documentation, it seems that `helplang` comes from the messages language. On another machine with `$LANG=en_US.UTF-8`, `helplang=en` as expected.

I am not very familiar with the internals of Vim, but it seems that a `$LANG` without an underscore is being parsed improperly. 

@deoxys314 ran the bisect and helped to diagnose this issue with me
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `833e5dab143034b7e43bc0be49b2eb3687ff9ab7` and the full history behind it is present.
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
