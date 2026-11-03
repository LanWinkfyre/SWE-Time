# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
SqlServer.Types is 20% slower on .NET 8

### Description

In https://github.com/dotnet/runtime/issues/75455#issuecomment-1263821647 I got help to diagnose that due to how SqlServer.Types calls native code, it runs much slower with W^X enabled.

With .NET 8 I re-ran my benchmarks with W^X disabled and saw a 20% regression compared to .NET 7.
[STIntersection.zip](https://github.com/dotnet/runtime/files/13726984/STIntersection.zip)

Do you have an idea what might have caused this performance regression and if it's "by design"?

### Configuration

To make as fair a comparison between .NET 7 and .NET 8, I disabled Dynamic PGO, DATAS and W^X.

```
BenchmarkDotNet v0.13.10, Windows 10 (10.0.19045.3803/22H2/2022Update)
Intel Core i7-10750H CPU 2.60GHz, 1 CPU, 12 logical and 6 physical cores
.NET SDK 9.0.100-alpha.1.23619.5
  [Host]     : .NET 8.0.0 (8.0.23.53103), X64 RyuJIT AVX2
  Job-VCKSWC : .NET 7.0.14 (7.0.1423.51910), X64 RyuJIT AVX2
  Job-KIDGWI : .NET 8.0.0 (8.0.23.53103), X64 RyuJIT AVX2
  Job-WWREOB : .NET 8.0.0 (8.0.23.11008), X64 RyuJIT AVX2
  Job-ROIKLT : .NET 9.0.0 (9.0.23.61807), X64 RyuJIT AVX2

EnvironmentVariables=DOTNET_GCDynamicAdaptationMode=0,DOTNET_EnableWriteXorExecute=0,DOTNET_TieredPGO=0,DOTNET_TieredCompilation=0,DOTNET_TC_QuickJit=0  Platform=X64  Server=True
```

### Regression?

Yes.
The earliest .NET 8 runtime I could find was Preview1 which also had the regression.
If earlier runtime builds are available, I'd be happy to bisect this further.

### Data

| Method         | Runtime           | Mean     | Error    | StdDev   | Ratio | RatioSD | Code Size |
|--------------- |------------------ |---------:|---------:|---------:|------:|--------:|----------:|
| STIntersection | .NET 7.0          | 78.36 us | 1.019 us | 0.953 us |  1.00 |    0.00 |   7,411 B |
| STIntersection | .NET 8.0-Preview1 | 94.64 us | 0.939 us | 0.878 us |  1.21 |    0.02 |   6,980 B |
| STIntersection | .NET 8.0          | 96.58 us | 1.565 us | 1.675 us |  1.23 |    0.03 |   7,377 B |
| STIntersection | .NET 9.0          | 95.33 us | 1.588 us | 1.486 us |  1.22 |    0.03 |   7,152 B |



I haven't figured out how to instruct BDN to use `corerun`, but with the benchmark below the numbers are as follow:




```cs
var c = new Benchmark();
for (int i = 0; i < 100_000; i++) c.STIntersection();

var ts = Stopwatch.StartNew();
for (int i = 0; i < 100_000; i++) c.STIntersection();
var elapsed = ts.Elapsed / 100_000;
Console.WriteLine(elapsed.TotalMicroseconds);
```

When I figure out how to get BDN to use `corerun`, I'll add the jitted assembly.
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `8bd23f0792c6339478222ebc6635266e8f4098b4` and the full history behind it is present.
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
