# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[Android]: Delete button of Samsung keyboard is not deleting text.

<!-- Thank you for using Flutter!

     If you are looking for support, please check out our documentation
     or consider asking a question on Stack Overflow:
      * https://flutter.dev/
      * https://api.flutter.dev/
      * https://stackoverflow.com/questions/tagged/flutter?sort=frequent

     If you have found a bug or if our documentation doesn't have an answer
     to what you're looking for, then fill out the template below. Please read
     our guide to filing a bug first: https://flutter.dev/docs/resources/bug-reports
-->

## Steps to Reproduce

See also the bug report here: https://github.com/ueman/feedback/issues/120

1. Clone https://github.com/ueman/feedback/ 
2. Run the example
3. Use the example as shown in this [video](https://www.youtube.com/watch?v=gZmws1kgt58)

**Expected results:** 
Delete button removes the last character.
I can reproduce it on a Samsung Galaxy A40 with Android 11. A user from the linked issue sees the same behavior on a Samsung Galaxy A21s on Android 11 with Samsung Keyboard. If you're using Gboard it works as expected. 

**Actual results:** 
Delete button does nothing.

<details>
  <summary>Logs</summary>

There are also some more infos on the linked issue here: https://github.com/ueman/feedback/issues/120

`flutter run --verbose` does not give any output while pressing the delete button.
```
```

<!--
     Run `flutter analyze` and attach any output of that command below.
     If there are any analysis errors, try resolving them before filing this issue.
-->

```
flutter analyze
Analyzing feedback...                                                   
No issues found! (ran in 3.3s)
```

<!-- Finally, paste the output of running `flutter doctor -v` here. -->



</details>
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `a921c1cf3d2616704bcbb83ab13d89e39be0c97c` and the full history behind it is present.
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
