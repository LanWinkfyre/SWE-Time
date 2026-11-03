# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
mouse over in preview area moves the section

When zooming in the selection frame is floating around along to mouse movments after an initial dragging in the preview. 
It needs pressing a key thats not defined to be used with mouse movements (e.g. Esc key) to leave the preview area without changing the selection frame.


**To Reproduce**
1. Use current master
2. open image in darkroom and zoom in
2. place mouse pointer in preview area
3. move around without pressing a button
4. the selection frame follows your mouse

**Which commit introduced the error**
t.b.d


**Platform**
* darktable version : current master 3.7.0+833~g307903a2a
* OS                : Win10, also OSX


bisecting done:
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `f5720d246a8f2289c77192a9e388a137957c92fa` and the full history behind it is present.
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
