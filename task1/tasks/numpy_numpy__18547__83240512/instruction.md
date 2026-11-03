# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
With NumPy 1.20, SymPy generated code cannot be serialized with dill

I have been using SymPy to generate NumPy code through `lambdify` and using dill to serialize the code. Since upgraded to NumPy 1.20.1, some generated code cannot be serialized correctly due to a RecursionError. The example code works with NumPy 1.19.

I have posted this issue in the SymPy and NumPy Gitter rooms, and I'm posting my bisecting results here. 

### Reproducing code example:

Prerequisites: SymPy 1.7.1, dill 0.3.3, NumPy 1.20.1

```python
import dill
import sympy
from sympy.abc import x

dill.settings['recurse'] = True

expr = sympy.sympify('re(x)')   # fails in 1.20.1, works in 1.19

# expr = sympy.sympify('log(x)')   # works in both 1.20.1 and 1.19

lfunc = sympy.lambdify(x, expr, 'numpy')

with open("out.pkl", 'wb') as f:
    dill.dump(lfunc, f)
```

Based on my nonexhausive testings, the error occurs when the function includes `re` or `im`. Other functions can be successfully serialized.. 

### Error message:

```
Traceback (most recent call last):
  File "test_dill.py", line 12, in <module>
    dill.dump(lfunc, f)
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/site-packages/dill/_dill.py", line 267, in dump
    Pickler(file, protocol, **_kwds).dump(obj)
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/site-packages/dill/_dill.py", line 454, in dump
    StockPickler.dump(self, obj)
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/pickle.py", line 487, in dump
    self.save(obj)
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/pickle.py", line 560, in save
    f(self, obj)  # Call unbound method with explicit self
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/site-packages/dill/_dill.py", line 1422, in save_function
    globs = globalvars(obj, recurse=True, builtin=True)
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/site-packages/dill/detect.py", line 220, in globalvars
    func.update(globalvars(nested_func, True, builtin))
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/site-packages/dill/detect.py", line 220, in globalvars
    func.update(globalvars(nested_func, True, builtin))
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/site-packages/dill/detect.py", line 220, in globalvars
    func.update(globalvars(nested_func, True, builtin))
  [Previous line repeated 981 more times]
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/site-packages/dill/detect.py", line 213, in globalvars
    func.update(nestedglobals(getattr(orig_func, func_code)))
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/site-packages/dill/detect.py", line 170, in nestedglobals
    dis.dis(func) #XXX: dis.dis(None) disassembles last traceback
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/dis.py", line 79, in dis
    _disassemble_recursive(x, file=file, depth=depth)
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/dis.py", line 373, in _disassemble_recursive
    disassemble(co, file=file)
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/dis.py", line 369, in disassemble
    _disassemble_bytes(co.co_code, lasti, co.co_varnames, co.co_names,
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/dis.py", line 401, in _disassemble_bytes
    for instr in _get_instructions_bytes(code, varnames, names,
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/dis.py", line 321, in _get_instructions_bytes
    labels = findlabels(code)
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/dis.py", line 437, in findlabels
    for offset, op, arg in _unpack_opargs(code):
  File "/Users/hcui7/miniconda3/envs/np120/lib/python3.8/dis.py", line 421, in _unpack_opargs
    for i in range(0, len(code), 2):
RecursionError: maximum recursion depth exceeded in comparison
```

### Bisecting Results



Could anyone help?

### NumPy/Python version information:

1.20.1 3.8.8 | packaged by conda-forge | (default, Feb 20 2021, 16:12:38)
[Clang 11.0.1 ]
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `954605ec08ad833899ffb956395f2d70f8eea2df` and the full history behind it is present.
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
