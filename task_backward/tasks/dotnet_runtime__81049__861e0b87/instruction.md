# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Random jit stress failures in JIT\Directed\arglist\vararg

https://dev.azure.com/dnceng-public/public/_build/results?buildId=144710&view=ms.vss-test-web.build-test-results-tab

Windows x64

```
set DOTNET_TieredCompilation=0
set DOTNET_JitStress=3cb

  Starting:    JIT.Directed.XUnitWrapper (parallel test collections = on, max threads = 4)
    JIT\Directed\arglist\vararg_TargetWindows\vararg_TargetWindows.cmd [FAIL]

      Failure: check_passing_four_three_double_struct(first, second, third, fourth)
      Failure: TestPassingTwentyFourByteStructs()

      240 Tests run. 238 Passed, 2 Failed.
```

  Investigating in more detail now.
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `0ca364767715fee7bc9d0273eec4f30a3c6cc8f0` and the full history behind it is present.
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
