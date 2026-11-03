# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression: Video freezes on Windows

This problem is first observed with lachs0r's build
mpv-x86_64-20140331.7z
It is **not** observed with 
mpv-x86_64-20140306.
Sorry, I can't narrow it down further. I am able to build the latest mpv version with the build scripts, but would appreciate any guidance on how to bisect in this environment.

Intel Haswell graphics on Windows 7 64-bit with opengl-hq, video will occasionally freeze on a single frame, while sound continues playing and the player remains otherwise responsive. It is most frequently triggered by switching between windowed and full screen mode.

Reiniting the video (i.e., inserting/removing a filter) rectifies the situation.


Also happens with vo=opengl. Seeking also seems to fix it.


ah! seems to requrire ao=wasapi=exclusive (not ao=wasapi) to reproduce



I should also add that with lachs0rs latest build, the problem has changed such that rather than freezing the video with no obvious effect to the audio, now the audio is effected and exhibits a continuous crackling mixed with the real audio and the playback rate seems to cut to about half for both video and audio.

Interestingly, I can't reproduce the behaviour when I build mpv in cygwin to try and test reverting the commit. I'm currently wrestling with lachs0rs build scripts to look into this further.
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `6589c5424ec16849c9665e8ea365d9e5ce0a88cb` and the full history behind it is present.
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
