# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
grid line placement broken for single category y axis

#### Expected behaviour
There should be a grid line on the top of the axis and one on the bottom.

#### Actual behaviour
The top grid line has moved to the middle, going straight through the points.

#### Live demo with steps to reproduce
broken in 7.0.2: https://jsfiddle.net/w0xfr2d3/
working in 7.0.1: https://jsfiddle.net/qu1pc5z2/

This only happens when there is only one category.

#### Product version
Highcharts 7.0.2 and above

#### Affected browser(s)
Firefox, chrome, Internet Explorer 11


Thank you for reporting this regression @robahs 

**Workaround:**
Disable `yAxis.startOnTick`, `yAxis.endOnTick` and modify a bit `yAxis.min` and `yAxis.max`: https://jsfiddle.net/BlackLabel/9x7w5yrf/ 

Snippet:
```js
    yAxis: {
        ...
        startOnTick: false,
        endOnTick: false,
        min: -0.1,
        max: 0.1
    },
```

*Internal note:*
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `1f755c038050548d02f3192d2a250d82ae2cbddf` and the full history behind it is present.
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
