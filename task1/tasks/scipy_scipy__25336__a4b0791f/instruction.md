# Locate the commit that introduced this regression

A regression was reported against `scipy/scipy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: pylint with --extension-pkg-whitelist=scipy cannot handle circular imports in special

### Describe your issue.

Any python script with `import scipy.special` can cause a failure when checked by `pylint --extension-pkg-whitelist=scipy` command. 
As the Python part of the reproducer is a single line, I pasted (into the Reproducing Code Example field) a log from an interactive bash session showing (hopefully) all important versions.

### Reproducing Code Example

```python
$ pyenv shell tmp

$ pip3 install -U pip
Requirement already satisfied: pip in /home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages (24.0)
Collecting pip
  Using cached pip-26.1.1-py3-none-any.whl.metadata (4.6 kB)
Using cached pip-26.1.1-py3-none-any.whl (1.8 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed pip-26.1.1

$ pip3 install -U pylint
Collecting pylint
  Using cached pylint-4.0.5-py3-none-any.whl.metadata (12 kB)
Collecting astroid<=4.1.dev0,>=4.0.2 (from pylint)
  Using cached astroid-4.0.4-py3-none-any.whl.metadata (4.4 kB)
Collecting dill>=0.3.6 (from pylint)
  Downloading dill-0.4.1-py3-none-any.whl.metadata (10 kB)
Collecting isort!=5.13,<9,>=5 (from pylint)
  Downloading isort-8.0.1-py3-none-any.whl.metadata (11 kB)
Collecting mccabe<0.8,>=0.6 (from pylint)
  Using cached mccabe-0.7.0-py2.py3-none-any.whl.metadata (5.0 kB)
Collecting platformdirs>=2.2 (from pylint)
  Using cached platformdirs-4.9.6-py3-none-any.whl.metadata (4.7 kB)
Collecting tomlkit>=0.10.1 (from pylint)
  Using cached tomlkit-0.15.0-py3-none-any.whl.metadata (2.8 kB)
Using cached pylint-4.0.5-py3-none-any.whl (536 kB)
Using cached astroid-4.0.4-py3-none-any.whl (276 kB)
Downloading isort-8.0.1-py3-none-any.whl (89 kB)
Using cached mccabe-0.7.0-py2.py3-none-any.whl (7.3 kB)
Downloading dill-0.4.1-py3-none-any.whl (120 kB)
Using cached platformdirs-4.9.6-py3-none-any.whl (21 kB)
Using cached tomlkit-0.15.0-py3-none-any.whl (41 kB)
Installing collected packages: tomlkit, platformdirs, mccabe, isort, dill, astroid, pylint
Successfully installed astroid-4.0.4 dill-0.4.1 isort-8.0.1 mccabe-0.7.0 platformdirs-4.9.6 pylint-4.0.5 tomlkit-0.15.0

$ pip3 install scipy==1.15.3
Collecting scipy==1.15.3
  Using cached scipy-1.15.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (61 kB)
Collecting numpy<2.5,>=1.23.5 (from scipy==1.15.3)
  Using cached numpy-2.4.6-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
Using cached scipy-1.15.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (37.3 MB)
Using cached numpy-2.4.6-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.6 MB)
Installing collected packages: numpy, scipy
Successfully installed numpy-2.4.6 scipy-1.15.3

$ python --version
Python 3.12.3

$ pip3 freeze
astroid==4.0.4
dill==0.4.1
isort==8.0.1
mccabe==0.7.0
numpy==2.4.6
platformdirs==4.9.6
pylint==4.0.5
scipy==1.15.3
tomlkit==0.15.0

$ cat m.py
import scipy.special

$ pylint --extension-pkg-whitelist=scipy m.py 2>&1 | tail -n 40
************* Module m
m.py:1:0: C0114: Missing module docstring (missing-module-docstring)
m.py:1:0: W0611: Unused import scipy.special (unused-import)

-----------------------------------
Your code has been rated at 0.00/10


$ pip3 install scipy==1.16.0
Collecting scipy==1.16.0
  Using cached scipy-1.16.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (61 kB)
Requirement already satisfied: numpy<2.6,>=1.25.2 in /home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages (from scipy==1.16.0) (2.4.6)
Using cached scipy-1.16.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (35.1 MB)
Installing collected packages: scipy
  Attempting uninstall: scipy
    Found existing installation: scipy 1.15.3
    Uninstalling scipy-1.15.3:
      Successfully uninstalled scipy-1.15.3
Successfully installed scipy-1.16.0

$ pip3 freeze
astroid==4.0.4
dill==0.4.1
isort==8.0.1
mccabe==0.7.0
numpy==2.4.6
platformdirs==4.9.6
pylint==4.0.5
scipy==1.16.0
tomlkit==0.15.0

$ pylint --extension-pkg-whitelist=scipy m.py 2>&1 | tail -n 40
                 ^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5705, in const_factory
    instance.postinit(_create_dict_items(value, instance))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5662, in _create_dict_items
    value_node = const_factory(value)
                 ^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5705, in const_factory
    instance.postinit(_create_dict_items(value, instance))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5660, in _create_dict_items
    key_node = const_factory(key)
               ^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5707, in const_factory
    return Const(value)
           ^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 2082, in __init__
    Instance.__init__(self, None)
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/bases.py", line 354, in __init__
    super().__init__(proxied)
RecursionError: maximum recursion depth exceeded

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/pylint/utils/ast_walker.py", line 87, in walk
    callback(astroid)
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/pylint/checkers/imports.py", line 541, in visit_import
    imported_module = self._get_imported_module(node, name)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/pylint/checkers/imports.py", line 1052, in _get_imported_module
    raise astroid.AstroidError from e
astroid.exceptions.AstroidError
************* Module m
m.py:1:0: C0114: Missing module docstring (missing-module-docstring)
m.py:1:0: F0002: m.py: Fatal error while checking 'm.py'. Please open an issue in our bug tracker so we address this. There is a pre-filled template that you can use in '/home/vrpolak/.cache/pylint/pylint-crash-2026-05-26-14-47-32.txt'. (astroid-error)

------------------------------------------------------------------
Your code has been rated at 0.00/10 (previous run: 0.00/10, +0.00)
```

### Error message

```shell
Nope, the full error has too many lines. I will give you the start and the end.

Exception on node <Import l.1 at 0x7faf5ba19e20> in file '/home/vrpolak/lf/fdio/csit/m.py'
Traceback (most recent call last):
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/pylint/checkers/imports.py", line 1027, in _get_imported_module
    return importnode.do_import_module(modname)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/nodes/_base_nodes.py", line 167, in do_import_module
    return mymodule.import_module(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/nodes/scoped_nodes/scoped_nodes.py", line 459, in import_module
    return AstroidManager().ast_from_module_name(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/manager.py", line 266, in ast_from_module_name
    return self.ast_from_file(found_spec.location, modname, fallback=False)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/manager.py", line 165, in ast_from_file
    return AstroidBuilder(self).file_build(filepath, modname)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/builder.py", line 149, in file_build
    return self._post_build(module, builder, encoding)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/builder.py", line 170, in _post_build
    self.add_from_names_to_locals(from_node, global_names)
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/builder.py", line 233, in add_from_names_to_locals
    imported = node.do_import_module()
               ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/nodes/_base_nodes.py", line 167, in do_import_module
    return mymodule.import_module(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/nodes/scoped_nodes/scoped_nodes.py", line 459, in import_module
    return AstroidManager().ast_from_module_name(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/manager.py", line 241, in ast_from_module_name
    return self.ast_from_module(named_module, modname)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/manager.py", line 340, in ast_from_module
    return AstroidBuilder(self).module_build(module, modname)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/builder.py", line 105, in module_build
    node = self.inspect_build(module, modname=modname, path=path)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/raw_building.py", line 463, in inspect_build
    self.object_build(node, module)
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/raw_building.py", line 520, in object_build
    self.object_build(child, member)
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/raw_building.py", line 520, in object_build
    self.object_build(child, member)
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/raw_building.py", line 520, in object_build
    self.object_build(child, member)
  [Previous line repeated 2 more times]
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/raw_building.py", line 512, in object_build
    child = nodes.const_factory(member)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5699, in const_factory
    instance.postinit(_create_dict_items(value, instance))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5656, in _create_dict_items
    value_node = const_factory(value)
                 ^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5699, in const_factory
    instance.postinit(_create_dict_items(value, instance))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/csit/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5656, in _create_dict_items
    value_node = const_factory(value)
                 ^^^^^^^^^^^^^^^^^^^^

...

  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5705, in const_factory
    instance.postinit(_create_dict_items(value, instance))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5660, in _create_dict_items
    key_node = const_factory(key)
               ^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 5707, in const_factory
    return Const(value)
           ^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/nodes/node_classes.py", line 2082, in __init__
    Instance.__init__(self, None)
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/astroid/bases.py", line 354, in __init__
    super().__init__(proxied)
RecursionError: maximum recursion depth exceeded

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/pylint/utils/ast_walker.py", line 87, in walk
    callback(astroid)
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/pylint/checkers/imports.py", line 541, in visit_import
    imported_module = self._get_imported_module(node, name)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vrpolak/.pyenv/versions/3.12.3/envs/tmp/lib/python3.12/site-packages/pylint/checkers/imports.py", line 1052, in _get_imported_module
    raise astroid.AstroidError from e
astroid.exceptions.AstroidError
************* Module m
m.py:1:0: C0114: Missing module docstring (missing-module-docstring)
m.py:1:0: F0002: m.py: Fatal error while checking 'm.py'. Please open an issue in our bug tracker so we address this. There is a pre-filled template that you can use in '/home/vrpolak/.cache/pylint/pylint-crash-2026-05-26-14-47-32.txt'. (astroid-error)
```

### SciPy/NumPy/Python version and system information

```shell
1.16.0 2.4.6 sys.version_info(major=3, minor=12, micro=3, releaselevel='final', serial=0)
/home/vrpolak/.pyenv/versions/tmp/lib/python3.12/site-packages/scipy/__config__.py:154: UserWarning: Install `pyyaml` for better output
  warnings.warn("Install `pyyaml` for better output", stacklevel=1)
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
      "version": "3.1.2",
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
      "version": "0.18.0",
      "include directory": "../../tmp/build-env-ltl35zwt/lib/python3.12/site-packages/pythran"
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
      "version": "0.3.28",
      "detection method": "pkgconfig",
      "include directory": "/opt/_internal/cpython-3.12.11/lib/python3.12/site-packages/scipy_openblas32/include",
      "lib directory": "/opt/_internal/cpython-3.12.11/lib/python3.12/site-packages/scipy_openblas32/lib",
      "openblas configuration": "OpenBLAS 0.3.28 DYNAMIC_ARCH NO_AFFINITY Haswell MAX_THREADS=64",
      "pc file directory": "/project"
    },
    "lapack": {
      "name": "scipy-openblas",
      "found": true,
      "version": "0.3.28",
      "detection method": "pkgconfig",
      "include directory": "/opt/_internal/cpython-3.12.11/lib/python3.12/site-packages/scipy_openblas32/include",
      "lib directory": "/opt/_internal/cpython-3.12.11/lib/python3.12/site-packages/scipy_openblas32/lib",
      "openblas configuration": "OpenBLAS 0.3.28 DYNAMIC_ARCH NO_AFFINITY Haswell MAX_THREADS=64",
      "pc file directory": "/project"
    },
    "pybind11": {
      "name": "pybind11",
      "version": "2.13.6",
      "detection method": "config-tool",
      "include directory": "unknown"
    }
  },
  "Python Information": {
    "path": "/tmp/build-env-ltl35zwt/bin/python",
    "version": "3.12"
  }
}
```
```

## What you have

- `/testbed/repo` is a git clone of `scipy/scipy` truncated just after the regression was
  reported.  `HEAD` is `b2c8661977540992f2f7028cbea57707aaf6f50b` and the full history behind it is present.
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
