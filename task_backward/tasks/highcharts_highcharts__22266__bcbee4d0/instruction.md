# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression v12: TypeScript types missing/incorrect

#### Expected behaviour

* The `highcharts` module should export `PointLabelObject`
* Additionally, the type for `plotOptions.X.dataLabels.formatter` has changed from `(this: PointLabelObject) => string` to `(this: Point) => string`, but it really is still a `PointLabelObject`.

#### Actual behaviour

* `PointLabelObject` has been removed
* The type for `plotOptions.X.dataLabels.formatter` should be correct.

#### Live demo with steps to reproduce

N/A

#### Product version

Highcharts Core v12

#### Affected browser(s)

N/A

<!-- ASANA TASK ID (do not delete): 1208901721897331 -->

_Internal note_
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `6cbbb6317a756821daea6af2c3f56db8e35c7167` and the full history behind it is present.
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
