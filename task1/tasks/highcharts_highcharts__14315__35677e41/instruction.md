# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Setting extremes on the histogram chart with no data to display generates an error in the console

#### Expected behaviour
Being able to set the extremes without error.

#### Actual behaviour
When the extremes for the histogram axis such that there is no data there to display, errors in console occurs.
```
"highcharts.src.js:3636 Error: <rect> attribute y: Expected length, "NaN"."
"highcharts.src.js:3636 Error: <rect> attribute height: Expected length, "NaN"."
```

#### Live demo with steps to reproduce
Click the button below the chart and check the console.
https://jsfiddle.net/BlackLabel/9yv5j6bq/

#### Product version
Highcharts JS v8.2.0

#### Affected browser(s)
All


*Internal note:*
It's a general, column-like series issue: https://jsfiddle.net/BlackLabel/dkwzt5e8/
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `c0dd6712d73fd73be9c67195a2ad65032ae684b5` and the full history behind it is present.
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
