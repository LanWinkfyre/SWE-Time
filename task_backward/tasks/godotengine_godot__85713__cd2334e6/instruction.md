# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Setting mouse mode to confined causes TextureButton hover to stop working (new -after upgrading to Godot 4.2 from 4.1.1)

### Godot version



### System information

Godot v4.2.stable.mono - Fedora Linux 38 (Thirty Eight) - X11 - Vulkan (Forward+) - dedicated NVIDIA GeForce GTX 1650 SUPER (nvidia; 545.29.06) - Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz (8 Threads)

### Issue description

I updated my project from 4.1.1 to 4.2. I noticed that the TextureButton hover textures stopped appearing. After some experimentation I narrowed it down to occurring after setting mouse mode to confined.

### Steps to reproduce

1. Make a new project
2. Make a new scene with TextureButton
3. Attach a script and set mouse mode to confined
4. Play the scene and moving the cursor over the TextureButton doesn't result in the hover texture

### Minimal reproduction project

- texture_button.tscn shows the issue with a C# script
- texture_buttongd.tscn shows the issue with a GDScript script

[hover_issue.zip](https://github.com/godotengine/godot/files/13539694/hover_issue.zip)
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `d76c1d0e516fedc535a2e394ab780cac79203477` and the full history behind it is present.
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
