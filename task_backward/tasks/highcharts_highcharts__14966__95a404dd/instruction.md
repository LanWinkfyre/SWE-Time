# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Accessibility module included & point y value null leads to errors in browser console

#### Expected behaviour
No errors in console. 

#### Actual behaviour
In case the accessibility module is included, there is a error (or multiple errors) in the console when selecting a point whose y value is null programmatically:
Error: <rect> attribute y: Expected length, "NaN".

In addition, the point that is added in the DOM has a y value of NaN.

![image](https://user-images.githubusercontent.com/77784146/105348348-84979900-5be8-11eb-95d7-a6acaad74776.png)

#### Live demo with steps to reproduce
https://jsfiddle.net/L8kaxdpw/20/

Rerpo steps:

1. Open attached jsfiddle
2. Open browser dev tools
3. Click on the button and check the console afterwards (not the console in jsfiddle but the actual browser console)

#### Product version
I was able to reproduce it in Highcharts 8.1.2 and 8.2.2


Hi @kemusag 

Thank you for contacting us and reporting this issue. It happens when the value of a point is `null` and the dummy point for the accessibility purpose is created. It eventually leads to setting a `y` attribute with `NaN` value.

**Workaround**
https://jsfiddle.net/BlackLabel/ayb1v4on/

_Internal note_
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `1671b3875eea1385ea02df42d219f154212f760f` and the full history behind it is present.
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
