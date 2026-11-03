# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Two AgX instances for scene referred (AgX) workflow if there is an auto preset for Agx module

### Is there an existing issue for this?

- [x] I checked and did not find my issue in the already reported ones

### Describe the bug

My selected workflow in the darktable settings is scene referred (AgX).
Additionally I have an auto applied preset for the AgX module.
After importing a RAW file (CR3, no HDR), there are two active instances of the AgX module: one from my auto preset, the second (above, later in the pipe) the standard AgX instance. Same if the history of the image is reset.
Until some days ago only one AgX module instance (with values from the auto preset) was there.



### Steps to reproduce

see above

### Expected behavior

_No response_

### Logfile | Screenshot | Screencast

_No response_

### Commit



### Where did you obtain darktable from?

self compiled

### darktable version



### What OS are you using?

Linux

### What is the version of your OS?

Fedora 43

### Describe your system

_No response_

### Are you using OpenCL GPU in darktable?

Yes

### If yes, what is the GPU card and driver?

issue does not depend on openCL

### Please provide additional context if applicable. You can attach files too, but might need to rename to .txt or .zip

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `65fe2e9e3ae0726fb6756e185df27b0b46b12e61` and the full history behind it is present.
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
