# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Main window is blank on MS WinXP 32-bit

## Description

Main window is blank

### Expected behavior

When I launch RetroArch, I get an empty console window and a small blank window. It essentially retains whatever picture was under it the moment it was opened. As far as I understand, this is supposed to be the main RetroArch UI, because pressing F makes it go fullscreen and double tapping Esc makes the window go away, while single Esc presses do nothing.

### Actual behavior

When I launch RetroArch, I get an empty console window and a small window containing the configured RetroArch UI.[
The verbose console output](https://pastebin.com/ShApdPiG)

### Steps to reproduce the bug

Run RetroArch

### Bisect Results

Right after installation

### Version/Commit

- RetroArch: v1.14.0, Compiler: MSVC 1600 32-bit Built: Dec 13 2022

### Environment information

- OS: Windows XP 32 Bit SP3
- [`systeminfo` command output](https://pastebin.com/FQ4hSML3)

### Attempted Troubleshooting

I’ve tried all the listed available video drivers (gl, gl1, d3d8, null), to no avail. I’ve also cycled between rgui, xmb and ozone for every driver. That didn’t help. None of the configurations worked, all drivers except null showed the same blank window.
Rebooting several times and reinstalling DX9 didn’t help, too.

####  [Related Forum Topic](https://forums.libretro.com/t/retroarch-on-winxp-32-bit-transparent-window/40195)




![image](https://github.com/libretro/RetroArch/assets/33353403/c51a69cd-ebc8-43fe-aabd-e3e92a64429f)



![image](https://github.com/libretro/RetroArch/assets/33353403/b916c8e7-c3e8-4a13-a3a9-e282b8c2fbcf)

I even installed a Windows XP VM just for this! So I really hope it will help solving this long standing issue!
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `e10361ed529cd07651012f0437911e7f5d9f2bdd` and the full history behind it is present.
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
