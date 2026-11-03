# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Test failure: access violation in cpblk tests

Affected tests:
- `JIT/Directed/PREFIX/volatile/1/cpblk/cpblk.sh`
- `JIT\\Directed\\PREFIX\\volatile\\1\\cpblk\\cpblk.cmd`

Runfo hits for [last 30 days](https://runfo.azurewebsites.net/search/tests/?q=started%3A%7E30+definition%3Aruntime+name%3A%22cpblk%22) as of 10/3:
- First occurrence on 9/30 in rolling run [36073](https://runfo.azurewebsites.net/view/build/?number=36073)
- Happened **2x-3x in each Rolling run** in last 3 days across various platforms (all are **arm64** -- on all platforms - Linux, OSX and Windows)

### Original Report

arm64, JitStress

Also fails in MinOpts

https://dev.azure.com/dnceng-public/public/_build/results?buildId=37829&view=ms.vss-test-web.build-test-results-tab&runId=754244&paneView=debug&resultId=108471

Started with 20220929.1 build:
https://dev.azure.com/dnceng-public/public/_build/results?buildId=37829&view=results

Tests:

JIT\\Directed\\PREFIX\\unaligned\\2\\cpblk\\cpblk.cmd
JIT\\IL_Conformance\\Old\\Conformance_Base\\ldc_c_cpblk\\ldc_c_cpblk.cmd
JIT\\Directed\\PREFIX\\unaligned\\4\\cpblk\\cpblk.cmd
JIT\\IL_Conformance\\Old\\Base\\cpblk\\cpblk.cmd
JIT\\IL_Conformance\\Old\\Conformance_Base\\c_cpblk\\c_cpblk.cmd
JIT\\IL_Conformance\\Old\\Conformance_Base\\cpblk\\cpblk.cmd
JIT\\Directed\\PREFIX\\unaligned\\1\\cpblk\\cpblk.cmd

Example:
```
  Starting:    JIT.Directed.XUnitWrapper (parallel test collections = on, max threads = 8)
    JIT\Directed\PREFIX\unaligned\4\cpblk\cpblk.cmd [FAIL]
      Fatal error. System.AccessViolationException: Attempted to read or write protected memory. This is often an indication that other memory is corrupt.
         at _cpblk.main(System.String[])
```

@dotnet/jit-contrib 
<!--Known issue error report start -->
### Report
#### Summary
|24-Hour Hit Count|7-Day Hit Count|1-Month Count|
|---|---|---|
|0|0|0|
<!--Known issue error report end -->
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `ca6fb31c65e7c26d1d3096133a1d862bd8af086d` and the full history behind it is present.
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
