# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Parameter types names duplicated with Doxygen 1.15.0

**Describe the bug**
In Doxygen 1.15.0, I'm seeing duplicated parameter type names in certain cases when building documentation for wxWidgets (C++).  This *seems* to be happening when the parameter is a typedef to another class.  In this case, `wxObjectRefData` is a typedef to `wxRefCounter` (from `interface/wx/object.h`):
```
typedef wxRefCounter wxObjectRefData;
```

**Screenshots**
See that wxObjectRefData is duplicated in `GetRefData` and `SetRefData`:
<img width="2026" height="690" alt="Image" src="https://github.com/user-attachments/assets/30bc7375-4af7-4dd5-ae5e-9ddb3782f0a9" />

**To Reproduce**
Sorry the example isn't exactly minimal but you can see the problem in `classwx_object.html`.  I'll try to make a more minimal example.
[example.zip](https://github.com/user-attachments/files/23945961/example.zip)

**Expected behavior**
Type name shouldn't be duplicated.

**Version**
1.15.0 on Fedora 43.


The bisection gave:




@doxygen any ideas?
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `b09c7316acaa5e8dc6d34bd69c1aba381c6d818c` and the full history behind it is present.
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
