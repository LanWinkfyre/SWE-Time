# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
"At least OpenGL 2.1 or OpenGL ES 2.0 required." message shown inappropriately or repeatedly

Somewhat related to #5915

### mpv version and platform

mpv 0.28.2
Arch Linux x86_64

```
mpv 0.28.2 (C) 2000-2017 mpv/MPlayer/mplayer2 projects
 built on Mon May 14 09:49:30 CEST 2018
ffmpeg library versions:
   libavutil       56.14.100
   libavcodec      58.18.100
   libavformat     58.12.100
   libswscale      5.1.100
   libavfilter     7.16.100
   libswresample   3.1.100
ffmpeg version: 4.0
```

### Reproduction steps

Have an old computer which supports only really old OpenGL versions (in my case, OpenGL 1.4 and OpenGL ES 2.0)
**OR**
(if you use mesa) Use the `MESA_GL_VERSION_OVERRIDE` and `MESA_GLES_VERSION_OVERRIDE` environment variables to change reported OpenGL(ES) versions
**THEN**
Play videos with `--vo=gpu --gpu-api=opengl`

### Expected behavior

When the computer does not meet the playback requirements (ie OpenGL <2.1 **AND** OpenGL ES <2.0), the error message "At least OpenGL 2.1 or OpenGL ES 2.0 required." should appear once, and then (after following context creation failure errors) mpv should exit with an error status. Otherwise, the error message should not appear and playback should happen normally (other errors notwithstanding).

### Actual behavior

The error message is displayed whenever the computer's OpenGL version isn't at least 2.1, even if the OpenGL ES remark is irrelevant (ie OpenGL ES is not selected, or the version is sufficient for playback). The error message can appear as many as 3 times consecutively.

### Log file

`mpv --vo=gpu --gpu-api=opengl --opengl-es=no` https://0x0.st/s_UG.txt
`mpv --vo=gpu --gpu-api=opengl --opengl-es=yes` https://0x0.st/s_UD.txt

### Sample files

Happens with every file I tried so far, so I'm fairly sure I don't need to upload samples.





Just for fun, some logs from the last "ok" commit:
`mpv --vo=opengl --opengl-es=no` https://0x0.st/s_Gr.txt
`mpv --vo=opengl --opengl-es=yes` https://0x0.st/s_0C.txt
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
