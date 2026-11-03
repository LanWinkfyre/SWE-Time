# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Reflecting a class with call() throws in dart2js

## Problem:
In dart2js the following throws. This is only an issue with Dart 1.22.0 and works fine in Dart 1.21.1.

### Code:
```dart
import 'dart:mirrors';

void main() {
  InstanceMirror mirror = reflect(new A());

  mirror.type;
}

class A {
  call() {
    return null;
  }
}
```

### Error:
```
Uncaught Error: Unsupported operation: Cannot find class for: () => dynamic
    at Object.wrapException (index.dart.js:6266)
    at Object.reflectClassByName (index.dart.js:9814)
    at Object.reflectClassByMangledName (index.dart.js:9789)
    at Object.reflectType (index.dart.js:9778)
    at JsInstanceMirror.dart.JsInstanceMirror.get$type (index.dart.js:10774)
    at StaticClosure.dart.main (index.dart.js:39025)
    at _IsolateContext.eval$1 (index.dart.js:4833)
    at Object.startRootIsolate (index.dart.js:4431)
    at index.dart.js:41128
    at index.dart.js:41129
```

Bisected:



Passing on the torch @rakudrama
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `cdda898b3cf85e66d41a6570e1d1a1c277903521` and the full history behind it is present.
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
