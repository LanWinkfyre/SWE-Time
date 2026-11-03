# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
**Godot version:** 3.2 RC1 official
(3.2 beta 6 works, is without the problem)

**OS/device including version:** Windows 8.1 (64bit)
AMD A8-6410 APU with AMD Radeon R5 Graphics

Driver package version - 13.302.1501-140320a-169666C-Toshiba
2D Driver Version - 8.1.1.1634
OpenGL® Version - 25.20.15000.13547
OpenCL™ Version - 10.0.2766.5
AMD Mantle Version - 9.1.10.0295
AMD Mantle API Version - 102400
(Wasn't sure which are relevant, so copying more)

**Issue description:**
Whenever i try to open a project, i get a popup about AMD display driver that crashed and was recovered while in the meantime the editor during splash screen stops responding (when i try to close it i get the info visible below). The prompt shows basically nothing.
![obraz](https://user-images.githubusercontent.com/51792746/72622877-65ff2200-3944-11ea-82c3-76db629bb190.png)
![Crash](https://user-images.githubusercontent.com/51792746/72621293-43b7d500-3941-11ea-9798-85e2cac8dbb1.PNG)
**Steps to reproduce:**
Try to open any project while using AMD?
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `e7ee9e01a64bb1296431d82f9f1d888a90b6ea1c` and the full history behind it is present.
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
