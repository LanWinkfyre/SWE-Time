# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Video output often freezes on 60fps VP9 video

### mpv version and platform

```
# mpv --version                                                    
mpv 0.21.0 (C) 2000-2016 mpv/MPlayer/mplayer2 projects
 built on Sun Oct 23 02:59:47 UTC 2016
ffmpeg library versions:
   libavutil       55.33.100
   libavcodec      57.63.103
   libavformat     57.53.100
   libswscale      4.1.100
   libavfilter     6.64.100
   libswresample   2.2.100
ffmpeg version: N-82090-g728ccae
```

xubuntu 16.04.1 with Intel video, no compositor, no `TearFree` or any other unusual options, 4K display

### Reproduction steps

1. Download https://ludios.org/tmp/WipEout%20HD%20-%20Supersonic%20in%201080p%2060FPS-uQqRIX1RMtE.webm
2. Play it in mpv
3. Fullscreen (optional)
4. Skip to 10:10 and play the video for about a minute
5. Observe that video output freezes, while audio keeps playing

Note that it will freeze at many other locations in the video, but it is not always reproducible at the exact same locations.

### Expected behavior

mpv frame skips where needed, but does not stop video output permanently

### Actual behavior

video output frozen permanently (until leaving and re-entering fullscreen, or sending other events)

### Log file

Nothing special seems to happen when the video output freezes.

http://sprunge.us/WhQi

### Sample files

https://ludios.org/tmp/WipEout%20HD%20-%20Supersonic%20in%201080p%2060FPS-uQqRIX1RMtE.webm

@wm4
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `3f5b41dfa30ca282fd99176bf879493dd72b3119` and the full history behind it is present.
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
