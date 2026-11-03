# Locate the commit that introduced this regression

A regression was reported against `ray-project/ray`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Import thread error when new workers are started (regression from 0.7.1 -> 0.7.2)

<!--
General questions should be asked on the mailing list ray-dev@googlegroups.com.
Questions about how to use Ray should be asked on
[StackOverflow](https://stackoverflow.com/questions/tagged/ray).

Before submitting an issue, please fill out the following form.
-->

### System information
- **OS Platform and Distribution (e.g., Linux Ubuntu 16.04)**: DLAMI, latest
- **Ray installed from (source or binary)**: binary
- **Ray version**: 0.7.2
- **Python version**: 3.6
- **Exact command to reproduce**: ci/long_running_tests/workloads/impala.py

<!--
You can obtain the Ray version with

python -c "import ray; print(ray.__version__)"
-->

### Describe the problem

When the number of workers in the impala stress tests are large enough that new worker processes must be created by the raylet, this causes the following import thread errors. The errors disappear when no new workers need to be started.

### Source code / logs

![Screenshot from 2019-07-05 12-07-18](https://user-images.githubusercontent.com/14922/60741403-14e68e00-9f1e-11e9-9b4d-2f6fd8b68f47.png)

![Screenshot from 2019-07-05 12-05-07](https://user-images.githubusercontent.com/14922/60741399-10ba7080-9f1e-11e9-8888-1a3e792018f7.png)
```

## What you have

- `/testbed/repo` is a git clone of `ray-project/ray` truncated just after the regression was
  reported.  `HEAD` is `4183303a2f2801dd5c7cc821b98a40de7a0ef9ba` and the full history behind it is present.
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
