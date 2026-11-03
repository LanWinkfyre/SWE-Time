# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
dartvm segfaults when passing --print_metrics

Passing the `--print_metrics` flag is causing the VM to segfault. You can repro by running hello world:

``` sh
sdk/bin/dart --print_metrics hello_world.dart
```

output is

```
hello world
Printing metrics for hi.dart$main-539982512
heap.old.used 0.000 b (0)
heap.old.used.max 0.000 b (0)
heap.old.capacity 0.000 b (0)
heap.old.capacity.max 1536.000 kb (1572864)
heap.old.external 0.000 b (0)
heap.new.used 0.000 b (0)
heap.new.used.max 0.000 b (0)
heap.new.capacity 0.000 b (0)
heap.new.capacity.max 1024.000 kb (1048576)
heap.new.external 0.000 b (0)
heap.global.used 0.000 b (0)
heap.global.used.max 0.000 b (0)

Segmentation fault (core dumped)
```

/cc @johnmccutchan @turnidge 


@johnmccutchan @a-siva
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `6859412facdf673013820715723305313fba5c53` and the full history behind it is present.
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
