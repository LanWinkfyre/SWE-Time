# Locate the commit that introduced this regression

A regression was reported against `scipy/scipy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: optimize: too many open files with multiprocessing 

### Describe your issue.

If I run the full SciPy tests on my M3 Macbook Pro running MacOs 15.5 with the default open file descriptor limit of 256:

```
goldbaum at Nathans-MBP in ~/Documents/scipy on main
± ulimit -n
256
```

Then the SciPy tests always eventually fail in the `scipy.optimize` tests.

The `scipy.optimize` tests pass if I run the tests for just that submodule.

I'm running the tests with `-svx` in the gist. If I run without `-x`, I'll get more failures along the same lines later in the test suite that also always go away if I run the test individually.

### Reproducing Code Example

```python
spin test
```

### Error message

Here is a gist of a full test session: https://gist.githubusercontent.com/ngoldbaum/85e6af21b375b6342c1b8659dd6a6df0/raw/577a639cf436b022805a369a7060afe7a5d0f684/gistfile1.txt.

The error is at the end:

```shell
FAILED scipy/optimize/tests/test_optimize.py::TestWorkers::test_equal_bounds[slsqp-2] - OSError: [Errno 24] Too many open files
```

### SciPy/NumPy/Python version and system information

In the gist I'm using NumPy 2.4.0-dev but it reproduces with NumPy 2.2.6 and the following config:

<details>

```shell
1.15.2 2.2.6 sys.version_info(major=3, minor=13, micro=3, releaselevel='final', serial=0)
Build Dependencies:
  blas:
    detection method: extraframeworks
    found: true
    include directory: unknown
    lib directory: unknown
    name: Accelerate
    openblas configuration: unknown
    pc file directory: unknown
    version: unknown
  lapack:
    detection method: extraframeworks
    found: true
    include directory: unknown
    lib directory: unknown
    name: Accelerate
    openblas configuration: unknown
    pc file directory: unknown
    version: unknown
  pybind11:
    detection method: config-tool
    include directory: unknown
    name: pybind11
    version: 2.13.6
Compilers:
  c:
    commands: cc
    linker: ld64
    name: clang
    version: 15.0.0
  c++:
    commands: c++
    linker: ld64
    name: clang
    version: 15.0.0
  cython:
    commands: cython
    linker: cython
    name: cython
    version: 3.0.12
  fortran:
    commands: gfortran
    linker: ld64
    name: gcc
    version: 13.3.0
  pythran:
    include directory: ../../../../../../private/var/folders/2s/h6hvv9ps03xgz_krkkstvq_r0000gn/T/pip-build-env-0gyi37ch/overlay/lib/python3.13/site-packages/pythran
    version: 0.17.0
Machine Information:
  build:
    cpu: aarch64
    endian: little
    family: aarch64
    system: darwin
  cross-compiled: false
  host:
    cpu: aarch64
    endian: little
    family: aarch64
    system: darwin
Python Information:
  path: /private/var/folders/2s/h6hvv9ps03xgz_krkkstvq_r0000gn/T/cibw-run-83tpwvzh/cp313-macosx_arm64/build/venv/bin/python
  version: '3.13'
```

</details>


I bisected this while watching my wife play Stardew Valley this morning. Good lazy Saturday activity.
```

## What you have

- `/testbed/repo` is a git clone of `scipy/scipy` truncated just after the regression was
  reported.  `HEAD` is `7d936fa25e2e8fa74ec6399620dd6490e4dfb33e` and the full history behind it is present.
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
