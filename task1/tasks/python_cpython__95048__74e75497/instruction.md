# Locate the commit that introduced this regression

A regression was reported against `python/cpython`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test_embed failing on 3.12

test_embed produces:

FAIL: test_no_memleak (test.test_embed.MiscTests.test_no_memleak) (frozen_modules='off', stmt='pass')

Traceback (most recent call last):
  File "/home/me/Documents/GitHub/cpython/Lib/test/test_embed.py", line 1763, in test_no_memleak
    self.assertEqual(refs, 0, out)
AssertionError: -1 != 0 : [-1 refs, 0 blocks]

FAIL: test_no_memleak (test.test_embed.MiscTests.test_no_memleak) (frozen_modules='on', stmt='pass')

Traceback (most recent call last):
  File "/home/me/Documents/GitHub/cpython/Lib/test/test_embed.py", line 1763, in test_no_memleak
    self.assertEqual(refs, 0, out)
AssertionError: -1 != 0 : [-1 refs, 0 blocks]

FAIL: test_no_memleak (test.test_embed.MiscTests.test_no_memleak) (frozen_modules='off', stmt='import __hello__')

Traceback (most recent call last):
  File "/home/me/Documents/GitHub/cpython/Lib/test/test_embed.py", line 1763, in test_no_memleak
    self.assertEqual(refs, 0, out)
AssertionError: -1 != 0 : [-1 refs, 0 blocks]

FAIL: test_no_memleak (test.test_embed.MiscTests.test_no_memleak) (frozen_modules='on', stmt='import __hello__')

Traceback (most recent call last):
  File "/home/me/Documents/GitHub/cpython/Lib/test/test_embed.py", line 1763, in test_no_memleak
    self.assertEqual(refs, 0, out)
AssertionError: -1 != 0 : [-1 refs, 0 blocks]

FAILED (failures=4, skipped=3)

Also:
./python -I -X showrefcount -c pass
[-1 refs, 0 blocks]

Searched for leak with git bisect and produced:




CPython versions tested on: latest 3.12
Operating system and architecture: fedora 5.18.11-200.fc36.x86_64
```

## What you have

- `/testbed/repo` is a git clone of `python/cpython` truncated just after the regression was
  reported.  `HEAD` is `bd390ef825c5f2ad86e0966173a6bcaca85a56f2` and the full history behind it is present.
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
