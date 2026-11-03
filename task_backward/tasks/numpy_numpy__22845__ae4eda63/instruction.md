# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: (main branch only; 1.24.0 fine) bizzare boolean product issue

I did see a number of `bool_` comparison related issues open, but they seem to be fine here for NumPy `1.24.0`, while in my case it is the `main` branch that is a problem and the stable release is working just fine.

 Before deciding to release the next RC for SciPy `1.10.0` I wanted to drill down on one of the test failures to make sure I couldn't just easily shim around these, but it looks like this stuff is going to be too tricky because there are tons of them. Maybe not so serious since it just on the unreleased `main` branch so perhaps I'll move forward for now.

Here is a specific reproducer with `*.npy` files available from `np.save` in this tarball:  [arrays.tar.gz](https://github.com/numpy/numpy/files/10273085/arrays.tar.gz)


```python
import numpy as np

print("np.__version__:", np.__version__)

with open("q.npy", "rb") as q_file:
    q = np.load(q_file)

with open("r.npy", "rb") as r_file:
    r = np.load(r_file)

print("q, q.shape, q.dtype:", q, q.shape, q.dtype)
print("r, r.shape, r.dtype:", r, r.shape, r.dtype)

print("q * r:", q * r)
```

The results from `main` and `1.24.0`, respectively, follow:



```
np.__version__: 1.24.0
q, q.shape, q.dtype: [ True False False ... False False False] (10000,) bool
r, r.shape, r.dtype: [ True  True  True ...  True  True  True] (10000,) bool
q * r: [ True False False ... False False False]
```

If you focus on the first element in the result array, the stable release looks much more sensible. 

This manifested as a single (first) element difference in the expected value of the test result for `scipy/stats/tests/test_sampling.py::TestDiscreteGuideTable::test_ppf[u0]`. In fact, the actual value is just fine, but that means `stats.binom.ppf(u, n, p)` may be broken with NumPy `main` at the moment (cc: @mdhaber @tupui ), and naturally these kinds of issues seem to cascade around in a way that I probably can't patch manually, so I'll probably wait for some fixes in NumPy if you agree this is a problem.


I did a `git bisect`:
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `28329b2aadf87d57371fefe606df6923ada80b93` and the full history behind it is present.
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
