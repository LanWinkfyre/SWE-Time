# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Loading next/previous item gets progressively slower with longer playlists

### mpv Information

```bash
mpv 0.39.0 Copyright © 2000-2024 mpv/MPlayer/mplayer2 projects
libplacebo version: v7.349.0
FFmpeg version: 7.0.2
FFmpeg library versions:
   libavcodec      61.3.100
   libavdevice     61.1.100
   libavfilter     10.1.100
   libavformat     61.1.100
   libavutil       59.8.100
   libswresample   5.1.100
   libswscale      8.1.100
```


### Other Information




### Reproduction Steps

After updating to mpv 0.39.0 (Fedora 41), I noticed that loading the next/previous item takes progressively more time as playlists get longer. This was not the case with 0.37.0 (Fedora 40).
To replicate, simply create a long playlist and pipe into mpv like so:
```
yes $'image1.jpg\nimage2.jpg' | head -200000 | mpv --playlist=- --no-config --profile=fast
```
With reasonable-sized images and a short playlist, loading is effectively instant. The same images take several seconds to load with 200k items in the playlist.

I'm using images to test, since I find it easier to judge loading times, but the issue is present with videos as well.
The issue is also present in the Flathub version of mpv.

### Expected Behavior

Loading the next/previous playlist item is always fast, irrespective of playlist length.

### Actual Behavior

Loading the next/previous playlist item seems to correlate with playlist length.

### Log File

[output.txt](https://github.com/user-attachments/files/17632150/output.txt)


### Sample Files

_No response_

### I carefully read all instruction and confirm that I did the following:

- [X] I tested with the latest mpv version to validate that the issue is not already fixed.
- [X] I provided all required information including system and mpv version.
- [X] I produced the log file with the exact same set of files, parameters, and conditions used in "Reproduction Steps", with the addition of `--log-file=output.txt`.
- [X] I produced the log file while the behaviors described in "Actual Behavior" were actively observed.
- [X] I attached the full, untruncated log file.
- [X] I attached the backtrace in the case of a crash.



I'll need some time to figure out the "why" though
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `23843b4aa594dc8c885575f3d237cde3c29398a2` and the full history behind it is present.
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
