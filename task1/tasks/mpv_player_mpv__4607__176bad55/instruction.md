# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Problem with ewa_* scalers

### mpv version and platform

 
GPU + Apple drivers should support OpenGL 4.1.  
This does not happen on a Broadwell iGPU (but otherwise identical system/configuration).

### Reproduction steps

Play video with scale/cscale set to an ewa_* scaler.

### Expected behavior

Normal playback.

### Actual behavior

Wrong colors with `cscale=ewa_*` or strange artifacts with `scale=ewa_*`.

### Log file


I double checked and the commit right before this one does not exhibit the problem.

Log showing cscale issue using `--no-config --cscale=ewa_lanczos --no-resume-playback -v`: https://0x0.st/G4L.txt
Log showing scale issue using `--no-config --scale=ewa_hanning --no-resume-playback -v`: https://0x0.st/G43.txt

Screenshot of unscaled video: https://0x0.st/G4t.png
Screenshot of fullscreen video exhibiting `scale` issue: https://0x0.st/G4v.png
Screenshot of fullscreen video exhibiting `cscale` issue: https://0x0.st/G4S.png
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `18c74f7dfe9cbefe9de818caa00c3f77ce600f71` and the full history behind it is present.
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
