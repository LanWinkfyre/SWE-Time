# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[4.8] Opening a Doc of a GDScript and restarting the editor results in a an empty "Unknown Help Class" tab

### Tested versions







CC @kitbdev 

### System information

 32.0.15.9227) - AMD Ryzen 5 5600H with Radeon Graphics (12 threads) - 31.34 GiB memory - WASAPI (48000 Hz, Stereo/mono)

### Issue description

Bug identified by YeldhamDev

After restarting the editor, docs of custom scripts turn into these "Unknown Help Class" tabs. In 4.7 they close on restart, but  they become the "Unknown Help Class".

<img width="908" height="485" alt="Image" src="https://github.com/user-attachments/assets/297f5a7a-3f5d-44f6-92bd-19d6e8e76716" />

### Steps to reproduce

1. Open the MRP
2. Open the Script Editor
3. Press "Search Help"
4. Type "new_script"
5. Open "new_script.gd"
6. Restart the editor (Project > Reload current project)
7. Open the Script Editor
8. Look at the tabs

### Minimal reproduction project (MRP)

[mrp.zip](https://github.com/user-attachments/files/30797804/mrp.zip)
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `51105ccbe58381774ecd7a7486d564b202a5192e` and the full history behind it is present.
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
