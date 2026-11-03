# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Shadows from DirectionalLight don't show any more

**Operating system or device - Godot version:**
Linux 4.8.11, godot  (master)
NVIDIA Corporation GK106 [GeForce GTX 645 OEM] with nouveau driver, mesa 12.0.6

**Issue description:**
Shadows from DirectionalLight sources don't show up any more. OmniLight and SpotLight work as intended though. I traced the problem back to the following commit:





**Steps to reproduce:**
Add a DirectionalLight and enable shadows. The shadows will not show up, instead all models in the scene will get slightly darker.
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `b19c9bd1983b8c72621595b7c22daade4ebf6625` and the full history behind it is present.
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
