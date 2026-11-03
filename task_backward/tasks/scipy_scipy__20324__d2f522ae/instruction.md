# Locate the commit that introduced this regression

A regression was reported against `scipy/scipy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
MAINT, BUG (?): pearsonr statistic return type change

Originally reported by @stefanv on mailing list, for an issue that was detected in `skimage`. My local testing suggests that the issue is reproducible for NumPy `1.26.4` and NumPy `2.0.0b1` though, so the reason may be due to a code change we've made directly.

I confirmed locally that the test below passes at `v1.12.0` tag, and fails on `main`. I think Stefan's argument was that the docstring still says `float` for the statistic.

```diff
--- a/scipy/stats/tests/test_stats.py
+++ b/scipy/stats/tests/test_stats.py
@@ -8495,3 +8495,8 @@ class TestExpectile:
         for alpha in np.r_[0, alpha_seq, 1 - alpha_seq[:-1:-1], 1]:
             e_list.append(stats.expectile(x, alpha=alpha))
         assert np.all(np.diff(e_list) > 0)
+
+
+def test_pearsonr_stat_ret_type():
+    res = stats.pearsonr([1, 2, 3], [4, 5, 6])
+    assert isinstance(res.statistic, float)
```

Maybe one of the `stats` folks can comment re: what we might want to do here for `1.13.0`? I'll see if I can bisect this for you folks.

Here's the result of `git bisect` process on the above regression test:
```

## What you have

- `/testbed/repo` is a git clone of `scipy/scipy` truncated just after the regression was
  reported.  `HEAD` is `f4263c24524f0b5ac5078056aa51721b8ca46392` and the full history behind it is present.
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
