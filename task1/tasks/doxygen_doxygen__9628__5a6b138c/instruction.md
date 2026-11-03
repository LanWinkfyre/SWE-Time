# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Warning: "Unexpected token TK_HTMLTAG found as part of a title section"

**Describe the bug**
When generating the documentation of the [FLTK project](https://www.fltk.org) a bogus warning "`Unexpected token TK_HTMLTAG found as part of a title section`" appears in current Doxygen `master`. This is a regression WRT Doxygen 1.9.4 and earlier (1.9.5 not tested).

**Expected behavior**
These warnings should not appear. The token "`TK_HTMLTAG`" does not exist in the FLTK source code but I found it in the Doxygen code.

**Screenshots**
No screenshots. Warnings appearing with current FLTK documentation:
```
.../preface.dox:74: warning: Unexpected token TK_HTMLTAG found as part of a title section
.../preface.dox:74: warning: Unexpected token TK_HTMLTAG found as part of a title section
.../preface.dox:80: warning: Unexpected token TK_HTMLTAG found as part of a title section
.../preface.dox:80: warning: Unexpected token TK_HTMLTAG found as part of a title section
.../preface.dox:80: warning: Unexpected token TK_HTMLTAG found as part of a title section
.../preface.dox:80: warning: Unexpected token TK_HTMLTAG found as part of a title section
```
Link to original source file [preface.dox](https://github.com/fltk/fltk/blob/4d17cf310dc953703bf3a60763b681eb217bc3e9/documentation/src/preface.dox#L74). Note that the preceding lines of those mentioned in the warnings contain HTML `<tt>` statements. I'll follow-up with a partial workaround (removing these `<tt>` tags).

**To Reproduce**
I'm currently not able to create a small reproducer since the warnings are not related to our FLTK source code. However, it's easy to reproduce the warnings with current FLTK code:
```
git clone https://github.com/fltk/fltk.git
cd fltk
# optionally check out `master` as of today:
git checkout 4d17cf310dc953703bf3a60763b681eb217bc3e9
mkdir build
cd build
# Make sure that `doxygen` can be found in your path so cmake finds it.
# I assume you know how to do this, but anyway:
# example: export PATH=/path/to/doxygen/build/bin:$PATH
cmake ..
make html
```
Please ignore warnings like "Tag 'CLASS_DIAGRAMS' ... has become obsolete. These warnings are due to an older Doxyfile (as you certainly know).

**Version**
$ doxygen --version

(self built)

**Additional context**
I'll try to `git bisect` when time permits and follow-up with more information.

Git bisect issued:




I hope this helps finding the bug.

I can try to fix the `__APPLE__` case in our source code.

However, regarding the usage of `<tt>` and other HTML tags "as part of a title section": is there a reason why this should be disallowed or is this warning a Doxygen bug (regression)?
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `44d739716a0e9f420958a4496188de2c6290df0e` and the full history behind it is present.
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
