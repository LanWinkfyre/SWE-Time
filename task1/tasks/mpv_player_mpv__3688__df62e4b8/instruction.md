# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Can't seek in audio files when using lavfi-complex

### mpv version and platform

0.21
### Reproduction steps

try to seek with the following:

```
mpv file.mp3 --lavfi-complex='[aid1]asplit[ao][a1];[a1] avectorscope=m=lissajous_xy:s=256x256:r=25 [spectrum];[vid1][spectrum]overlay[vo]'
```
### Expected behavior

immediate seek
### Actual behavior

audio stops and resumes after seconds
### Log file

http://pastebin.com/XG8vm02z

Bisected, the bad commit is:



hr-seek works.
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `a2fa0d0b68ce200598122145254f56ae1adff91e` and the full history behind it is present.
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
