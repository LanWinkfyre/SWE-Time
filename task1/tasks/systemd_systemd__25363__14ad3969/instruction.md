# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
systemd-boot 252 fails to boot on MacBookAir4,2/Mac

### systemd version the issue has been seen with

252.1

### Used distribution

archLinux

### Linux kernel version used

6.0.8-arch1-1

### CPU architectures issue was seen on

x86_64

### Component

bootctl

### Expected behaviour you didn't see

Systemds UEFI boot manager should be loaded and working

### Unexpected behaviour you saw

after upgrading systemd to 252 and updating the UEFI bootloader, my macbook fails to boot my linux install. There are unfortunately no errors, the mac simply skips to the next bootloader available. Only solution is to downgrade to 251. I've never experienced any issue like that, the bootloader has always worked fine

### Steps to reproduce the problem

upgrade a MacBookAir4,2 to systemd-252 and update the bootloader

### Additional program output to the terminal or log subsystem illustrating the issue

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `e48237358fd21e26722506c5cf89c99f2c40a90f` and the full history behind it is present.
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
