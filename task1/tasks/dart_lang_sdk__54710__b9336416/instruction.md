# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
dartfuzz: divergence between AOT/DebugX64 and other configurations (AOT/ReleaseX64, JIT/DebugX64)


```
dart runtime/tools/dartfuzz/dartfuzz.dart --no-fp --no-ffi --flat --seed 2175016768 fuzz.dart
```

(1)
```
out/DebugX64/dart fuzz.dart >out1
```

(2)
```
DART_CONFIGURATION='DebugX64' pkg/vm/tool/precompiler2 fuzz.dart foo.snapshot
DART_CONFIGURATION='DebugX64' pkg/vm/tool/dart_precompiled_runtime2 foo.snapshot >out2
```

(3)
```
DART_CONFIGURATION='ReleaseX64' pkg/vm/tool/precompiler2 fuzz.dart foo.snapshot
DART_CONFIGURATION='ReleaseX64' pkg/vm/tool/dart_precompiled_runtime2 foo.snapshot >out3
```

(1) and (3) result in the same output, (2) doesn't match those.

```
diff out1 out3
diff out1 out2
9484a9485
> [4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187]
12932a12934
> [4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187]
15517a15520
> [4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187]
18103,18106c18106
< [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
< [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
< [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
< [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
---
> [4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187, 4092851187]
```


 /cc @sstrickl
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `ba8b4704e94035fb7e10c520c0a504dc8010765d` and the full history behind it is present.
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
