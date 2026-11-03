# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
file-size and stream-end properties are 0 when opening local files paused

### Important Information

Provide following Information:

- Platform and Version: openSUSE Tumbleweed 20231106
- Source of the mpv binary: built using mpv-build

When opening local files with `pause`, the properties `file-size` and `stream-end` are `0` instead of the actual file's size.
Simply waiting does not result in mpv updating them to the correct value.
Unpausing, or seeking **does** update them.




### Reproduction steps

1. create `input.conf` to easily check `file-size` and `stream-end` properties: `F2 print-text "file-size: ${=file-size} - stream-end: ${=stream-end}"`
2. open (video) file with mpv, paused `mpv test_file.mkv --no-config --pause --input-conf=input.conf`
3. press F2 key

### Expected behavior

`file-size` and `stream-end` properties are set the actual file's size,
mpv prints e.g. `file-size: 1422859102 - stream-end: 1422859102`

### Actual behavior

`file-size` and `stream-end` properties are both set to `0`,
mpv prints `file-size: 0 - stream-end: 0`
Only unpausing or seeking updates both properties.

### Log file
https://0x0.st/HtFF.txt
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `438ead7a3d50468b8150f2dc2727b96c78db9874` and the full history behind it is present.
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
