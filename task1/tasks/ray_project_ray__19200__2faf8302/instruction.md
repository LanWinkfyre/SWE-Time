# Locate the commit that introduced this regression

A regression was reported against `ray-project/ray`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[Bug] [Dashboard] Dashboard.log spammy error message

### Search before asking

- [X] I searched the [issues](https://github.com/ray-project/ray/issues) and found no similar issues.


### Ray Component

Dashboard

### What happened + What you expected to happen

```

2021-10-07 11:00:00,324 ERROR base_events.py:1619 -- Exception in callback PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()
handle: <Handle PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()>
Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.7/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "src/python/grpcio/grpc/_cython/_cygrpc/aio/completion_queue.pyx.pxi", line 147, in grpc._cython.cygrpc.PollerCompletionQueue._handle_events
BlockingIOError: [Errno 11] Resource temporarily unavailable
2021-10-07 11:00:00,327 ERROR base_events.py:1619 -- Exception in callback PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()
handle: <Handle PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()>
Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.7/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "src/python/grpcio/grpc/_cython/_cygrpc/aio/completion_queue.pyx.pxi", line 147, in grpc._cython.cygrpc.PollerCompletionQueue._handle_events
BlockingIOError: [Errno 11] Resource temporarily unavailable
2021-10-07 11:00:00,330 ERROR base_events.py:1619 -- Exception in callback PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()
handle: <Handle PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()>
Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.7/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "src/python/grpcio/grpc/_cython/_cygrpc/aio/completion_queue.pyx.pxi", line 147, in grpc._cython.cygrpc.PollerCompletionQueue._handle_events
BlockingIOError: [Errno 11] Resource temporarily unavailable
2021-10-07 11:00:00,334 ERROR base_events.py:1619 -- Exception in callback PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()
handle: <Handle PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()>
Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.7/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "src/python/grpcio/grpc/_cython/_cygrpc/aio/completion_queue.pyx.pxi", line 147, in grpc._cython.cygrpc.PollerCompletionQueue._handle_events
BlockingIOError: [Errno 11] Resource temporarily unavailable
2021-10-07 11:00:00,336 ERROR base_events.py:1619 -- Exception in callback PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()
handle: <Handle PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()>
Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.7/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "src/python/grpcio/grpc/_cython/_cygrpc/aio/completion_queue.pyx.pxi", line 147, in grpc._cython.cygrpc.PollerCompletionQueue._handle_events
BlockingIOError: [Errno 11] Resource temporarily unavailable
2021-10-07 11:00:00,653 ERROR base_events.py:1619 -- Exception in callback PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()
handle: <Handle PollerCompletionQueue._handle_events(<_UnixSelecto...e debug=False>)()>
Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.7/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "src/python/grpcio/grpc/_cython/_cygrpc/aio/completion_queue.pyx.pxi", line 147, in grpc._cython.cygrpc.PollerCompletionQueue._handle_events
BlockingIOError: [Errno 11] Resource temporarily unavailable
```
it is logged per second. I can't find out were does it come from so would need to bisect the commits. 

### Reproduction script

```
import ray

ray.init()

@ray.remote
def f():
    import time
    time.sleep(100000)

ray.get(f.remote())
```

then tail dashboard.log from /tmp/raysession_latest/logs

### Anything else

_No response_

### Are you willing to submit a PR?

- [X] Yes I am willing to submit a PR!



of course it's my own commits!
```

## What you have

- `/testbed/repo` is a git clone of `ray-project/ray` truncated just after the regression was
  reported.  `HEAD` is `fd438d5630556a3727e7699ee3a86de5f8ffa929` and the full history behind it is present.
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
