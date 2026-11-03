# Locate the commit that introduced this regression

A regression was reported against `ray-project/ray`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
CI test linux://python/ray/tests:test_channel is consistently_failing

CI test **linux://python/ray/tests:test_channel** is consistently_failing. Recent failures: 
	- https://buildkite.com/ray-project/postmerge/builds/4400#018f6537-f627-42c9-a037-195010e2b35c
	- https://buildkite.com/ray-project/postmerge/builds/4400#018f6537-f623-449e-a07b-e99c4a177a24

DataCaseName-linux://python/ray/tests:test_channel-END
Managed by OSS Test Policy
```

## What you have

- `/testbed/repo` is a git clone of `ray-project/ray` truncated just after the regression was
  reported.  `HEAD` is `a3d5874c9e0b1198aa2ed7e2fbbb0a29a57b3a14` and the full history behind it is present.
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
