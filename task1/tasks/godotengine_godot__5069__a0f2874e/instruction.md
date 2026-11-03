# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
AnimatedSprite3D doesn't recognize its frames

**OS, GPU, Version** 
Linux 4.5.2 x86_64 01:00.0 
VGA compatible controller: NVIDIA Corporation GK106 [GeForce GTX 645 OEM](rev a1)
"Nouveau" driver


**Issue description** 
The AnimatedSprite3D doesn't recognize its frames.
No frame is displayed in editor and when running it in editor.
Git bisect hints that it might also be the case for AnimatedSprite(2D) but I haven't tested it yet.

**Steps to reproduce:**
Start the editor
Create a new AnimatedSprite3D
Load frames into the AnimatedSprite3D
-> Nothing is displayed in editor, current frame can't be changed.
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `955ed0a95f61e14e6c941540b11905a16fb40d00` and the full history behind it is present.
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
