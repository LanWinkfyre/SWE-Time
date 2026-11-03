# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
**Godot version:**
3.1 beta 7


**OS/device including version:**
Mac OS
AMD Radeon R9 M370X


**Issue description:**
The TPS Demo from Godot is pixelated after start. (Not Main Menu)
Testing the same Project with Godot 3.1 beta 3 and everything works fine.
So something must be wrong with Godot 3.1. beta 7


**Steps to reproduce:**
Just open and run the TPS Project.
Issue appears with beta 7, with beta 3 it's all fine

<img width="1920" alt="bildschirmfoto 2019-02-25 um 03 03 44" src="https://user-images.githubusercontent.com/47374234/53309790-189c4100-38aa-11e9-859e-a6236df83f42.png">
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `74d0ed2236b333d0a292e15b9c2a9380c2c122a1` and the full history behind it is present.
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
