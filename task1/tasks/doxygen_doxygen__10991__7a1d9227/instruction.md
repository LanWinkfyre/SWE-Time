# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
@snippetdoc not support multi lines

**Describe the bug**
If I create snippet with multi lines, then It output weird characters and formats.

example code:

```python
"""[test1]
first line

second line
[test1]"""

def foo():
    """! function foo

    @snippet{doc} this test1
    """
    pass
```

**Screenshots**

![image](https://github.com/doxygen/doxygen/assets/3370086/d4d17529-6ba1-4248-a329-bcd89bbec468)



**To Reproduce**

The above piece of codes with default doxyfile.

**Expected behavior**

There should be two lines, first line and second line, without `autotoc_md0`, without bold.

**Version**




```
aa.py:7: warning: invalid argument for command '\iline'
```

Looks like it is a problem in the commentcnv.
When having:
```
## \file

"""[test1]
first line

second line
[test1]"""

## function foo_hash
#
# @snippet{doc} this test1
def foo_hash():
    pass

def foo_exclamation():
    """! function foo

    @snippet{doc} this test1
    """
    pass
```
the result is
```
output=[
## \file

"""[test1]
first line

second line
[test1]"""

## function foo_hash
#
#  \ifile ".../aa.py" \iline 4 \ilinebr   first line
#
# second line
#  \ifile ".../aa.py" \iline 11 \ilinebr
def foo_hash():
    pass

def foo_exclamation():
    """! function foo

     \ifile ".../aa.py" \iline 4 \ilinebr     first line
#
#   second line
#    \ifile ".../aa.py" \iline 25 \ilinebr
    """
    pass
]
```
note the `#` signs with the function `foo_exclamation` these should in case of `"""!` not be present

A bisect gave:
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `93ad49251c5f273a7a276e22ef2f8ef48afdd86c` and the full history behind it is present.
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
