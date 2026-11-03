# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
regression - --tscale=sphinx playback dies with 4k 60fps content

When I play a 4k 60fps VP9 video with this config

```
vo=gpu-next
hwdec=d3d11va
gpu-api=d3d11

video-sync=display-resample
interpolation
tscale=sphinx
```

playback only shows a black screen for the first few seconds and the logs are flooded with issues.

```
[ffmpeg] AVHWFramesContext: Static surface pool size exceeded.
[ffmpeg/video] vp9: get_buffer() failed
Error while decoding frame (hardware decoding)!
[ffmpeg] AVHWFramesContext: Static surface pool size exceeded.
[ffmpeg/video] vp9: get_buffer() failed
Error while decoding frame (hardware decoding)!
[ffmpeg] AVHWFramesContext: Static surface pool size exceeded.
[ffmpeg/video] vp9: get_buffer() failed
Error while decoding frame (hardware decoding)!
Attempting next decoding method after failure of vp9-d3d11va.
[ffmpeg/video] vp9: Not all references are available
[ffmpeg/video] vp9: Not all references are available
```

When commenting out `tscale=sphinx`, issue is gone.

Log:
[output.txt](https://github.com/mpv-player/mpv/files/13418958/output.txt)

Broke with
https://github.com/shinchiro/mpv-winbuild-cmake/releases/tag/20231120

Still good with
https://github.com/shinchiro/mpv-winbuild-cmake/releases/tag/20231118

Win 11 23H2
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `8faa0abae8270aedee8972070cd7c83b1cb0a095` and the full history behind it is present.
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
