# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[ao/alsa] Device underrun detected

### mpv version and platform

OS: `Slackware64-current`



### Reproduction steps

1. mpv --ao alsa https://angellore.bandcamp.com/album/la-litanie-des-cendres
2. Skip to about 10 seconds before the first track ends and wait for the next track to start.
3. It should print `[ao/alsa] Device underrun detected.` as the next track starts.
4. Note this will not happen if you directly skip to the next track and seems to occur with any bandcamp link. I have not seen it with local content.

### Expected behavior

It should not experience a device underrun with alsa.

### Actual behavior

It will prints the follow warning when starting the next track on the playlist, but not when skipping directly to the next track.
```
[ao/alsa] Device underrun detected.
```







### Log file

https://0x0.st/s_S4.txt

For the other alsa errors see issue https://github.com/mpv-player/mpv/issues/5890.

### Sample files

This bandcamp link will reproduce it.
https://angellore.bandcamp.com/album/la-litanie-des-cendres
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `bca59516cc172e72a606b01b783added9c45dfb8` and the full history behind it is present.
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
