# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Vulkan: Screen Space Reflection not working

**Godot version:**


**OS/device including version:**
MX Linux (Debian Based)
Nvidia GT 1030

**Issue description:**
SS reflection not working  properly

**Steps to reproduce:**
Create a simple scene with some meshes
Add world environment
Add sky
Add SS reflection.

Weird glitch appear

![ssreflection](https://user-images.githubusercontent.com/1168582/102703485-29bbfc00-424e-11eb-9052-942eb9831891.gif)


SSR in Vulkan has been broken a for a few months now (since the introduction of SDFGI or so).
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `e9d12f9e4ea30a6c3f2cf179f104a153d668c2a3` and the full history behind it is present.
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
