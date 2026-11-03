# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression: Incorrect video scaling on wayland

### Important Information

- mpv version: 0.34 (tested with master as well)
- Linux Distribution and Version: Arch Linux, current™
- Source of the mpv binary: - https://archlinux.org/packages/community/x86_64/mpv/
                                            - https://github.com/archlinux/svntogit-community/blob/packages/mpv/trunk/PKGBUILD
- If known which version of mpv introduced the problem: 0.34
- Window Manager and version: Wayland: sway 1.6.1
- GPU driver and version: Intel-GPU in Linux 5.14.16
- Possible screenshot or video of visual glitches: Video starts incorrectly scaled

### Reproduction steps

`--no-config` didn't help, hence the reproduction steps below.
Unfortunately, on this multi-monitor-setup, the problem only exists on one of the three monitors in question (all of them differently scaled due to different DPI). The affected screen is the one that is unscaled, however it is unclear to me if that is coincidence or meaningful to the regression.

Assumed the video initially gets opened on the one affected screen (screenshots further down under expected and actual behavior):

1. get a video file (tested with VP_9, mp4, Youtube-Streaming)
2. call `mpv <videofile/videolink>
3. observe a video that is (usually, see 5) way too large for the window it's played in
4. full-screen and de-fullscreen -> issue's gone
5. move video to another screen -> problem returns, this time video gets too small
6. full-screen and de-fullscreen -> issue's gone
7. move back to screen where it's initially opened: original issue arises again

4 and 6 can also be de-fullscreen and re-fullscreen, same behavior
5's exact behavior might be related to different scalings on different screens

Given that only some screens are affected combined with 7. might maybe point to mpv picking the wrong scaling factors for the display in use, but that's guesswork on my side given the evidence and might be entirely incorrect.

### Bisection

 Unfortunately I don't see myself capable of fixing this issue right away, so I'm afraid I have to recourse to merely reporting.

### Log file

[mpvlog.txt](https://github.com/mpv-player/mpv/files/7496721/mpvlog.txt)

### Expected behavior

Video always has the correct size so that it fits the window:
![good](https://user-images.githubusercontent.com/6452205/140737414-3fee9f6f-8f62-40c8-ad26-fcdb1b6a6a19.png)

### Actual behavior

Video is incorrectly scaled upon opening:
![bad](https://user-images.githubusercontent.com/6452205/140737454-a3ea8b28-321b-472d-8658-9de28c370d99.png)
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `73563cebf9ae6c3c8f5ca4a84f67b2e96c08f51f` and the full history behind it is present.
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
