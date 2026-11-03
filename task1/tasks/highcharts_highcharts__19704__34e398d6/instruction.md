# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Gantt charts exception in 11.1 vs 10.3.3

#### Expected behaviour
No exception

#### Actual behaviour
Exception reported
Uncaught TypeError: Cannot read properties of undefined (reading 'isActive')
    at highcharts-gantt.src.js:42112:33
    at Array.forEach (<anonymous>)
    at x.d [as drawDataLabels] (highcharts-gantt.src.js:41947:21)
    at x.render (highcharts-gantt.src.js:33503:21)
    at highcharts-gantt.src.js:36597:21
    at Array.forEach (<anonymous>)
    at B.renderSeries (highcharts-gantt.src.js:36595:17)
    at B.render (highcharts-gantt.src.js:36678:17)
    at B.firstRender (highcharts-gantt.src.js:36837:17)
    at B.<anonymous> (highcharts-gantt.src.js:35276:21)

Debugging shows that the datalabels array as a length of 3, with nothing at index 0.

This seems to correlate with the data that contains a first element that is empty:
 `    "dataLabels": [
      {}, 
      {
      "enabled": true,
      ...
`

#### Live demo with steps to reproduce
Run: https://jsfiddle.net/alpic80/wgdL5r3n/14/

switch script to 10.3.3 by uncommenting in header and error will go away.

#### Product version
Highcharts Gantt 11.1 (works in 10.3.3)

#### Affected browser(s)
All


Hello @castortech and thanks for reporting the issue.

_Internal note:_
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `0a045faee69f61563ddbbefb86d435ec1975c667` and the full history behind it is present.
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
