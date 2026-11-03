# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
When switching from pattern fill to solid fill there is a moment where the colors are all black


#### Expected behaviour
When changing from a pattern fill to a solid color, the change should be immediate with no period of black fill.

#### Actual behaviour
When switching from pattern fill to solid colors, there is a moment where the fill is black before changing to the correct solid color.

#### Live demo with steps to reproduce
https://jsfiddle.net/6orega9s/

1. Click "Enable pattern fill" button. This works correctly
2. Click "Disable pattern fill" button. There is a brief period where the bars are black before changing to the correct color

The issue appears to be that there is an animation using the `color-mix()` CSS function. The `color-mix()` function doesn't support the `url()` value used by the pattern fill.

#### Product version
12.2 & 12.3 (No problem in 12.1)

#### Affected browser(s)
Tested on Chrome

<img width="833" height="315" alt="Image" src="https://github.com/user-attachments/assets/7c101c13-b4cf-4ffb-8499-99b1c4226920" />

<!-- ASANA TASK ID (do not delete): 1210938351271707 -->

Thank you for reporting!

This is a regression and it has been added to our backlog. As a temporary workaround, you can use the following patch from the demo: https://jsfiddle.net/BlackLabel/s9j5fvx8/

---
Internal note:
Last working version: 12.1.2
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `c3cebbf82b7ea1f42455cdd6f1dfd0fb9562b0d9` and the full history behind it is present.
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
