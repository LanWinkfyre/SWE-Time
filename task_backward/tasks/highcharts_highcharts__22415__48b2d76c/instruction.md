# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
legend checkBox disappears after responsive layout change

#### Expected behaviour
When layout is changed with responsive setting, checkBox items are correctly displayed in legend

#### Actual behaviour
When layout is changed with responsive setting, checkBox items are disappear permanently

#### Live demo with steps to reproduce
https://jsfiddle.net/BlackLabel/zycaxsk6/
change size to below 400px, then return to wider screen, and note that checkboxes in legend disappear permanently.

#### Product version
Highcharts Core

Regression, last working version: 10.2.1

#### Affected browser(s)


<!-- ASANA TASK ID (do not delete): 1209015342147457 -->

The issue is not related to responsive rules logic. The issue can be reproduced with chart update: https://jsfiddle.net/BlackLabel/wjfgv9u2/

**Internal note**
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `8b71b62df6bf5292c4014e7fea3bde392886598b` and the full history behind it is present.
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
