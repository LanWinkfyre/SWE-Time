# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Doxygen 1.8.17 false warnings and no generate output for documented const functions

Starting with 1.8.17 there are warnings about missing documentation for const functions that in fact are documented. The documentation is also missing in the generate output. The same input source code generates the expected output and no warnings on 1.8.16.

The issue can be demonstrated with an example.

> cat example.cpp
```
class Example
{
public:
	int foo();
	int foo() const;
};

/**
 * \brief Foo
 */
int Example::foo()
{
	return 0;
}

/**
 * \brief Const foo
 */
int Example::foo() const
{
	return 0;
}
```

Generate doxygen:
> doxygen -g config
> doxygen config

Warning that the documentation is missing.

> example.cpp:5: warning: Member foo() const (function) of class Example is not documented.
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `10b2b8fc694b60a17ccd2642f3a40c851e33b9da` and the full history behind it is present.
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
