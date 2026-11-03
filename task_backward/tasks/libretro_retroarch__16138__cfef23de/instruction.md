# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Closing Retroarch saves the active remap setting input_player1_analog_dpad_mode file to global config too.

## Description
Closing retroarch saves the active remap file setting relative to "Input_player1_analog_dpad_mode" to global settings too.

### Expected behavior
That setting should be tied to the remap file.


### Steps to reproduce the bug

* load Ikaruga
* Quick menu, controls, Save Game remap file
* From the menu, I read that Active remap file is set to Ikaruga, good.
* Then i set Port 1, Analog to digital: Left Analog
* Analog to digital works, good.
* Quit cleanly from Retroarch. (*see note*)
* Check the remap file and it has the correct input_player1_analog_dpad_mode = "1" line, good.
* Restart retroarch
* Check the input settings without loading anything
* See that Port 1 is set to Analog to digital: Left Analog


(*note*) Note that at that point, if, before closing retroarch, one selects "close content" then the issue is not present.


### Version/Commit
1.06.0.3

### Environment information
Archlinux build.


https://github.com/libretro/RetroArch/assets/1230726/2ba054ef-1bc8-4bdf-86ad-4e8deb81cb45
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `a99a7deab1d9a249f2347ce79b8d7e06be8386ce` and the full history behind it is present.
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
