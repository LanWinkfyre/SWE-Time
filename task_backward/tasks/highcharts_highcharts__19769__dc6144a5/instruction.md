# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
update in angular not working with v11.x.x 

Online example from https://github.com/highcharts/highcharts-angular
[Optimal way to update](https://stackblitz.com/edit/highcharts-angular-update-optimal-way)

is not working with version 11.x.x highcharts

#### Expected behaviour
title and series should be updated

#### Actual behaviour
only title is updated

#### Live demo with steps to reproduce
https://stackblitz.com/edit/highcharts-angular-update-optimal-way-reh7uy?file=package.json



Hi @lm2j! 

Thank you for reporting the issue! It looks like it has been broken since v.11.1.0.


 @TorsteinHonsi do you think that is something the Highcharts should handle or the integration `highcharts-angular` should work around?


As a workaround, you can use the `chartRef` obtained from the `chartInstance` emitter to update the chart- [demo](https://stackblitz.com/edit/highcharts-angular-update-optimal-way-umhi92?file=src%2Fapp%2Fapp.component.ts%3AL37,src%2Fapp%2Fapp.component.html).
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `46b7f455a1174eb8b7a971be4c7f5a91fa1d85da` and the full history behind it is present.
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
