# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Double click fullscreen on touchpad is broken on latest Manjaro KDE Plasma (X11)

### mpv Information

```bash
mpv v0.38.0 Copyright © 2000-2024 mpv/MPlayer/mplayer2 projects
 built on Apr 18 2024 06:31:17
libplacebo version: v6.338.2
FFmpeg version: n6.1.1
FFmpeg library versions:
   libavutil       58.29.100
   libavcodec      60.31.102
   libavformat     60.16.100
   libswscale      7.5.100
   libavfilter     9.12.100
   libswresample   4.12.100
```


### Other Information

- Linux version: Manjaro Linux
- Kernel Version: Linux 6.6.30-2-MANJARO
- GPU Model: Intel Corporation CoffeeLake-H GT2 [UHD Graphics 630] 
- Mesa/GPU Driver Version: OpenGL version string: 4.6 (Compatibility Profile) Mesa 24.0.6-manjaro1.1
- Window Manager and Version: kwin_x11 idk version
- Source mpv: Manjaro repo


### Reproduction Steps

Install Manjaro with latest KDE Plasma, install mpv, open some video. Exit fullscreen if in fullscreen.

When you click on window, cursor immediately goes into "Move window" mode.
When clicking with mouse, it goes back fast enough to register second click in normal mode and go into fullscreen. (Although still not perfect, sometimes it doesn't register second click)
When clicking with touchpad, it goes into "Move window" mode and stays there for 0.5-1 second, so double click can't register and you can't go into fullscren.

upd. if you click suuuuuper fast with touchpad, you can manage to double click before cursor goes into "Move window" mode :3

### Expected Behavior

Working

I expect that when I click, cursor doesn't go into "Move window" mode, but if I click, hold and then move cursor while holding, it goes into "Move window" mode.
If I'm not wrong, before latest Manjaro KDE Plasma update (KDE 5 -> KDE 6), it was working pretty good. Not sure if issue should be fixed on their side or on mpv side.

### Actual Behavior

Not working

### Log File

[output.txt](https://github.com/mpv-player/mpv/files/15457900/output.txt)


### Sample Files

_No response_

### I carefully read all instruction and confirm that I did the following:

- [X] I tested with the latest mpv version to validate that the issue is not already fixed.
- [X] I provided all required information including system and mpv version.
- [X] I produced the log file with the exact same set of files, parameters, and conditions used in "Reproduction Steps", with the addition of `--log-file=output.txt`.
- [X] I produced the log file while the behaviors described in "Actual Behavior" were actively observed.
- [X] I attached the full, untruncated log file.
- [X] I attached the backtrace in the case of a crash.

  cc @na-na-hi
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `021c5dedb1f0759d6748dd6303c1fdf7f35367e4` and the full history behind it is present.
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
