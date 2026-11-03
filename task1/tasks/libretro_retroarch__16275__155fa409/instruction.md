# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Upside-down image sent to AI translation service when using HW renderer

## Description

When using the AI translation hotkey with a HW rendered core, the screenshot is sent upside-down to the translation server, making the translation impossible.

For example this is my RetroArch window:

![image](https://github.com/libretro/RetroArch/assets/33353403/42e164f1-8c65-4153-8a1c-697ab795b6b7)

and this is what the translation server received:

![image](https://github.com/libretro/RetroArch/assets/33353403/91dac11f-bf88-4922-a6aa-c488ce32f19f)

AFAICT it doesn't happen with software rendered cores.

### Expected behavior

Send screenshot in the correct position.

### Actual behavior

Send screenshot upside-down.

### Steps to reproduce the bug

1. Set AI translation stuff (AI service and a AI hotkey).
2. Start a game with a HW rendered core (I was able to reproduce with Beetle PSX HW, SwanStation and Flycast).
3. Press the AI hotkey, translation should be gibberish.
4. Check your last screenshot sent on the AI translation website you used.

### Bisect Results



### Version/Commit



### Environment information

- OS: Windows 10 but @Sanaki confirmed it happening on Linux as well
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `70daba65942d9b4695d83a28511c2e2b7e8f3d53` and the full history behind it is present.
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
