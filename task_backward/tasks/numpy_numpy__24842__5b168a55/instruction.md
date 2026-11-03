# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Occasional failure to sort complex numbers by absolute value on M2 macs

### Describe the issue:

Consider the complex array in the attached npy file (bad.npy in bad.zip), sort it by absolute value, and assert that the absolute value is increasing.  The assertion will occasionally fail (around 1-5 times per 100 iterations).
[bad.zip](https://github.com/numpy/numpy/files/12781432/bad.zip)
It is also possible to see the failure by running the loop from within an ipython shell, but it is much rarer (once per 1000 to 10000 iterations).

This occurs on a conda python + pip-installed numpy (a mix which may or may not be a good idea, I know); AFAICT this happens with numpy 1.25-1.26 but not on numpy 1.24.

### Reproduce the code example:

```python
for i in $(seq 0 99); do
    echo "$i"
    python -c 'import numpy as np; nz = np.load("/tmp/bad.npy"); z = nz[np.argsort(abs(nz))]; assert np.diff(abs(z)).min() >= 0'
done
```


### Error message:

```shell
AssertionError
```


### Runtime information:

1.26.0
3.11.3 | packaged by conda-forge | (main, Apr  6 2023, 08:58:31) [Clang 14.0.6 ]

[{'numpy_version': '1.26.0',
  'python': '3.11.3 | packaged by conda-forge | (main, Apr  6 2023, 08:58:31) '
            '[Clang 14.0.6 ]',
  'uname': uname_result(system='Darwin', node='ICR-XYN62WVT43', release='22.6.0', version='Darwin Kernel Version 22.6.0: Wed Jul  5 22:17:35 PDT 2023; root:xnu-8796.141.3~6/RELEASE_ARM64_T8112', machine='arm64')},
 {'simd_extensions': {'baseline': ['NEON', 'NEON_FP16', 'NEON_VFPV4', 'ASIMD'],
                      'found': ['ASIMDHP'],
                      'not_found': ['ASIMDFHM']}},
 {'architecture': 'armv8',
  'filepath': '/Users/antony/.local/lib/python3.11/site-packages/numpy/.dylibs/libopenblas64_.0.dylib',
  'internal_api': 'openblas',
  'num_threads': 8,
  'prefix': 'libopenblas',
  'threading_layer': 'pthreads',
  'user_api': 'blas',
  'version': '0.3.23.dev'},
 {'architecture': 'armv8',
  'filepath': '/Users/antony/.local/lib/python3.11/site-packages/scipy/.dylibs/libopenblas.0.dylib',
  'internal_api': 'openblas',
  'num_threads': 8,
  'prefix': 'libopenblas',
  'threading_layer': 'pthreads',
  'user_api': 'blas',
  'version': '0.3.21.dev'},
 {'architecture': 'armv8',
  'filepath': '/opt/homebrew/Cellar/openblas/0.3.24/lib/libopenblasp-r0.3.24.dylib',
  'internal_api': 'openblas',
  'num_threads': 8,
  'prefix': 'libopenblas',
  'threading_layer': 'openmp',
  'user_api': 'blas',
  'version': '0.3.24'},
 {'filepath': '/opt/homebrew/Cellar/gcc/13.2.0/lib/gcc/current/libgomp.1.dylib',
  'internal_api': 'openmp',
  'num_threads': 8,
  'prefix': 'libgomp',
  'user_api': 'openmp',
  'version': None}]

### Context for the issue:

_No response_

I bisected locally on M2 max architecture:
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `5ca26b1b9df5e8c89923a2bb723a5ab95b6fe09b` and the full history behind it is present.
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
