# Locate the commit that introduced this regression

A regression was reported against `prometheus/prometheus`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
retention shown in runtime page set to 0s

In Prometheus 2.8-rc0 the runtime page shows '0s' retention.

2.7.1:
![retention](https://user-images.githubusercontent.com/291750/54060292-7579ee80-41fc-11e9-9c74-d00667ba333d.png)

2.8-rc0:
![retention2](https://user-images.githubusercontent.com/291750/54060359-b6720300-41fc-11e9-83bc-fa316efd143f.png)



Bisect:
```

## What you have

- `/testbed/repo` is a git clone of `prometheus/prometheus` truncated just after the regression was
  reported.  `HEAD` is `d390497280d61918aa8792f87a2f458e5e231ec2` and the full history behind it is present.
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
