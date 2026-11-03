# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Cannot see a line series that is touching the x-axis

#### Expected behaviour

In 10.3.3, we can notice that series line from x=1 to 2 is touching the x-axis and is visible.

Link: **https://jsfiddle.net/hby5Loxg/**

![image](https://github.com/user-attachments/assets/1439a68f-e2bd-4721-8004-b7d42088cab8)


#### Actual behaviour

In 11.4.8, we cannot see the series line from x=1 to 2.

Link: **https://jsfiddle.net/hby5Loxg/1/**

![image](https://github.com/user-attachments/assets/1f54b9c9-5564-45b1-83d5-53cd78518054)


I found a workaround by setting `chart.plotBorderWidth` to `0` but we want to keep the border.

#### Live demo with steps to reproduce
(Given above)

#### Product version
Highcharts 11.4.8


#### Affected browser(s)
Tried on Chrome

<!-- ASANA TASK ID (do not delete): 1209068777757214 -->

Hi @nishikantparmariam! Thank you for reporting the issue.

As a workaround I've prepared a simple plugin for you: https://jsfiddle.net/BlackLabel/cux60qev/ The logic adds some additional offset, based on line width to the chart clip box.

_Internal note_
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `7d12b6296615ffdc7cc976b54db5c23038b37d01` and the full history behind it is present.
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
