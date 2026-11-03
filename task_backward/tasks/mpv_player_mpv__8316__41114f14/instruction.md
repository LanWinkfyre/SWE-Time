# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
PCM audio output produce broken file after v0.33.0 update

I'm using mpv to record audio streaming by specifying `--ao=pcm --ao-pcm-file=test.wav` options. However, the output files can't be played properly after v0.33.0 update.

### Important Information

- mpv version: v0.33.0
- Linux Distribution and Version: Arch Linux 5.9.10-arch1-1
- Source of the mpv binary: [Arch repository](https://www.archlinux.org/packages/community/x86_64/mpv/)
- If known which version of mpv introduced the problem: v0.33.0
- Window Manager and version: sway version 1.5-96578aa9 (Oct 31 2020, branch 'master')
- GPU driver and version: 00:02.0 VGA compatible controller: Intel Corporation 3rd Gen Core processor Graphics Controller (rev 09)
- Possible screenshot or video of visual glitches: None

### Reproduction steps

1. Execute the following commnad to record audio for 10 seconds

```
$ timeout 10s mpv --no-config "http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk" --ao=pcm --ao-pcm-file=test.wav
```

2. Play the output file, but audio is broken

```
$ mpv test.wav
```

3. By downgrading mpv to the previous version, the output audio file works fine.

```
$ sudo pacman -U /var/cache/pacman/pkg/mpv-1:0.32.0-6-x86_64.pkg.tar.zst
```

### Expected behavior

The output audio files can be played properly.

### Actual behavior

The output audio files are broken.

### Log file

[mpv_output.log](https://gist.github.com/ynakao/f8852e5d6a34924dcac0453320f95b84)

Log generation command

```
$ timeout 10s mpv --no-config "http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk" --ao=pcm --ao-pcm-file=test.wav --log-file=mpv_output.log
```

### Sample files

None.

 



Also, as a workaround -- or maybe a better solution anyway? -- encoding mode seems to work: `mpv --o=test.wav 'http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk'`
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `fa7afc3e19acffd3198fdc8fddb671013a337b05` and the full history behind it is present.
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
