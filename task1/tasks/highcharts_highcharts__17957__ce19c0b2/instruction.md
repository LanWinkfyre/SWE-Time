# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Data label disappears on hover

#### Expected behaviour
Data label persist on hover

#### Actual behaviour
Data label disappears on hover

#### Live demo with steps to reproduce
https://jsfiddle.net/qhwz90nL/

Removing off the `marker.enabled: false` bit, the issue is resolved.
https://jsfiddle.net/qhwz90nL/1/

#### Product version
Presumably originating in the Accessibility module.


#### Affected browser(s)
FF, Chrome


Hi @kluvin and thank you for reporting that issue!

_Internal note:_

FYI @TorsteinHonsi
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `a0f343a71759c824743fa2c03fead7f3a36c9c4a` and the full history behind it is present.
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
