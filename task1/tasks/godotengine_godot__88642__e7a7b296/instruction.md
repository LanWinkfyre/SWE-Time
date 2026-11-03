# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Viewport related settings are not updated realtime

### Tested versions


Godot v4.3 dev3 (for comparison)

### System information

 31.0.15.4592) - 13th Gen Intel(R) Core(TM) i7-13700F (24 Threads)

### Issue description

Tuning parameters that related to 3d viewport, such as scaling ratio and antialiasing options, seems have no effect, until reloading the whole project.
Tested on Godot v4.3 dev3, and everything works fine.

https://github.com/godotengine/godot/assets/33864304/97427428-1c3f-43ab-bdd1-e1444d8c97e7


### Steps to reproduce

1. Open the Minimal Reproduction Project using the latest build
2. Open project settings, and play around Scaling 3D-Scale, and antialiasing options

### Minimal reproduction project (MRP)

[MRP.zip](https://github.com/godotengine/godot/files/14363391/MRP.zip)




 cc @KoBeWi
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `16d61427cab3a8e43f0a9a8ee724fc176b6433c6` and the full history behind it is present.
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
