# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
journalctl: --follow doesn't work with --machine

### Submission type
- [x] Bug report
- [ ] Request for enhancement (RFE)
### systemd version the issue has been seen with

231
### Used distribution

Arch linux
### In case of bug report: Expected behaviour you didn't see

`--follow` works when used in combination with `--machine`
### In case of bug report: Unexpected behaviour you saw

New journal entries weren't shown after starting `journalctl --machine WHATEVER --follow`.
### In case of bug report: Steps to reproduce the problem
1. Start a container with nspawn
   
   ```
   # systemd-nspawn -bD arch
   ...
   ```
2. Run journalctl in another terminal
   
   ```
   # journalctl --machine arch --follow
   ...
   ```
3. Back to the container, write something in the journal
   
   ```
   [root@arch ~]# logger hello
   ```
4. Check that nothing gets printed in the journal terminal
5. Run journalctl again to see it printed
   
   ```
   # journalctl --machine arch --follow
   ...
   Aug 08 15:25:07 arch root[42]: hello
   ```
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `3f193af8807be50913b87e1a5b88c494f8985667` and the full history behind it is present.
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
