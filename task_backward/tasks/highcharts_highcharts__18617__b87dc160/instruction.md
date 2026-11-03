# Locate the commit that introduced this regression

A regression was reported against `highcharts/highcharts`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Stacklabels positioned incorrectly on bar chart with multiple grouped stacks

#### Expected behaviour
Numbers should appear at the end of the corresponding bar

This works fine as column, but not as bar:
https://jsfiddle.net/n2mpzw1r/

#### Actual behaviour
Numbers appear on different bars than they correspond to

#### Live demo with steps to reproduce
https://jsfiddle.net/bcvha0ns/9/ - 2 grouped stacks
https://jsfiddle.net/bcvha0ns/11/ - 3 grouped stacks

#### Product version
Latest

#### Affected browser(s)
Tested with Edge & Chrome

Hi @mharaguchi! 
Thank you for reporting the issue.



FYI @pawellysy
```

## What you have

- `/testbed/repo` is a git clone of `highcharts/highcharts` truncated just after the regression was
  reported.  `HEAD` is `e0b0d6411d9bd81a09357f7b752e26b0296bb507` and the full history behind it is present.
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
