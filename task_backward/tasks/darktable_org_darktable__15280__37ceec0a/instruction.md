# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
### Describe the bug

 darktable tries to start every lua script in the ~/.config/darktable/lua directory.

I'm not sure of the cause at present, but you end up with a messed up darktablerc file as the result.  It may be fixable by just deleting all the lua lines, but I'm trying to report this before it affects too many people.

### Steps to reproduce

1. git pull
2. build darktable
3. start darktable
4. observe all the loading messages and the UI going nuts

### Expected behavior

darktable should not try and start every script on startup

### Logfile | Screenshot | Screencast

_No response_

### Commit

_No response_

### Where did you install darktable from?

darktable.org

### darktable version



### What OS are you using?

Linux

### What is the version of your OS?

Ubuntu 22.04

### Describe your system?

_No response_

### Are you using OpenCL GPU in darktable?

None

### If yes, what is the GPU card and driver?

_No response_

### Please provide additional context if applicable. You can attach files too, but might need to rename to .txt or .zip
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `0930cccd42d3cc94e04345da5a6779d1ebdaaeff` and the full history behind it is present.
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
