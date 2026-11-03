# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Can't seek backwards in Ogg Opus file

### mpv version and platform
<pre>

 built on Sat Sep 21 23:34:29 CEST 2019
ffmpeg library versions:
   libavutil       56.35.100
   libavcodec      58.58.101
   libavformat     58.32.104
   libswscale      5.6.100
   libavfilter     7.58.102
   libswresample   3.6.100
ffmpeg version: N-94982-gea673a0edb
</pre>

### Reproduction steps
Attempt to seek backwards

### Expected behavior
Backward seek occurs.

### Actual behavior
A few warnings are thrown and the playback restarts a few seconds later than before.



### Log file
https://0x0.st/ztOP.log

### Sample files
https://0x0.st/ztOZ.ogg
bug is not reproducible when playing from HTTP (demuxer cache?)
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `61b46d101e95ce29c680082cc11ae72c7b80e045` and the full history behind it is present.
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
