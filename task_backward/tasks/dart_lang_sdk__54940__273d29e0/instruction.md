# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[gardening/vm] vm/dart/devirtualization_during_inlining_il_test not inlining on all bots



The tests
```
vm/dart/devirtualization_during_inlining_il_test Crash (expected Pass)
```
are failing on configurations
```
dartkp-weak-asserts-linux-release-x64
```

```
stdout:
matching IL (After AllocateRegisters) for test
Failed to match: Unmatched instruction: interpolate <- StaticCall({i: [boxed_index]}) in block B3
B0[GraphEntry] {
  v0 <- Constant[value: null]() T{Null, Null, +null}
  v79 <- UnboxedConstant[value: 0, representation: int64]() T{_Smi, _Smi}
  v80 <- UnboxedConstant[value: 10, representation: int64]() T{_Smi, _Smi}
  v81 <- UnboxedConstant[value: 1, representation: int64]() T{_Smi, _Smi}
}
B1[FunctionEntry] {
  v2 <- Parameter[index: 0]() T{TestIterable, TestIterable}
}
  CheckStackOverflow()
  Goto() goto [5]
B5[JoinEntry]
  v78 <- Phi(v79, v24) T{int}
  CheckStackOverflow()
  Branch if RelationalOp[kind: >=](v78, v80) then goto [4, 3]
B4[TargetEntry]
  ParallelMove()
  Return(v0)
B3[TargetEntry]
  ParallelMove()
  v24 <- BinaryInt64Op[op_kind: +](v78, v81) T{int}
  ParallelMove()
  v86 <- BoxInt64(v78)
  MoveArgument(v2)
  MoveArgument(v86)
  v25 <- StaticCall[function: TestIterable.elementAt](v2, v86) T{int?, +null}
  MoveArgument(v25)
  v11 <- StaticCall[function: _StringBase._interpolateSingle](v25) T{String, +null}
  MoveArgument(v11)
  StaticCall[function: printToConsole](v11)
  Goto() goto [5]

stderr:
Unhandled exception:
Failed to match
#0      FlowGraph.match (package:vm/testing/il_matchers.dart:49:9)
#1      matchIL$test (file:///b/s/w/ir/runtime/tests/vm/dart/devirtualization_during_inlining_il_test.dart:58:9)
#2      _LibraryMirror._invoke (dart:mirrors-patch/mirrors_impl.dart:1001:68)
#3      _ObjectMirror.invoke (dart:mirrors-patch/mirrors_impl.dart:250:25)
#4      TestCase.run (file:///b/s/w/ir/pkg/vm/bin/compare_il.dart:65:13)
#5      main (file:///b/s/w/ir/pkg/vm/bin/compare_il.dart:39:10)
<asynchronous suspension>

--- Re-run this test:
python3 tools/test.py -n dartkp-weak-asserts-linux-release-x64 vm/dart/devirtualization_during_inlining_il_test
```

Expected flow graph:

```dart
void matchIL$test(FlowGraph graph) {
  graph.match([
    match.block('Graph'),
    match.block('Function', [
      'obj' << match.Parameter(index: 0),
      match.CheckStackOverflow(),
      match.Goto('LoopHeader'),
    ]),
    'LoopHeader' <<
        match.block('Join', [
          'index' << match.Phi(match.any, 'inc'),
          match.CheckStackOverflow(),
          match.Branch(match.RelationalOp('index', match.any, kind: '>='),
              ifTrue: 'LoopExit', ifFalse: 'LoopBody'),
        ]),
    'LoopExit' <<
        match.block('Target', [
          match.Return(),
        ]),
    'LoopBody' <<
        match.block('Target', [
          'inc' << match.BinaryInt64Op('index', match.any),
          'boxed_index' << match.BoxInt64('index'),
          'interpolate' << match.StaticCall('boxed_index'),
          match.StaticCall('interpolate'),
          match.Goto('LoopHeader'),
        ]),
  ]);
}
```

It looks like the inliner is not inlining the supposed to be inlined methods:

```dart
class TestIterable extends IterableBase<int> {
  @pragma('vm:prefer-inline')
  TestIterator get iterator => TestIterator(this);

  @override
  int get length => 10;

  @pragma('vm:prefer-inline')
  int elementAt(int index) {
    return index;
  }
}
```

Logs: https://dart-ci.appspot.com/log/vm-kernel-precomp-linux-release-x64/dartkp-weak-asserts-linux-release-x64/15940/vm/dart/devirtualization_during_inlining_il_test

Will bisect locally.




Ensuring SDK repo in /usr/local/google/home/dacoharkes/dart-sdk/sdk/.




 

 

 

 

 



Ran twice, ended with the same result.

This seems an unlikely commit to cause this.

Test history on all the bots: https://dart-ci.web.app/#showLatestFailures=false&test=vm/dart/devirtualization_during_inlining_il_test

Also failing on another bot already: https://dart-current-results.web.app/#/filter=vm/dart/devirtualization_during_inlining_il_test&showAll

Log on other bot: https://dart-ci.appspot.com/log/any/vm-aot-optimization-level-linux-release-x64/134/vm/dart/devirtualization_during_inlining_il_test

Seems to be the same issue, not inlining.

* dartkp-weak-asserts-linux-release-x64
* vm-aot-optimization-level-linux-release-x64

Previous failure approved on:

* https://github.com/dart-lang/sdk/issues/53608
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `a626c89b6a6555c211337511382ff2179700a8df` and the full history behind it is present.
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
