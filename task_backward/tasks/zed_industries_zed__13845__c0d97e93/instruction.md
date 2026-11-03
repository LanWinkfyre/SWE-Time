# Locate the commit that introduced this regression

A regression was reported against `zed-industries/zed`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
margin padding on Linux

### Check for existing issues

- [X] Completed

### Describe the bug / provide steps to reproduce it



there are margins around the window now, as shown in the screenshot. I'm running Xmonad as a window manager, if that's relevant.










### Environment


OS: Linux X11 linuxmint 21
Memory: 125.6 GiB
Architecture: x86_64

### If applicable, add mockups / screenshots to help explain present your vision of the feature

![margins](https://github.com/zed-industries/zed/assets/68482/a47be209-a8ed-46da-ba08-ca6e5e347912)


### If applicable, attach your `~/Library/Logs/Zed/Zed.log` file to this issue.

<details><summary>Zed.log</summary><pre>
<!-- Click below this line and paste or drag-and-drop your log-->

<!-- Click above this line and paste or drag-and-drop your log--></pre></details>
```

## What you have

- `/testbed/repo` is a git clone of `zed-industries/zed` truncated just after the regression was
  reported.  `HEAD` is `c8b106245c7e62353e0cd595213b166e03378130` and the full history behind it is present.
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
