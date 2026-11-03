# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: dtype changed from float64 to int64 in scipy discrete_rv

### Describe the issue:

The issue is seen with the NumPy nightly wheels since a few days ago. I don't know what exactly the cause is because it is something happening inside SciPy but somehow an array ended up being a different dtype when passed through to the `_pmf` method shown below which causes it to fail with:
```python
  File "/home/oscar/current/active/sympy/t.py", line 6, in _pmf
    return (2/3)*3**(1 - i)
                 ~^^~~~~~~~
ValueError: Integers to negative integer powers are not allowed.
```

### Reproduce the code example:

```python
from scipy.stats import rv_discrete

class rv_exponential(rv_discrete):
    def _pmf(self, i):
        print(i.dtype, i.shape)
        return (2/3)*3**(1 - i)

rv = rv_exponential(a=0.0, b=float('inf'))

print(rv.rvs())
```


### Error message:

```shell
$ python t.py 
int64 (28,)
Traceback (most recent call last):
  File "/home/oscar/current/active/sympy/t.py", line 10, in <module>
    print(rv.rvs())
          ^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py", line 3430, in rvs
    return super().rvs(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py", line 1108, in rvs
    vals = self._rvs(*args, size=size, random_state=random_state)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py", line 1034, in _rvs
    Y = self._ppf(U, *args)
        ^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py", line 1049, in _ppf
    return self._ppfvec(q, *args)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/numpy/lib/_function_base_impl.py", line 2470, in __call__
    return self._call_as_normal(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/numpy/lib/_function_base_impl.py", line 2463, in _call_as_normal
    return self._vectorize_call(func=func, args=vargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/numpy/lib/_function_base_impl.py", line 2553, in _vectorize_call
    outputs = ufunc(*inputs)
              ^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py", line 3057, in _drv2_ppfsingle
    qb = self._cdf(b, *args)
         ^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py", line 3396, in _cdf
    return self._cdfvec(k, *args)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/numpy/lib/_function_base_impl.py", line 2470, in __call__
    return self._call_as_normal(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/numpy/lib/_function_base_impl.py", line 2463, in _call_as_normal
    return self._vectorize_call(func=func, args=vargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/numpy/lib/_function_base_impl.py", line 2553, in _vectorize_call
    outputs = ufunc(*inputs)
              ^^^^^^^^^^^^^^
  File "/home/oscar/.pyenv/versions/sympy-3.12.git/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py", line 3392, in _cdf_single
    return np.sum(self._pmf(m, *args), axis=0)
                  ^^^^^^^^^^^^^^^^^^^
  File "/home/oscar/current/active/sympy/t.py", line 6, in _pmf
    return (2/3)*3**(1 - i)
                 ~^^~~~~~~~
ValueError: Integers to negative integer powers are not allowed.
```


### Python and NumPy Versions:

This is seen with the NumPy nightly wheels since a few days ago.

With released NumPy 2.0.1 the code runs to completion with
```console
$ python t.py 
float64 (11,)
float64 (1,)
float64 (6,)
float64 (3,)
float64 (2,)
0
```

### Runtime Environment:

_No response_

### Context for the issue:

This comes from a SciPy issue: https://github.com/scipy/scipy/issues/21272 and a SymPy issue https://github.com/sympy/sympy/issues/26862



CC @mtsokol
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `2459d80adf7d8e7c0c6debf72f5207a6ca37f264` and the full history behind it is present.
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
