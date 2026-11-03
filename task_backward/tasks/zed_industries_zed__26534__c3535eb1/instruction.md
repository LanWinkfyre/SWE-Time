# Locate the commit that introduced this regression

A regression was reported against `zed-industries/zed`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
MacOS: Open project in new window broken, window shows native window tabs (regression)

### Summary

On the current build on main, opening a project in a new window is severely broken on MacOS. If you open another project in a new window, the window initiating the open turns black. Instead, the new window now shows native window tabs, but these are broken aswell. 

Aditionally, every window now shows native window tabs even if only one project is open, making the title bar excessively large.

 

Steps to trigger the problem:
1. Open any project in Zed.
2. Open the "Recent Projects" menu.
3. Select any project from the list and open it with CMD + Enter (to open in a new window).

Actual Behavior:

One window becomes black and partly unresponsive, the other window shows native window tabs which are not usable. The title bar is larger and shows native window tabs, however these disappear once you click on the tab corresponding to the black window.

<details><summary>Video of the behaviour on my machine</summary>
<video src="https://github.com/user-attachments/assets/29c4d22a-aeab-412f-81bc-41797e6b3530" width="100%"></video>
</details> 

<details><summary>Repoening Zed after closing it with CMD+Q</summary>
<img width="1680" alt="Image" src="https://github.com/user-attachments/assets/0b63b200-037d-4624-93c7-59fe108e3a4a" />
</details>

<details><summary>Zed showing native window tabs and thus a bigger title bar</summary>
<img width="1680" alt="Image" src="https://github.com/user-attachments/assets/4aa70145-5814-4c43-9c3e-6d487de6fce8" />
</details>

Expected Behavior:




### Zed Version and System Specs


OS: macOS 15.0.1
Memory: 8 GiB
Architecture: aarch64
```

## What you have

- `/testbed/repo` is a git clone of `zed-industries/zed` truncated just after the regression was
  reported.  `HEAD` is `f3f97895a93681ca0e27195ecb1b0fdd21e01042` and the full history behind it is present.
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
