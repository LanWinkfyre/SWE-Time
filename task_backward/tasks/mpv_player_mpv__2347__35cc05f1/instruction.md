# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression: VDPAU no longer used for some videos

Hi,

although I have had this problem for some time, I just now decided to look into it.

I am on an up-to-date Arch Linux system with the following software versions:
FFmpeg 2.8
Mesa 11.0, radeon driver r600
mpv 0.11.0 (+ current git master)

Some videos (H.264 in particular, not sure about other formats) that mpv played with VDPAU hardware decoding a few months ago are only played using software decoding now. Similar videos that should only differ in bit rate and resolution (I just noticed different profiles as well)  are fine. I tested the options "--vo=opengl --hwdec=vdpau", "--vo=opengl-hq --hwdec=vdpau" and "--vo=vdpau --hwdec=vdpau" and there doesn't seem to be a difference in behavior.

ffprobe output for a problematic file:

```
Metadata:
  major_brand     : isom
  minor_version   : 512
  compatible_brands: isomiso2avc1mp41
  encoder         : Lavf56.15.102
Duration: 02:15:26.40, start: 0.000000, bitrate: 754 kb/s
  Stream #0:0(eng): Video: h264 (Constrained Baseline) (avc1 / 0x31637661), yuv420p, 640x360 [SAR 1:1 DAR 16:9], 596 kb/s, 59.94 fps, 59.94 tbr, 11988 tbn, 119.88 tbc (default)
  Metadata:
    handler_name    : VideoHandler
  Stream #0:1(eng): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 110 kb/s (default)
  Metadata:
    handler_name    : SoundHandler
  Stream #0:2(und): Data: none (rtp  / 0x20707472), 28 kb/s (default)
  Metadata:
    creation_time   : 2015-09-25 22:43:30
    handler_name    : GPAC ISO Hint Handler
  Stream #0:3(und): Data: none (rtp  / 0x20707472), 8 kb/s (default)
  Metadata:
    creation_time   : 2015-09-25 22:49:49
    handler_name    : GPAC ISO Hint Handler
```

ffprobe output for a non-problematic file:

```
Metadata:
  major_brand     : isom
  minor_version   : 512
  compatible_brands: isomiso2avc1mp41
  encoder         : Lavf56.15.102
Duration: 01:53:39.50, start: 0.000000, bitrate: 2041 kb/s
  Stream #0:0(eng): Video: h264 (Main) (avc1 / 0x31637661), yuv420p, 960x540 [SAR 1:1 DAR 16:9], 1802 kb/s, 59.94 fps, 59.94 tbr, 11988 tbn, 119.88 tbc (default)
  Metadata:
    handler_name    : VideoHandler
  Stream #0:1(eng): Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 127 kb/s (default)
  Metadata:
    handler_name    : SoundHandler
  Stream #0:2(und): Data: none (rtp  / 0x20707472), 88 kb/s (default)
  Metadata:
    creation_time   : 2015-09-26 02:45:24
    handler_name    : GPAC ISO Hint Handler
  Stream #0:3(und): Data: none (rtp  / 0x20707472), 9 kb/s (default)
  Metadata:
    creation_time   : 2015-09-26 02:49:37
    handler_name    : GPAC ISO Hint Handler
```

I decided to do a git bisect and it blamed the following commit:







```
 (+) Video --vid=1 (*) (h264)
 (+) Audio --aid=1 --alang=eng (*) (aac)
Using hardware decoding.
AO: [pulse] 48000Hz stereo 2ch float
VO: [opengl] 640x360 vdpau
```



```
 (+) Video --vid=1 (*) (h264)
 (+) Audio --aid=1 --alang=eng (*) (aac)
Using hardware decoding.
AO: [pulse] 48000Hz stereo 2ch float
[ffmpeg/video] h264: get_buffer() failed
[ffmpeg/video] h264: thread_get_buffer() failed
[ffmpeg/video] h264: decode_slice_header error
[ffmpeg/video] h264: no frame!
Error while decoding frame!
Hardware decoding failed, falling back to software decoding.
VO: [opengl] 640x360 yuv420p
```

mpv output on v0.11.0:

```
 (+) Video --vid=1 (*) (h264)
 (+) Audio --aid=1 --alang=eng (*) (aac)
AO: [pulse] 48000Hz stereo 2ch float
Using software decoding.
VO: [opengl] 640x360 yuv420p
```

VLC correctly uses VDPAU hardware decoding for this file.

Best regards and thanks for your work on mpv,

Andreas
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `6875e6a77946de2cecbdbfc6e9930a79f31767e0` and the full history behind it is present.
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
