# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Bubble chart omits axis labels for empty edge categories

#### Expected behaviour
In a bubble chart with categories specified, all categories should be visible on the axis and have labels, even if no data points exist in those categories.

#### Actual behaviour
Axis labels are only rendered for:
- Categories with data points
- Categories that are between other categories with data points

#### Live demo with steps to reproduce
https://jsfiddle.net/fvLo5k92/

- Categories 1 to 5 are defined (values 0 to 4) but only categories 2 to 4 are visible.
- If you change the values of the bubbles to `{ x: 2, y: 2 }`, only the 3rd category will displayed
- If you change `chart.type` to `'scatter'` - the labels will be displayed as expected

Additional notes:
- If you remove `min` and `max` from the `xAxis`, the xAxis will resize and the empty categories are not rendered at all
- If you remove `min` and `max` from the `yAxis`, the yAxis will not resize and still display empty space without labels

#### Product version
12.2.0

#### Affected browser(s)
Chromium-based browsers (others not tested)

<!-- ASANA TASK ID (do not delete): 1210250750242648 -->

Thank you for reporting this!

I’ve confirmed that this is a regression.
**Last working version:** 11.4.8


As a temporary workaround, you can apply the following fix:
https://jsfiddle.net/BlackLabel/b2cw7mfx/

Feel free to follow the ticket for any updates on its progress. Regards!
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `420fc9c6f8b30b9fdccb42131020895ca08b19d4` and the full history behind it is present.
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
