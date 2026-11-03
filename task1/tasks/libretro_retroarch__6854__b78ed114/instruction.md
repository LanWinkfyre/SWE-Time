# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[Regression] Thumbnails not shown in Quick Menu or when returning to "Run" menu after closing content

## Description

When launching a game from a playlist, the thumbnail is correctly shown when selecting "Run". After the game has launched and you enter the Quick Menu, the thumbnail is not shown. After choosing "Close content" to quit the game and get back to the playlist entry launch ("Run") menu, the thumbnail is no longer shown. When pressing back to return to the playlist, the thumbnail reappears.

### Expected behavior

The thumbnail shall be shown in the Quick Menu and when returning to the playlist item launch menu after choosing to close content.

### Actual behavior

See description.

### Steps to reproduce the bug

1. Select a playlist item with a thumbnail and press OK.
2. Before pressing OK again to run the content, note that the thumbnail is still shown.
3. After launching the content, go into the Quick Menu. Note that the thumbnail is not shown, which it should be.
4. Choose "Close content" to return to the playlist item launch menu. Note that the thumbnail is no longer shown.
5. Press back to return to the playlist. The thumbnail is now shown.

### Bisect Results



### Environment information

Same issue verified on both Linux and Windows.
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `861d87281ee075eb811f77ad83d6115c396763e1` and the full history behind it is present.
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
