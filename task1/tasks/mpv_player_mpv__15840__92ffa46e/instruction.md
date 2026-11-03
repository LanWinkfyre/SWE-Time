# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Unable to unset demuxer-lavf-format

### mpv Information

```bash
mpv 0.39.0 Copyright © 2000-2024 mpv/MPlayer/mplayer2 projects
libplacebo version: v6.338.2
FFmpeg version: 6.1.2
FFmpeg library versions:
   libavcodec      60.31.102
   libavdevice     60.3.100
   libavfilter     9.12.100
   libavformat     60.16.100
   libavutil       58.29.100
   libswresample   4.12.100
   libswscale      7.5.100
```

### Other Information

```text
- Linux version: Alpine Linux v3.21
- Kernel Version: 6.12.9-0-lts
- GPU Model: Intel Corporation Iris Plus Graphics G4 (Ice Lake) (rev 07)
- Mesa/GPU Driver Version: mesa-24.2.8
- Window Manager and Version:Cagebreak 2.4.0
- Source of mpv: Alpine Repository
- Latest known working version: 0.38.0
- Issue started after the following happened: upgrade to 0.39.0
```

### Reproduction Steps

Start mpv with:

```
 mpv --load-scripts=no --script=$(pwd)/mpv-sb.so --idle
```

`mpv-sb.so` is a work in progress c-plugin that sets `demuxer-lavf-format` based on header data sent by a media server. For files that the media server doesn't natively support, I need to unset `demuxer-lavf-format` and let mpv probe for the format to use. The below c-plugin code worked with mpv 0.38.0, allowing me to play a list of tracks and setting or unsetting `demuxer-lavf-format` as required for the track.

```
char *fmt;

 switch (msg.strm.mode) {
  case 'a': fmt = "aac"; break;
  case 'd': fmt = "dsf"; break;
  case 'f': fmt = "flac"; break;
  case 'm': fmt = "mp3"; break;
  case 'o': fmt = "ogg"; break;
  case 's': fmt = NULL; break;
  case 'u': fmt = "opus"; break;
  default: fmt = NULL;
}

mpv_set_property(g_handle, "demuxer-lavf-format", MPV_FORMAT_STRING, &fmt);
```

After playing a track that explicitly sets the format and then changing to a track that doesn't, which sets fmt = NULL, I now get:

```
[lavf] Unknown lavf format 
[lavf] Unknown lavf format 
A: 00:00:03 / 00:05:00 (1%)
Failed to recognize file format.
```
It seems that format is always set here now, even after trying to unset it. I tested with this patch and setting fmt = "none" above instead of NULL and that does restore the old behavior:

```
--- ./demux/demux_lavf.c
+++ ./demux/demux_lavf.c
@@ -448,7 +448,7 @@
         format = s->lavf_type;
     if (!format)
         format = avdevice_format;
-    if (format) {
+    if (format && strcmp(format, "none") != 0) {
         if (strcmp(format, "help") == 0) {
             list_formats(demuxer);
             return -1;​
```

I did a git bisect between 0.38.0 and 0.39.0 and this is the commit that broke it for me:




Is there something I should do differently to unset "demuxer-lavf-format" rather than setting it to NULL?

### Expected Behavior

Set and unset `demuxer-lavf-format` successfully.

### Actual Behavior

Unable to unset `demuxer-lavf-format` after setting it.

### Log File

[mpv.log](https://github.com/user-attachments/files/18722378/mpv.log)

I know that's not a proper log file. When I run with --log-file I get:
```
Assertion failed: str (../misc/json.c: write_json_str: 258)
```

### Sample Files

_No response_

### I carefully read all instruction and confirm that I did the following:

- [x] I tested with the latest mpv version to validate that the issue is not already fixed.
- [x] I provided all required information including system and mpv version.
- [x] I produced the log file with the exact same set of files, parameters, and conditions used in "Reproduction Steps", with the addition of `--log-file=output.txt`.
- [x] I produced the log file while the behaviors described in "Actual Behavior" were actively observed.
- [x] I attached the full, untruncated log file.
- [x] I attached the backtrace in the case of a crash.
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `e4b64fba9c5c6ca97189f32c056d05c2b47cebd6` and the full history behind it is present.
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
