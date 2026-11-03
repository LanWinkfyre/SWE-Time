# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression in handling of shorthand signed/unsigned types in function parameters (with bisect and test case)

The following reduced code snippet produces a warning:

```
a.cpp:1: warning: unable to resolve reference to `foo(float)' for \ref command
```

```cpp
/**
@brief Foo

The following produces a warning: @ref foo(float)
*/
struct Foo {
    /** @brief Float */
    void foo(float value);

    /** @brief Unsigned */
    void foo(unsigned value);
};

// to fix the warning, either:
// - comment out this definition,
// - or change both to say `unsigned int value`
void Foo::foo(unsigned value) {}
```

 In particular I think the check should explicitly check for `unsigned int` being unnamed parameter, while anything else (such as `unsigned value`) being named (and the same for `signed`). For completness, here's the (wrong) generated XML output:

```xml
      <memberdef kind="function" ...>
        <type>void</type>
        <definition>void Foo::foo</definition>
        <argsstring>(unsigned value)</argsstring>
        <name>foo</name>
        <param>
          <type>unsigned value</type>
        </param>
```

while it should be

```xml
      <memberdef kind="function" ...>
        <type>void</type>
        <definition>void Foo::foo</definition>
        <argsstring>(unsigned value)</argsstring>
        <name>foo</name>
        <param>
          <type>unsigned</type>
          <declname>value</declname>
        </param>
```
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `449a7e2b4ff114a72be573013558bae19672ebbc` and the full history behind it is present.
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
