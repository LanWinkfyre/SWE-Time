# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
RGUI menu display regression (Linux/KMSDRM)

### Is there an existing issue for this?

- [X] This is a bug in RetroArch frontend
- [X] I have searched the existing issues

### Description

 The same configuration that was used before would center the RGUI menu, but after the commit in question the menu is displayed close to the right side. The issue occurs using a wide-screen (1080p, 4k) resolution.

 The configuration used is _Aspect Ration = 4:3_ (using _Auto_ instead of _4:3_ yields the same result) and _Lock Aspect Ration = Off_ (I think this is the default). See the picture below:

![image](https://github.com/user-attachments/assets/d0dc1b0f-3c1d-4656-8e59-1aef3a1e84df)

The issue is also that opening the menu during gameplay will also switch the underlying game viewport to the right after exiting, breaking the original alignment (centered) of the game viewport.



### Expected behavior

RGUI menu to be centered.

### Steps to reproduce the bug

* Start RetroArch with `--menu` or open the Menu
* Change the display driver to **RGUI** and then in **Settings -> User Interface -> Appearance** set _Aspect Ratio_ to _4:3_.
* On a wide screen, notice how the RGUI is not centered to the screen/viewport, but aligned to the right side.

### Version/Commit



### Bisect Results



### Present in the nightly version

I don't know

### Platform & operating system

Linux aarch64, KMSDRM video driver, GL renderer

### Affected Cores

any

### Environment information

* Linux aarch64 (Pi4 with current RaspiOS, based on Debian 12 bookworm).
* KMSDRM display driver (haven't tested on other systems like X11 or Win32)
* GL video driver

### Relevant log output

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `f2a86f34d136952be35cdbde42335d27cb15e774` and the full history behind it is present.
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
