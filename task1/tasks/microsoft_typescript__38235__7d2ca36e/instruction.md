# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
No-op mapped type not assignable; but original type is assignable

<!-- 🚨 STOP 🚨 𝗦𝗧𝗢𝗣 🚨 𝑺𝑻𝑶𝑷 🚨

Half of all issues filed here are duplicates, answered in the FAQ, or not appropriate for the bug tracker. Even if you think you've found a *bug*, please read the FAQ first, especially the Common "Bugs" That Aren't Bugs section!

Please help us by doing the following steps before logging an issue:
  * Search: https://github.com/Microsoft/TypeScript/search?type=Issues
  * Read the FAQ: https://github.com/Microsoft/TypeScript/wiki/FAQ

Please fill in the *entire* template below.
-->

<!--
Please try to reproduce the issue with the latest published version. It may have already been fixed.
For npm: `typescript@next`
This is also the 'Nightly' version in the playground: http://www.typescriptlang.org/play/?ts=Nightly
-->
**TypeScript Version:**  3.8.3

<!-- Search terms you tried before logging this (so others can find this issue more easily) -->
**Search Terms:**

no-op mapped type, assignable

**Code**

```ts
type Foo<IdentifierT extends Record<PropertyKey, PropertyKey>> =
    IdentifierT
;

type Bar<IdentifierT extends Record<PropertyKey, PropertyKey>, T> =
    {
        [k in keyof T] : Foo<IdentifierT & { k : k }>
    }
;

type Merge2<T> = { [k in keyof T] : T[k] }
type Bar2<IdentifierT extends Record<PropertyKey, PropertyKey>, T> =
    {
        [k in keyof T]: Foo<Merge2<IdentifierT & { k: k }>>
        //                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        //                  Works in 3.5.1
        //                  Works in 3.6.3
        //                  Works in 3.7.5
        //                  Fails in 3.8.3
    }
;

type Identity<T> = T;
type Merge3<T> = Identity<{ [k in keyof T] : T[k] }>
type Bar3<IdentifierT extends Record<PropertyKey, PropertyKey>, T> =
    {
        [k in keyof T]: Foo<Merge3<IdentifierT & { k: k }>>
        //                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        //                  Works in 3.5.1
        //                  Works in 3.6.3
        //                  Works in 3.7.5
        //                  Fails in 3.8.3
    }
;
```

**Expected behavior:**

Passes type checking

**Actual behavior:**

Fails in TS 3.8.3

**Playground Link:** 

[Playground](https://www.typescriptlang.org/play/#code/C4TwDgpgBAYg9nAPASQCYQHbAJYDNsQBOAKlBAB7CaoDOUAShAMZyGqIAKhckhoA0hBAAaKAFcMAawxwA7hgB8CqAF4AsACgo2qGkw58RYpoDcmzaEhQAQgENCKdFjwESZStTqMWbTt14CQqJcPESBIAqixMrqWjoA3po6yVAA2pJQ2BhQkkJwuFDEALpQAFywCI76LkZQAGRQ8TllzQC+Ckk6rabmGpbQALJEAOYQAEyI0aqNaRlZOXkFxS3E6SXdfeDQdoQTes6GbhRUGLQMzKzsIQEggiJQ12G3QpGFMZ3aiXEps5nZuSB8oUiuV4EghoRRnsnAZXKQGk1JOUMu0Ot8UgB6DE-HEpAB+BMJROJJNJeI+mOxuOpAHVWJI6PMAMwAOgArCyAIwU5JY6m0+mM7KsgBsLKZPJ0fP5OLphAZfygrIA7OzJdppTKUjBbNgADZCpUsgAc4opGzMGgsW10MOwoEmMUKlv6UAhoyZjum+xwDqa6UVAKBy3Kq0k6zRrp2np9NSOHlOXguvkefGe91T4VeU1iyS+uID8yDSxBFXBIwgMbth3hMyRbSU6qgmq1OjJ7Y7BKbLdbUDlCuZ7K53apve0-cNorN6N5o7HE8VKrVM6lc97Ov1k5N0+SFqAA)

**Related Issues:**

Not that I could find

-----

Well, it isn't exactly a "no-op" mapped type.

It will strip call and constructor signatures, but "no-op mapped type" was the best name I had for it.

I just bisected the ts compiler to find the cause using

build.sh
```sh
#!/bin/bash
set -e -x
bisect_error=125

yarn install --silent || exit $bisect_error
gulp -L local || exit $bisect_error

node built/local/tsc.js --noEmit ../example.ts
```




bisect reports:
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `d9ad27f2dd17cc1413b7d442d2915b13e0347d3e` and the full history behind it is present.
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
