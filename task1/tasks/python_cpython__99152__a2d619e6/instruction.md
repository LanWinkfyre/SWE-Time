# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Behaviour change in partialmethod in Python3.11

# Bug report

The behavior of `partialmethod` changed in python3.11. This caused a library that I use [testsuite to fail](https://github.com/hh-h/aiohttp-swagger3/issues/108).

Here is a minimal use case that demonstrates this: 

```
from functools import partialmethod


class Cell:
    def __init__(self):
        self.alive = False

    def set_state(self, state):
        self.alive = bool(state)


class Wrapper:
    def set_state_wrap(self, cell: Cell, state):
        cell.set_state(state)


wrapper = Wrapper()

Cell.set_alive = partialmethod(wrapper.set_state_wrap, True)

cell = Cell()
cell.set_alive()
print(cell.alive)

```

In python3.10, this prints `True`. In python3.11 it errors with:

```
Traceback (most recent call last):
  File "/home/gary/partialmethod.py", line 23, in <module>
    c.set_alive()
TypeError: Wrapper.set_state_wrap() missing 1 required positional argument: 'state'
```

The arguments passed to `Wrapper.set_state_wrap` are:
__python3.10__:  `wrapper, cell, True`
__python3.11__:  `cell, True`

So `partialmethod` is forgetting that `set_state_wrap` is a method of `wrapper`, and it needs to pass that in as the first arg.


I know that the way that they are using `partialmethod` here is not how it is intended to be used, and feels wrong. However this change is behavior if intended should be documented.

# Your environment

- CPython versions tested on: Python 3.11.0  (broken) Python 3.10.7 (working)
- Operating system and architecture: Fedora Linux 36








>
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `8feb7ab77c80968a6de6079299a39b0494b1701b` and the full history behind it is present.
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
