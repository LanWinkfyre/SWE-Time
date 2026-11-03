# Locate the commit that introduced this regression

A regression was reported against `scipy/scipy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: SciPy won't pick the correct BLAS when running the test suite in a debug configuration

### Describe your issue.

SciPy tests cannot be run due to a missing symbol provided by LAPACK/BLAS (according to @ev-br), which doesn't have the `scipy_` prefix when using `scipy-openblas`. This is occurring when SciPy is compiled in a debug configuration, either via `dev.py build --debug` or `--config-settings=setup-args="-Dbuildtype=debug"` using pip. 

This issue is occurring both in CPython 3.12 and 3.13t. An important note is that when a release configuration is set, this error is not occurring, thus something is going wrong when setting the debug compilation flags and their interaction with the `BLAS_SYMBOL_PREFIX` macro flag.

### Reproducing Code Example

```python
docker pull quay.io/pypa/manylinux2014_x86_64
docker run -it quay.io/pypa/manylinux2014_x86_64 /bin/bash

cd home
export PATH=/opt/python/cp312-cp312/bin/:$PATH
git clone https://github.com/scipy/scipy.git --recursive

python -m pip install -i https://pypi.anaconda.org/scientific-python-nightly-wheels/simple numpy cython
python -m pip install ninja meson-python pybind11 pythran
python -m pip install pytest hypothesis pooch

cd scipy
python -m pip install -r requirements/openblas.txt
python -c "import scipy_openblas32; print(scipy_openblas32.get_pkg_config())" > scipy-openblas.pc

PKG_CONFIG_PATH=$PWD pip install -e . -vvv --no-build-isolation  --config-settings=setup-args="-Dbuildtype=debug"
pytest -x -v scipy
```


### Error message

```shell
ImportError while importing test module '/home/scipy/scipy/differentiate/tests/test_differentiate.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/opt/python/cp312-cp312/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
scipy/differentiate/tests/test_differentiate.py:11: in <module>
    from scipy import stats, optimize, special
scipy/__init__.py:136: in __getattr__
    return _importlib.import_module(f'scipy.{name}')
/opt/python/cp312-cp312/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
scipy/stats/__init__.py:602: in <module>
    from ._stats_py import *
scipy/stats/_stats_py.py:51: in <module>
    from . import distributions
scipy/stats/distributions.py:10: in <module>
    from . import _continuous_distns
scipy/stats/_continuous_distns.py:24: in <module>
    from . import _stats
_stats.pyx:1: in init scipy.stats._stats
    ???
E   ImportError: /home/scipy/build/cp312/scipy/special/cython_special.cpython-312-x86_64-linux-gnu.so: undefined symbol: dstevr_
```


### SciPy/NumPy/Python version and system information

```shell
{
  "Compilers": {
    "c": {
      "name": "gcc",
      "linker": "ld.bfd",
      "version": "10.2.1",
      "commands": "cc"
    },
    "cython": {
      "name": "cython",
      "linker": "cython",
      "version": "3.1.0",
      "commands": "cython"
    },
    "c++": {
      "name": "gcc",
      "linker": "ld.bfd",
      "version": "10.2.1",
      "commands": "c++"
    },
    "fortran": {
      "name": "gcc",
      "linker": "ld.bfd",
      "version": "10.2.1",
      "commands": "gfortran"
    },
    "pythran": {
      "version": "0.16.1",
      "include directory": "../../../opt/_internal/cpython-3.12.4/lib/python3.12/site-packages/pythran"
    }
  },
  "Machine Information": {
    "host": {
      "cpu": "x86_64",
      "family": "x86_64",
      "endian": "little",
      "system": "linux"
    },
    "build": {
      "cpu": "x86_64",
      "family": "x86_64",
      "endian": "little",
      "system": "linux"
    },
    "cross-compiled": false
  },
  "Build Dependencies": {
    "blas": {
      "name": "scipy-openblas",
      "found": true,
      "version": "0.3.27.dev",
      "detection method": "pkgconfig",
      "include directory": "/opt/_internal/cpython-3.12.4/lib/python3.12/site-packages/scipy_openblas32/include",
      "lib directory": "/opt/_internal/cpython-3.12.4/lib/python3.12/site-packages/scipy_openblas32/lib",
      "openblas configuration": "OpenBLAS 0.3.27.dev DYNAMIC_ARCH NO_AFFINITY Haswell MAX_THREADS=64",
      "pc file directory": "/home/scipy"
    },
    "lapack": {
      "name": "scipy-openblas",
      "found": true,
      "version": "0.3.27.dev",
      "detection method": "pkgconfig",
      "include directory": "/opt/_internal/cpython-3.12.4/lib/python3.12/site-packages/scipy_openblas32/include",
      "lib directory": "/opt/_internal/cpython-3.12.4/lib/python3.12/site-packages/scipy_openblas32/lib",
      "openblas configuration": "OpenBLAS 0.3.27.dev DYNAMIC_ARCH NO_AFFINITY Haswell MAX_THREADS=64",
      "pc file directory": "/home/scipy"
    },
    "pybind11": {
      "name": "pybind11",
      "version": "2.13.1",
      "detection method": "config-tool",
      "include directory": "unknown"
    }
  },
  "Python Information": {
    "path": "/opt/_internal/cpython-3.12.4/bin/python",
    "version": "3.12"
  }
}
```


I just did the bisection.
```

## What you have

- `/testbed/repo` is a git clone of `scipy/scipy` truncated just after the regression was
  reported.  `HEAD` is `d60b48d0a457c1d92f4ad1b3e4ef5063ba170980` and the full history behind it is present.
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
