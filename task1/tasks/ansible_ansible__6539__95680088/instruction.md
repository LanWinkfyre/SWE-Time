# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test_get_diff (TestUtils.TestUtils) failing in devel

##### Issue Type:

Bug Report
##### Ansible Version:


##### Environment:

Centos 6.5
##### Summary:

```
======================================================================
FAIL: test_get_diff (TestUtils.TestUtils)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/root/ansible/test/units/TestUtils.py", line 669, in test_get_diff
    self.assertEqual(ansible.utils.get_diff(standard), standard_expected)
AssertionError: u'--- before: foo \n+++ after: bar \n@@ -1,1 +1,1 @@\n-fooo+foo' != '--- before: foo\n+++ after: bar\n@@ -1 +1 @@\n-fooo+foo'
>>  raise self.failureException, \
          (None or '%r != %r' % (u'--- before: foo \n+++ after: bar \n@@ -1,1 +1,1 @@\n-fooo+foo', '--- before: foo\n+++ after: bar\n@@ -1 +1 @@\n-fooo+foo'))
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `9da26da335924f1fe4dd8fae94780dbfccbe4269` and the full history behind it is present.
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
