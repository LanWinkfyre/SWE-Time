# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Treemap - data labels issue

In the treemap chart, long data labels are rendered wrong when useHTML feature is set to true. 

Last working versions, where data labels were rendered as users expect is 7.0.1 - [demo](https://jsfiddle.net/BlackLabel/572rya6b/)

Temporary [workaround](https://jsfiddle.net/BlackLabel/aqyjh7zu/). 

Could be related to: [#8160](https://github.com/highcharts/highcharts/issues/8160)

#### Live demo with steps to reproduce

[Demo](https://jsfiddle.net/BlackLabel/xc8zr7d2/)

#### Product version
versions > 7.0.1
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `53d9bed3abd49e160290fad5c95ffa446fe72244` and the full history behind it is present.
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
