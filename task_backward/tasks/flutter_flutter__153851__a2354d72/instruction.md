# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Drawer is snapping into place while dragging half way

### Steps to reproduce

1. Slowly drag the Drawer to open/close
2. Do not swipe or release, keep dragging until fully closed/open


### Expected results

Drawer will follow the position of my finger while dragging

### Actual results

Drawer will snap to fully closed or fully open position while my finger is still dragging half way.

### Code sample

<details open><summary>Code sample</summary>

```dart
 Scaffold(
      drawer: Drawer(),
    );
```

</details>


### Screenshots or Video

<details open>
<summary>Screenshots / Video demonstration</summary>

[Upload media here]

</details>


### Logs

<details open><summary>Logs</summary>

```console
[Paste your logs here]
```

</details>


### Flutter Doctor output

<details open><summary>Doctor output</summary>



</details>


 Kindly cc @nate-thegrate for thoughts.
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `b74fa8afc7e2365f96098e6ff0fb150beb22682a` and the full history behind it is present.
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
