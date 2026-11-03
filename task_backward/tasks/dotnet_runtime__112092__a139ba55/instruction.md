# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Assertion failed 'argInfo.argIsUsed == false' during 'Morph - Inlining'

Sample failure log: https://dev.azure.com/dnceng-public/public/_build/results?buildId=937252&view=logs&j=6a7e26fa-36e7-5a45-28af-dc6c8e6724e6&t=089ef86b-599a-543a-2c8c-82b31601e3ec

```
  ILC: /__w/1/s/src/coreclr/jit/fginline.cpp:1888
  ILC: Assertion failed 'argInfo.argIsUsed == false' in 'System.Threading.Tasks.Tests.ParallelForTests+MyPartitioner`1[System.__Canon]:GetDynamicPartitions():System.Collections.Generic.IEnumerable`1[System.__Canon]:this' during 'Morph - Inlining' (IL size 23; hash 0x3ce6bc1d; FullOpts)
  
/__w/1/s/artifacts/bin/coreclr/linux.x64.Checked/build/Microsoft.NETCore.Native.targets(316,5): error MSB3073: The command ""/__w/1/s/artifacts/bin/coreclr/linux.x64.Checked/x64/ilc/ilc" @"/__w/1/s/artifacts/obj/System.Threading.Tasks.Parallel.Tests/Release/net10.0/native/System.Threading.Tasks.Parallel.Tests.ilc.rsp"" exited with code 134. [/__w/1/s/src/libraries/System.Threading.Tasks.Parallel/tests/System.Threading.Tasks.Parallel.Tests.csproj]
```

This is failing in native AOT `OptimizationPreference=Speed` runs on both Windows and Linux. I.e. you need to add `/p:OptimizationPreference=Speed` to the build command line, in addition to `/p:TestNativeAot=true`.
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `e424e0538fcafa56802d6ee23263aa0772e327d3` and the full history behind it is present.
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
