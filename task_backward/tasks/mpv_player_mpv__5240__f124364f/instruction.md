# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression: failure to take screenshot with hwdec=vaapi

### mpv version and platform


ffmpeg 2d131fc31
libva1 1.8.3-1
Intel Ivy Bridge 

### Reproduction steps

`mpv <file> --hwdec=vaapi`
press `s` for screen shot 

### Expected behavior

png screenshot taken

### Actual behavior
```
[ffmpeg] AVHWFramesContext: Failed to read image from surface 0x400002b: 16 (surface is in use).
Taking screenshot failed.
```
### Log file
[log](http://sprunge.us/EdPd)

### Bisect
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `0e311fc0e8658a2c1f60bd57366c854e7fc129bc` and the full history behind it is present.
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
