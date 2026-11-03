# Locate the commit that introduced this regression

A regression was reported against `pandas-dev/pandas`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BUG: Missing keys using aggregation dictionary that are unsortable raise TypeError instead of  SpecificationError

- [ ] I have checked that this issue has not already been reported.

- [ ] I have confirmed this bug exists on the latest version of pandas.

- [ ] (optional) I have confirmed this bug exists on the master branch of pandas.

---

**Note**: Please read [this guide](https://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports) detailing how to provide the necessary information for us to reproduce your bug.

#### Code Sample, a copy-pastable example



code sample based on test_agg_consistency in pandas/tests/resample/test_resample_api.py

#### Problem description

with mypy 0.790

pandas/core/aggregation.py:741: error: Value of type variable "_LT" of "sorted" cannot be "Optional[Hashable]"  [type-var]

#### Expected Output

pandas.core.base.SpecificationError: Column(s) [2, 'bar'] do not exist

#### Output of ``pd.show_versions()``

<details>

[paste the output of ``pd.show_versions()`` here leaving a blank line after the details tag]

</details>


> This seems to be a regression from 1.0.5
```

## What you have

- `/testbed/repo` is a git clone of `pandas-dev/pandas` truncated just after the regression was
  reported.  `HEAD` is `89ddd8a70ede962dfcff01cf21f375b88fc8098b` and the full history behind it is present.
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
