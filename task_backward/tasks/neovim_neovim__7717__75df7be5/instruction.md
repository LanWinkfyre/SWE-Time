# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wrong default 'titleold' on Fedora 26 when locale set to en_GB

- `nvim --version`: 0.2.1, 0.2.2, master
- Vim (version: ) behaves differently? yes
- Operating system/version: Fedora 26
- Terminal name/version: gnome-terminal
- `$TERM`: xterm-256color

### Steps to reproduce using `nvim -u NORC`

```
LC_ALL=en_GB nvim -u NORC
:set title
:set titleold?
```

### Actual behaviour
```
  titleold=Project-Id-Version: Vim(UK English)^@Report-Msgid-Bugs-To: ^@POT-Crea
tion-Date: 2014-05-26 14:21+0200^@PO-Revision-Date: 2003-02-25 11:05+0000^@Last-
Translator: Mike Williams <mrw@eandem.co.uk>^@Language-Team: Mike Williams <mrw@
eandem.co.uk>^@Language: ^@MIME-Version: 1.0^@Content-Type: text/plain; charset=
ISO_8859-1^@Content-Transfer-Encoding: 7bit^@
```
### Expected behaviour
```
  titleold=
```

### Additional information

The bug was introduced with this commit:


The bug appears only when locale is set to ```en_GB```, other locales seem to work file.  
I am able to reproduce in on fresh Fedora 26 install in virtual machine.  
I can't reproduce the bug on Ubuntu 17.10.

Edit:
Bug shows only after running ```sudo make install```. When I try to install nvim to non-default location (e.g. ```make DESTDIR=/home/user install```) bug does not appear.
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `8813b29cec13f7410427fbb8913d3753dd6626a7` and the full history behind it is present.
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
