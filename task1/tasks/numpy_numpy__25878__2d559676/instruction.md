# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: tricky Cython compile failure with main via C API changes

This code compiles after Cython `3.0.8` translation with NumPy `1.26.4` but not with `main` on x86_64 Linux/GNU toolchain:

```python
cimport numpy as cnp
cdef cnp.npy_intp dims[2]
pos = cnp.PyArray_ZEROS(2, dims, cnp.NPY_FLOAT32, 0)
cnp.PyArray_FILLWBYTE(pos, 0)
```

<details>
<summary> sample `setup.py` file </summary>

```python
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Extension modules
extensions = [
    Extension("reproducer", ["reproducer.pyx"],
              include_dirs=[np.get_include()],
              language="c++")
              # will fail to compile on 1.26.4 with this:
              #extra_compile_args=["-DNPY_NO_DEPRECATED_API=NPY_1_9_API_VERSION"])
]


setup(
    ext_modules = cythonize(extensions),
    include_dirs=[np.get_include()]
)

```
</details>

I've made a small repo (https://github.com/tylerjereddy/mda_repro_issue_4460) for reproduction with `python setup.py build`. I dissected it out from a build failure in another ecosystem project (https://github.com/MDAnalysis/mdanalysis/issues/4460) against NumPy `main`. The `git bisect` hits:



I can't tell what to do though, but since setting `"-DNPY_NO_DEPRECATED_API=NPY_1_9_API_VERSION"` also causes the compile failure with NumPy `1.26.4` (and same for `1_7` version), one might expect this to have been a somewhat intentional change.

However, I spent quite some time searching the devdocs for clues,  Am I missing a location in the docs/migration guide, or is there something that could clarify what to do here?
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `18c13458d544d9b935b63e7b495a346ec14f5468` and the full history behind it is present.
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
