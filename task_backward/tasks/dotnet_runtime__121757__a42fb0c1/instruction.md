# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Assertion failed '!op1->isUsedFromMemory()' in 'System.Drawing.Printing.PrinterSettings:set_Copies(short):this' during 'Generate code'

Native AOT outerloop test runs on ARM64 are broken with the above assertion:

https://dev.azure.com/dnceng-public/public/_build/results?buildId=1205834&view=logs&j=2f6a7d26-0d60-5ade-d191-981fe0847989&t=950a5a68-ae8a-5bb4-8cad-fb293bb99dc4&l=9014

```
ILC: /__w/1/s/src/coreclr/jit/codegenarm64.cpp:4998
  ILC: Assertion failed '!op1->isUsedFromMemory()' in 'System.Drawing.Printing.PrinterSettings:set_Copies(short):this' during 'Generate code' (IL size 62; hash 0x062727f7; FullOpts)
  
##[error]artifacts/bin/coreclr/linux.arm64.Checked/build/Microsoft.NETCore.Native.targets(330,5): error MSB3073: (NETCORE_ENGINEERING_TELEMETRY=Build) The command ""/__w/1/s/artifacts/bin/coreclr/linux.arm64.Checked/x64/ilc/ilc" @"/__w/1/s/artifacts/obj/System.Resources.ResourceManager.Tests/Release/net10.0-unix/native/System.Resources.ResourceManager.Tests.ilc.rsp"" exited with code 134.
/__w/1/s/artifacts/bin/coreclr/linux.arm64.Checked/build/Microsoft.NETCore.Native.targets(330,5): error MSB3073: The command ""/__w/1/s/artifacts/bin/coreclr/linux.arm64.Checked/x64/ilc/ilc" @"/__w/1/s/artifacts/obj/System.Resources.ResourceManager.Tests/Release/net10.0-unix/native/System.Resources.ResourceManager.Tests.ilc.rsp"" exited with code 134. [/__w/1/s/src/libraries/System.Runtime/tests/System.Resources.ResourceManager.Tests/System.Resources.ResourceManager.Tests.csproj::TargetFramework=net10.0-unix]
```



Cc @jakobbotsch @EgorBo @jonathandavies-arm
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `ea8d8a0339bdf8b736ef5706900bab48429d1cf6` and the full history behind it is present.
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
