# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[CRASH] Opening a Browse File window from the Project Manager crashes the editor

### Tested versions





### System information

Godot v4.6.dev4 - Windows 10 (build 19045) - Multi-window, 3 monitors - Vulkan (Forward+) - dedicated NVIDIA GeForce RTX 3080 (NVIDIA; 32.0.15.6590) - 12th Gen Intel(R) Core(TM) i7-12700K (20 threads) - 31.74 GiB memory

### Issue description

Opening a Browse File or Browse Folder window while accessing the Editor Settings from the Project Manager will crash the editor.

Here is a log from this crash. I don't get any more information than "<couldn't map PC to fn name>" in the backtrace, even on custom builds.



### Steps to reproduce

1. Open the Godot Editor, displaying the Project Manager.
2. Go to Settings -> Edit All Settings, displaying the Editor Settings.
3. Open a file dialog (for example, go to General -> FileSystem -> Directories and click the folder button next to Default Project Path).

The editor will crash.

### Minimal reproduction project (MRP)

N/A (the bug is visible without any project).



That was a good use of time 😅
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `ef34c3d534a16b140aef0643ed2fa36f8e9d1612` and the full history behind it is present.
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
