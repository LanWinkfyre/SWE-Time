# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Documentation: WARN_NO_PARAMDOC not disabled by EXTRACT_ALL?

The online documentation (and the configuration file generated on default with `$ doxygen -g`) [state](https://www.doxygen.nl/manual/config.html#cfg_warn_no_paramdoc) for `WARN_NO_PARAMDOC`: ‘If EXTRACT_ALL is set to YES then this flag will automatically be disabled.’

Example Doxyfile A:
```
WARN_AS_ERROR    = YES
WARN_NO_PARAMDOC = YES
EXTRACT_ALL      = YES
```
Example Doxyfile B:
```
WARN_AS_ERROR    = YES
WARN_NO_PARAMDOC = NO
EXTRACT_ALL      = YES
```
Consequently, those two example configurations should produce the *same* result. However, when I use the following example C code, only the one with `WARN_NO_PARAMDOC` enabled errors.
```
#include <stdio.h>

/*!
 * \brief Hello World!
 * \return void
 */
void hello() {
	puts("Hello World!");
}

/*!
 * \brief main
 * \retval 0 Always
 */
int main(void) {
	hello();
	return 0;
}
```
Personally, I like the behavior to be able to have more fine grained control. Therefore, I file this as a miss in the Doxygen configuration file documentation. However, if I misunderstood something, please, correct me!

**Version**
1.9.1 on Ubuntu 21.10, re-tested with current binary release (1.9.2)

There is now a discrepancy between the documentation and the implementation.

A bisect reveals that the commit:

causes this extra warning.
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `e321a870fda2c1c5bf759d6320b0063675f79fcd` and the full history behind it is present.
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
