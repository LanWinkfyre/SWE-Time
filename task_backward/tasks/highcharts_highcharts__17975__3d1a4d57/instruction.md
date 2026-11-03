# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Dumbbell resize bug

#### Expected behaviour
When shrinking the window in the x-axis and then returning to its previous size, the chart also returns to its original state, the way it's displayed doesn't change.

#### Actual behaviour
When shrinking the window in the x-axis until the points on the chart disappear, returning to the previous size of the window causes the chart not to return to its original state. Displays incorrectly, points are still invisible.

#### Live demo with steps to reproduce
https://jsfiddle.net/BlackLabel/kvL340fa/

Steps:
1. Shrink the window with a chart to the minimum width.
2. Expand the window to its original width.

#### Product version
Highcharts v10.3.1 + Highcharts More + Dumbbell


Hi @Vazonik thank you for reporting that!

Internal note: 


Workaround:
Broken since v10.3.0 so you can use the previous version- [demo](https://jsfiddle.net/BlackLabel/kbfh7pd8/).
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `c4780cb830d3180b5eb67899c42461397c0c9179` and the full history behind it is present.
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
