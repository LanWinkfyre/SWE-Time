# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Rendering errors on Mobile and Compatility renderer using Godot 4.3 Beta 3

### Tested versions

- Reproducible in: 4.3-beta3.  - Not reproducible in: 4.3-beta2, 4.3-beta1, 4.3-dev6

### System information

Godot v4.3.beta3 - Arch Linux #1 SMP PREEMPT_DYNAMIC TKG Fri, 21 Jun 2024 13:02:41 +0000 - Wayland - Vulkan (Mobile) - dedicated NVIDIA GeForce GTX 1060 6GB (nvidia; 555.58.02) - AMD Ryzen 5 1600 Six-Core Processor (12 Threads)

### Issue description

When I launch the game using the Mobile or the compatibility renderers, he game renders with darker colors. It looks like if the light is not being correctly rendered. When I launch the game in my Android phone via remote depuration, it renders incorrectly in both rendererers, and in my computers it only looks wrong in Compatiblity one. This is only happening in Godot 4.3-beta3

This is the game running in Godot 4.3-beta2
![Screenshot_20240711-201748](https://github.com/godotengine/godot/assets/57129654/43484ac4-dd67-4f53-bfef-d478bc3c31b8)

And this is in Godot 4.3-beta3
![Screenshot_20240711-200738_TFG](https://github.com/godotengine/godot/assets/57129654/aaa95cb2-300e-4d70-b112-01bfc759d355)


### Steps to reproduce

- Install Godot 4.3 beta3
On phone:
- Set the renderer to Mobile or Compatibility
- Connect the phone via USB
- Start remote depuration on any scene
On PC:
- Set the renderer to Compatibility
- Start the game on any scene

### Minimal reproduction project (MRP)

[MRP.zip](https://github.com/user-attachments/files/16182393/MRP.zip)




CC @m4gr3d 

I think I have a fix already, testing now
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `383a6e4ef285fddcb0e1cbe28a20332c7e5a815b` and the full history behind it is present.
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
