# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: repr of generic datetime crashes

### Reproducing code example:

<!-- A short code example that reproduces the problem/missing feature. It should be
self-contained, i.e., possible to run as-is via 'python myproblem.py' -->

```python
import numpy as np
dt = np.dtype([('b', np.datetime64)])
arr = np.zeros(1, dt)
repr(arr)
```

<!-- Remove these sections for a feature request -->

### Error message:

<!-- If you are reporting a segfault please include a GDB traceback, which you
can generate by following
https://github.com/numpy/numpy/blob/master/doc/source/dev/development_environment.rst#debugging -->

<!-- Full error message, if any (starting from line Traceback: ...) -->
```
  File "C:\Program Files\Python 3.5\lib\site-packages\IPython\core\formatters.py", line 693, in __call__
    printer.pretty(obj)
  File "C:\Program Files\Python 3.5\lib\site-packages\IPython\lib\pretty.py", line 380, in pretty
    return _default_pprint(obj, self, cycle)
  File "C:\Program Files\Python 3.5\lib\site-packages\IPython\lib\pretty.py", line 495, in _default_pprint
    _repr_pprint(obj, p, cycle)
  File "C:\Program Files\Python 3.5\lib\site-packages\IPython\lib\pretty.py", line 693, in _repr_pprint
    output = repr(obj)
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 1433, in array_repr
    ', ', prefix, suffix=suffix)
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 670, in array2string
    return _array2string(a, options, separator, prefix)
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 460, in wrapper
    return f(self, *args, **kwargs)
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 486, in _array2string
    format_function = _get_format_function(data, **options)
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 433, in _get_format_function
    return StructuredVoidFormat.from_data(data, **options)
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 1270, in from_data
    format_function = _get_format_function(data[field_name], **options)
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 428, in _get_format_function
    return formatdict['datetime']()
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 365, in <lambda>
    'datetime': lambda: DatetimeFormat(data, legacy=legacy),
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 1222, in __init__
    super(DatetimeFormat, self).__init__(x)
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 1183, in __init__
    max_str_len = max(len(self._format_non_nat(np.max(non_nat))),
  File "C:\Users\wiese\Repos\numeric-python\numpy\build\testenv\Lib\site-packages\numpy\core\arrayprint.py", line 1233, in _format_non_nat
    casting=self.casting)
ValueError: Cannot convert a NumPy datetime value other than NaT with generic units
```

### Numpy/Python version information:
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `591880b0a7bcbb493d9ec023783157818f2f5236` and the full history behind it is present.
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
