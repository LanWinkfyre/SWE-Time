# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
# Bug report

### Bug description:

If you put a breakpoint here:

```diff
diff --git a/Lib/tokenize.py b/Lib/tokenize.py
index 117b485b934..9d215ea4ea1 100644
--- a/Lib/tokenize.py
+++ b/Lib/tokenize.py
@@ -574,6 +574,7 @@ def _transform_msg(msg):

 def _generate_tokens_from_c_tokenizer(source, encoding=None, extra_tokens=False):
     """Tokenize a source reading Python code as unicode strings using the internal C tokenizer"""
+    breakpoint()
     if encoding is None:
         it = _tokenize.TokenizerIter(source, extra_tokens=extra_tokens)
     else:
```

and run this:



pdb cannot show the stack. Bisecting points to







### CPython versions tested on:

CPython main branch

### Operating systems tested on:

macOS
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `1391ee664c8f019996e0cbf658e12fa38abd211d` and the full history behind it is present.
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
