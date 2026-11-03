# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Test failure JIT\\Regression\\VS-ia64-JIT\\V2.0-Beta2\\b311420\\b311420\\b311420.cmd

Run: [runtime-coreclr r2r 20220320.1](https://dev.azure.com/dnceng/public/_build/results?buildId=1673361&view=ms.vss-test-web.build-test-results-tab&runId=45918680&resultId=107303&paneView=debug)

Failed test:
```
R2R windows arm Checked no_tiered_compilation @ Windows.10.Arm64v8.Open

- JIT\\Regression\\VS-ia64-JIT\\V2.0-Beta2\\b311420\\b311420\\b311420.cmd
- JIT\\Regression\\VS-ia64-JIT\\V1.2-M02\\b28158\\b28158\\b28158.cmd
- JIT\\jit64\\opt\\cse\\HugeField2\\HugeField2.cmd
- JIT\\opt\\virtualstubdispatch\\hashcode\\ctest1_cs_r\\ctest1_cs_r.cmd
- JIT\\opt\\virtualstubdispatch\\hashcode\\ctest1_cs_d\\ctest1_cs_d.cmd
- JIT\\opt\\virtualstubdispatch\\hashcode\\ctest1_cs_do\\ctest1_cs_do.cmd
- JIT\\opt\\virtualstubdispatch\\hashcode\\ctest1_cs_do\\ctest1_cs_do.cmd
- JIT\\jit64\\opt\\cse\\HugeField1\\HugeField1.cmd
- JIT\\opt\\virtualstubdispatch\\bigvtbl\\bigvtbl_cs_do\\bigvtbl_cs_do.cmd
- JIT\\opt\\virtualstubdispatch\\bigvtbl\\bigvtbl_cs_r\\bigvtbl_cs_r.cmd
- JIT\\opt\\virtualstubdispatch\\bigvtbl\\bigvtbl_cs_d\\bigvtbl_cs_d.cmd
- JIT\\opt\\virtualstubdispatch\\bigvtbl\\bigvtbl_cs_ro\\bigvtbl_cs_ro.cmd
- JIT\\jit64\\hfa\\main\\testB\\hfa_nf0B_r\\hfa_nf0B_r.cmd
- JIT\\jit64\\mcc\\interop\\mcc_i04\\mcc_i04.cmd
- JIT\\jit64\\mcc\\interop\\mcc_i17\\mcc_i17.cmd
- JIT\\opt\\virtualstubdispatch\\manyintf\\ctest_cs_r\\ctest_cs_r.cmd

R2R windows arm Checked @ Windows.10.Arm64v8.Open

- JIT\\Regression\\VS-ia64-JIT\\V2.0-Beta2\\b311420\\b311420\\b311420.cmd
- JIT\\Regression\\VS-ia64-JIT\\V1.2-M02\\b28158\\b28158\\b28158.cmd
- JIT\\jit64\\opt\\cse\\HugeField2\\HugeField2.cmd
- JIT\\opt\\virtualstubdispatch\\hashcode\\ctest1_cs_d\\ctest1_cs_d.cmd
- Loader\\classloader\\MethodImpl\\CovariantReturns\\UnitTest\\UnitTestMultiModule\\UnitTestMultiModule.cmd
- JIT\\opt\\virtualstubdispatch\\hashcode\\ctest1_cs_do\\ctest1_cs_do.cmd
- JIT\\opt\\virtualstubdispatch\\hashcode\\ctest1_cs_ro\\ctest1_cs_ro.cmd
- JIT\\opt\\virtualstubdispatch\\bigvtbl\\bigvtbl_cs_ro\\bigvtbl_cs_ro.cmd
- JIT\\jit64\\opt\\cse\\HugeField1\\HugeField1.cmd
- JIT\\opt\\virtualstubdispatch\\bigvtbl\\bigvtbl_cs_r\\bigvtbl_cs_r.cmd
```
**Error message:**
```
Could Not Find D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\IL-CG2\composite-r2r.dll
Could Not Find D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\b311420.dll.rsp
Failed to load: 'D:\h\w\AB170977\p\coreclr.dll'. Error: 0x000000c1

Return code:      1
Raw output file:      D:\h\w\AB170977\w\B1180983\uploads\Reports\JIT.Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\b311420.output.txt
Raw output:
BEGIN EXECUTION
b311420.dll
1 file(s) copied.
Response file: D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\b311420.dll.rsp
D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\IL-CG2\b311420.dll
-o:D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\b311420.dll
--targetarch:arm
--verify-type-and-field-layout
--method-layout:random
-r:D:\h\w\AB170977\p\System..dll
-r:D:\h\w\AB170977\p\Microsoft..dll
-r:D:\h\w\AB170977\p\mscorlib.dll
-r:D:\h\w\AB170977\p\netstandard.dll
-O
" "dotnet" "D:\h\w\AB170977\p\crossgen2\crossgen2.dll" @"D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\b311420.dll.rsp"   -r:D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\IL-CG2*.dll"
Emitting R2R PE file: D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\b311420.dll
"D:\h\w\AB170977\p\corerun.exe" -p "System.Reflection.Metadata.MetadataUpdater.IsSupported=false"  b311420.dll
Expected: 100
Actual: -1
END EXECUTION - FAILED
FAILED
Test Harness Exitcode is : 1
To run the test:

set CORE_ROOT=D:\h\w\AB170977\p
D:\h\w\AB170977\w\B1180983\e\JIT\Regression\VS-ia64-JIT\V2.0-Beta2\b311420\b311420\b311420.cmd
Expected: True
Actual:   False


Stack trace
   at JIT_Regression._VS_ia64_JIT_V2_0_Beta2_b311420_b311420_b311420_._VS_ia64_JIT_V2_0_Beta2_b311420_b311420_b311420_cmd()
```

> Failed to load: 'D:\h\w\AB170977\p\coreclr.dll'. Error: 0x000000c1

I ran into this issue on Windows ARM32 locally as well while trying to investigate #66424.
FWIW, 0xc1 is `ERROR_BAD_EXE_FORMAT`.  @janvorli can you take a look?
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `7a01e0f14f8df4992b046096093224ce53ec7a59` and the full history behind it is present.
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
