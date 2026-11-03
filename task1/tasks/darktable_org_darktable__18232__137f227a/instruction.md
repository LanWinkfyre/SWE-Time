# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Darktable stuck in processing loop

### Describe the bug

I was editing an image. When I enabled _diffuse or sharpen_ with the built-in _local contrast (fine)_ preset, darktable displayed _working_, then it went away, then came back, continuing until I pressed `l` to get back to the lighttable. The console showed constant activity (I only had pipeline and cache debug enabled, I think). After restarting, I was unable to reproduce this.
The rogue pipeline run starts on line 92223 (`5236.7362 pipe state changing`). Yes, I know it's huge.

[spinning.zip](https://github.com/user-attachments/files/18464431/spinning.zip)

[DSD01499.ARW.xmp.txt](https://github.com/user-attachments/files/18464434/DSD01499.ARW.xmp.txt)
The raw file is at https://discuss.pixls.us/uploads/short-url/oAeRWht8HsAph1zqcLtbBOBXDD1.ARW

### Steps to reproduce

I'll try to reproduce this later; initial attempt failed.

### Expected behavior

No spinning

### Logfile | Screenshot | Screencast

_No response_

### Commit

_No response_

### Where did you obtain darktable from?

self compiled

### darktable version



### What OS are you using?

Linux

### What is the version of your OS?

Ubuntu 24.10

### Describe your system?

_No response_

### Are you using OpenCL GPU in darktable?

Yes

### If yes, what is the GPU card and driver?

NVidia 1060, 550.127.08

### Please provide additional context if applicable. You can attach files too, but might need to rename to .txt or .zip

_No response_

bisect
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `f5f3c098bada9ec55bb0d44af992702f92bdbf77` and the full history behind it is present.
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
