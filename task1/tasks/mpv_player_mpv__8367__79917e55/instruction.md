# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Distorted audio with dvb-usb

### Important Information

Provide following Information:
- mpv version 
0.33
- Linux Distribution and Version 
EndeavourOS

- Source of the mpv binary
Arch official repo; package version 1:0.33.0-3

- If known which version of mpv introduced the problem
0.33

- GPU driver and version
AMD Radeon RX 5600 XT

I use mpv to watch TV with tvheadend 4.2.8-4 and a 'Technotrend TT Connect S2-3600':

`mpv --playlist=http://localhost:9981/playlist`

 mpv version 0.33 introduces distorted audio. I have to restart mpv several times or switch channels several times to make it work. Downgrading to the previous package version 1:0.32.0-6 solves the issue.


I downgraded libplacebo and finished a git bisect:




 I did a fresh git pull but then the git bisect was not going well. I had many comits where I had strange video stuttering with no audio at all. I did not know what to do with them: Skip them or mark them as bad? In the end I did not finish the second bisect.



PS:
I want to mention that I see the following log messages in the console when the issue happens:

```
Using hardware decoding (vaapi-copy).
AO: [pulse] 48000Hz stereo 2ch s16
VO: [gpu] 1280x720 nv12
AV: 00:00:02 / 00:00:03 (61%) A-V:  0.000 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:02 / 00:00:03 (62%) A-V:  0.000 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:02 / 00:00:03 (63%) A-V:  0.000 Dropped: 1 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:02 / 00:00:03 (66%) A-V:  0.000 Dropped: 2 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:02 / 00:00:04 (68%) A-V:  0.000 Dropped: 2 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:02 / 00:00:04 (68%) A-V:  0.000 Dropped: 2 Cache: 1.2s/1MB
Audio device underrun detected.
AV: 00:00:03 / 00:00:04 (72%) A-V:  0.000 Dropped: 2 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:03 / 00:00:04 (73%) A-V:  0.000 Dropped: 2 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:03 / 00:00:04 (73%) A-V:  0.000 Dropped: 2 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:04 / 00:00:05 (77%) A-V: -0.000 Dropped: 2 Cache: 1.1s/1MB
Audio device underrun detected.
AV: 00:00:04 / 00:00:05 (78%) A-V:  0.000 Dropped: 9 Cache: 1.2s/1MB
Audio device underrun detected.
AV: 00:00:05 / 00:00:06 (83%) A-V: -0.000 Dropped: 11 Cache: 1.1s/1MB
```
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `a9aa5a1b1cf3573a219dec2b98aea06d3b866908` and the full history behind it is present.
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
