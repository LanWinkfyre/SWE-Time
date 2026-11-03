# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[gardening] flutter_regress_91370_il_test fails



The tests
```
vm/dart_2/flutter_regress_91370_il_test Crash (expected Pass)
```
are failing on configurations
```
dartkp-linux-debug-x64
dartkp-linux-release-x64
```

```
DART_CONFIGURATION=ReleaseX64 /b/s/w/ir/pkg/vm/tool/compare_il /b/s/w/ir/runtime/tests/vm/dart_2/flutter_regress_91370_il_test.dart /b/s/w/ir/out/ReleaseX64/generated_compilations/dartkp-linux-release-x64/runtime_tests_vm_dart_2_flutter_regress_91370_il_test/out.il

exit code:
255

stdout:
matching IL (Before LICM, After LICM) for testNarrowingThroughIsCheckWithTypeArgMonomorphic
... ok
matching IL (Before LICM, After LICM) for testNarrowingThroughIndexedLoadFromFixedArray
... ok
matching IL (Before LICM, After LICM) for testNarrowingThroughThisCallWithPositionalParam
Failed to match: Unmatched instruction: Branch({cc: StrictCompare({d: {kind: ===}, i: [this_cid,*]}), s: [B3,*]}) in block B3
B0[GraphEntry]
  v0 <- Constant()
  v1 <- Constant()
  v4 <- Constant()
  v7 <- Constant()
  v10 <- Constant()
  v15 <- Constant()
  v54 <- UnboxedConstant()
  v55 <- UnboxedConstant()
  v75 <- UnboxedConstant()
  v76 <- UnboxedConstant()
  v77 <- UnboxedConstant()
B6[FunctionEntry]
  v2 <- Parameter[index: 0]()
  v3 <- Parameter[index: 1]()
  CheckStackOverflow()
  v5 <- LoadField[slot: :type_arguments](v2)
  v6 <- AssertAssignable(v3, v4, v5, v0)
  Goto()
B5[JoinEntry]
  v8 <- Phi(v75, v14)
  v9 <- Phi(v75, v16)
  CheckStackOverflow()
  Branch()
B3[TargetEntry]
  v53 <- LoadClassId(v2)
  Branch()
B8[TargetEntry]
  v30 <- Redefinition(v6)
  v29 <- Redefinition(v2)
  v26 <- LoadField[slot: data](v30)
  v27 <- LoadField[slot: str](v26)
  v61 <- LoadField[slot: String.length](v27)
  v72 <- UnboxInt64(v61)
  Goto()
B15[TargetEntry]
  Branch()
B10[TargetEntry]
  v42 <- Redefinition(v6)
  v41 <- Redefinition(v2)
  v38 <- LoadField[slot: data](v42)
  v39 <- LoadField[slot: str](v38)
  v66 <- LoadField[slot: String.length](v39)
  v73 <- UnboxInt64(v66)
  Goto()
B16[TargetEntry]
  v52 <- Redefinition(v6)
  v51 <- Redefinition(v2)
  Goto()
B17[JoinEntry]
  v56 <- Phi(v72, v73, v75)
  v14 <- BinaryInt64Op(v8, v56)
  v16 <- BinaryInt64Op(v9, v77)
  Goto()
B4[TargetEntry]
  Return(v8)

stderr:
Unhandled exception:
Failed to match
#0      FlowGraph.match (package:vm/testing/il_matchers.dart:44:9)
#1      matchIL$testNarrowingThroughThisCallWithPositionalParam (file:///b/s/w/ir/runtime/tests/vm/dart_2/flutter_regress_91370_il_test.dart:257:26)
#2      _LibraryMirror._invoke (dart:mirrors-patch/mirrors_impl.dart:999:68)
#3      _ObjectMirror.invoke (dart:mirrors-patch/mirrors_impl.dart:248:25)
#4      TestCase.run (file:///b/s/w/ir/pkg/vm/bin/compare_il.dart:65:13)
#5      main (file:///b/s/w/ir/pkg/vm/bin/compare_il.dart:39:10)
<asynchronous suspension>

--- Re-run this test:
python3 tools/test.py -n dartkp-linux-release-x64 vm/dart_2/flutter_regress_91370_il_test
```

https://dart-ci.appspot.com/log/vm-kernel-precomp-linux-release-x64/dartkp-linux-release-x64/15779/vm/dart_2/flutter_regress_91370_il_test

 I'll bisect locally.
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `69afe5a40710f45e7d7a5d749ff31fc30832ed08` and the full history behind it is present.
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
