# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Memory leak in recarrays reappeared in 1.16.3


<!-- Please describe the issue in detail here, and fill in the fields below -->

### Reproducing code example:

<!-- A short code example that reproduces the problem/missing feature. It should be
self-contained, i.e., possible to run as-is via 'python myproblem.py' -->

```python
try:
    import resource  # linux/macos
except ImportError:
    import psutil  # windows
import sys

import numpy as np


def peak_memory_usage():
    """Return peak memory usage in MB"""
    if sys.platform.startswith('win'):
        p = psutil.Process()
        return p.memory_info().peak_wset / 1024 / 1024
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    factor_mb = 1 / 1024
    if sys.platform == 'darwin':
        factor_mb = 1 / (1024 * 1024)
    return mem * factor_mb


while True:
    np.recarray([1, 2, 3], formats=['i4'])
    print(peak_memory_usage())
```

<!-- Remove these sections for a feature request -->

### Error message:

The number (peak memory usage in MB) is increasing in every iteration...

### Numpy/Python version information:

<!-- Output from 'import sys, numpy; print(numpy.__version__, sys.version)' -->
```
1.16.3 3.7.3 (default, Apr  7 2019, 01:06:41)
[GCC 8.2.1 20181127]
```
Python 3.7.3



```shell
#!/usr/bin/env zsh
echo "Cleaning up"
git clean -xdf
echo "Building..."
python setup.py --quiet build_ext --inplace -j 32 || exit 125
echo "Running memory leak test"
python ../numpy_test/memory_leak_test.py
```

which calls `memory_leak_test.py`:

```
try:
    import resource  # linux/macos
except ImportError:
    import psutil  # windows
import sys

import numpy as np


def peak_memory_usage():
    """Return peak memory usage in MB"""
    if sys.platform.startswith('win'):
        p = psutil.Process()
        return p.memory_info().peak_wset / 1024 / 1024
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    factor_mb = 1 / 1024
    if sys.platform == 'darwin':
        factor_mb = 1 / (1024 * 1024)
    return mem * factor_mb


peak_memory_before = peak_memory_usage()
for i in range(100000):
    np.recarray([1, 2, 3], formats=['i4'])
    # print(peak_memory_usage())
peak_memory_after = peak_memory_usage()

print(f"Peak memory before loop: {peak_memory_before:.1f} MB, "
      f"after: {peak_memory_after:.1f} MB")

if peak_memory_after - peak_memory_before > 1:
    print("Memory leak detected")
    exit(1)
else:
    print("Everything is OK!")
```

It took half an hour on my 16 core Xeon and this is the bisect log:
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `4178b5a731cd183563d53ed145e7dce278aa39f6` and the full history behind it is present.
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
