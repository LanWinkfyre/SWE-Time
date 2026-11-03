# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Unable to see achievement's description when using RGUI

## Description

In 1.7.2+ it's impossible to see the Achievement description while using RGUI.

### Expected behavior

See the achievement's description, like this:

![rgui-cheevosdescription](https://user-images.githubusercontent.com/8508804/39888380-01b4d99e-546b-11e8-9e4f-673351301258.png)


### Actual behavior

Not seeing the achievement's description, like this:

![rgui-cheevosnodescription](https://user-images.githubusercontent.com/8508804/39888682-eb7f9c8a-546b-11e8-99dd-b0c7dd00ad7e.png)




### Steps to reproduce the bug

1. invoke RGUI -> Quick Menu -> Achievements
2. put the cursor in any achievement and press `Select`
3. the achievement description doesn't appear and the top screen's title now says SELECT FILE (NULL).


### Bisect Results



### Environment information

- OS: noticed this issue while running 1.7.2 on a Raspberry pi (RetroPie) and confirmed on Linux.
- Compiler: gcc
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `c3c50bae299d72ba44bf577ec79060407e69197d` and the full history behind it is present.
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
