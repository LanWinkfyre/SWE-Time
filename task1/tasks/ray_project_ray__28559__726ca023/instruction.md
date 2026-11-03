# Locate the commit that introduced this regression

A regression was reported against `ray-project/ray`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[core] All long-running release tests that use a local Ray cluster are failing

### What happened + What you expected to happen

long_running_* tests create a local Ray cluster and are failing:


```python
Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.7/site-packages/ray/_private/node.py", line 316, in __init__
    self.redis_password,
  File "/home/ray/anaconda3/lib/python3.7/site-packages/ray/_private/services.py", line 385, in wait_for_node
    raise TimeoutError("Timed out while waiting for node to startup.")
TimeoutError: Timed out while waiting for node to startup.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "workloads/many_tasks_serialized_ids.py", line 49, in <module>
    dashboard_host="0.0.0.0",
  File "/home/ray/anaconda3/lib/python3.7/site-packages/ray/cluster_utils.py", line 224, in add_node
    spawn_reaper=self._shutdown_at_exit,
  File "/home/ray/anaconda3/lib/python3.7/site-packages/ray/_private/node.py", line 320, in __init__
```

[Example failed run.](https://console.anyscale.com/o/anyscale-internal/projects/prj_FKRmeV5pA6X72aVscFALNC32/clusters/ses_bJWY3VjSNEx1H352CzMaNUkc?command-history-section=command_history)

### Versions / Dependencies




### Reproduction script

long_running_* tests

### Issue Severity

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `ray-project/ray` truncated just after the regression was
  reported.  `HEAD` is `86c552021b015aa0a0688b63ea5ee9a0487b0e11` and the full history behind it is present.
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
