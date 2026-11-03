# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression in terminal underline handling

### systemd version the issue has been seen with

256.1

### Used distribution

Arch

### Linux kernel version used

6.9.5-arch1-1

### CPU architectures issue was seen on

x86_64

### Component

systemctl

### Expected behaviour you didn't see

Usual output of `$ systemctl` with underlined lines of text not blinking.

### Unexpected behaviour you saw

Undesirable output of `$ systemctl` with underlined lines of text blinking away (only happens on specific terminals - see below).

### Steps to reproduce the problem

The problem only occurs on a few different terminals. So far I have reproduced the problem on `rxvt-unicode`, `xterm` and `foot`. The first 2 in particular have been around for quite a long time.. which makes me think this is a `systemd` issue (although, of course those terminals might just be buggy?).

To reproduce:

- install / run one of the aforementioned terminal applications
- inside that terminal, run `systemctl`

Bisection (unsurprisingly) points to:

Thanks for your help.

### Additional program output to the terminal or log subsystem illustrating the issue

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `eb37c0c07809d48aba34ffeced5c18055b70d81e` and the full history behind it is present.
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
