# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
dart2js compiler crashing due to visiting properties with value child of null

I'm getting the following assert crash on two very large codesets, so unfortunately I don't have a smaller or external-friendly reproduction source set to provide alongside the error.

Here's the output from the compiler:

---------

Internal Error: The compiler crashed when compiling this element.

The compiler is broken.

When compiling the above element, the compiler crashed. It is not

not. Regardless, the compiler should not crash.

The Dart team would greatly appreciate if you would take a moment to
report this problem at http://dartbug.com/new.

Please include the following information:

* the name and version of your operating system,



* the entire message you see here (including the full stack trace
  below as well as the source location above).

The compiler crashed: NoSuchMethodError: The method 'accept' was called on null.
Receiver: null
Tried calling: accept<dynamic>(Instance of 'TokenCounter')
#0      Object.noSuchMethod (dart:core-patch/object_patch.dart:50:5)
#1      Property.visitChildren (package:js_ast/src/nodes.dart:1765:11)
#2      BaseVisitor.visitNode (package:js_ast/src/nodes.dart:89:10)
#3      TokenCounter.visitNode (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js/js.dart:114:13)
#4      BaseVisitor.visitProperty (package:js_ast/src/nodes.dart:175:37)
#5      Property.accept (package:js_ast/src/nodes.dart:1758:50)
#6      ObjectInitializer.visitChildren (package:js_ast/src/nodes.dart:1739:44)
#7      BaseVisitor.visitNode (package:js_ast/src/nodes.dart:89:10)
#8      TokenCounter.visitNode (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js/js.dart:114:13)
#9      BaseVisitor.visitExpression (package:js_ast/src/nodes.dart:121:41)
#10     BaseVisitor.visitObjectInitializer (package:js_ast/src/nodes.dart:174:55)
#11     ObjectInitializer.accept (package:js_ast/src/nodes.dart:1733:50)
#12     Assignment.visitChildren (package:js_ast/src/nodes.dart:1133:30)
#13     BaseVisitor.visitNode (package:js_ast/src/nodes.dart:89:10)
#14     TokenCounter.visitNode (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js/js.dart:114:13)
#15     BaseVisitor.visitExpression (package:js_ast/src/nodes.dart:121:41)
#16     BaseVisitor.visitAssignment (package:js_ast/src/nodes.dart:127:41)
#17     Assignment.accept (package:js_ast/src/nodes.dart:1126:50)
#18     ExpressionStatement.visitChildren (package:js_ast/src/nodes.dart:514:16)
#19     BaseVisitor.visitNode (package:js_ast/src/nodes.dart:89:10)
#20     TokenCounter.visitNode (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js/js.dart:114:13)
#21     BaseVisitor.visitStatement (package:js_ast/src/nodes.dart:95:39)
#22     BaseVisitor.visitExpressionStatement (package:js_ast/src/nodes.dart:100:59)
#23     ExpressionStatement.accept (package:js_ast/src/nodes.dart:508:50)
#24     Block.visitChildren (package:js_ast/src/nodes.dart:491:55)
#25     BaseVisitor.visitNode (package:js_ast/src/nodes.dart:89:10)
#26     TokenCounter.visitNode (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js/js.dart:114:13)
#27     BaseVisitor.visitStatement (package:js_ast/src/nodes.dart:95:39)
#28     BaseVisitor.visitBlock (package:js_ast/src/nodes.dart:99:31)
#29     Block.accept (package:js_ast/src/nodes.dart:485:50)
#30     Fun.visitChildren (package:js_ast/src/nodes.dart:1460:10)
#31     BaseVisitor.visitNode (package:js_ast/src/nodes.dart:89:10)
#32     TokenCounter.visitNode (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js/js.dart:114:13)
#33     BaseVisitor.visitExpression (package:js_ast/src/nodes.dart:121:41)
#34     BaseVisitor.visitFun (package:js_ast/src/nodes.dart:151:27)
#35     Fun.accept (package:js_ast/src/nodes.dart:1453:50)
#36     TokenCounter.countTokens (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js/js.dart:118:39)
#37     Iterable.forEach (dart:core/iterable.dart:277:30)
#38     ModelEmitter.emitProgram (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js_emitter/startup_emitter/model_emitter.dart:195:34)
#39     Emitter.emitProgram (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js_emitter/startup_emitter/emitter.dart:69:21)
#40     CodeEmitterTask.assembleProgram.<anonymous closure> (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js_emitter/code_emitter_task.dart:199:26)
#41     CompilerTask.measure (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/common/tasks.dart:64:51)
#42     CodeEmitterTask.assembleProgram (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js_emitter/code_emitter_task.dart:169:12)
#43     JavaScriptBackend.assembleProgram (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/js_backend/backend.dart:702:31)
#44     Compiler.generateJavaScriptCode (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/compiler.dart:388:31)
#45     Compiler.compileFromKernel.<anonymous closure> (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/compiler.dart:429:9)
#46     CompilerTask.measureSubtask (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/common/tasks.dart:179:35)
#47     Compiler.compileFromKernel (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/compiler.dart:403:14)
#48     Compiler.runInternal (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/compiler.dart:272:13)
<asynchronous suspension>
#49     Compiler.run.<anonymous closure>.<anonymous closure> (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/compiler.dart:223:38)
#50     new Future.sync (dart:async/future.dart:224:31)
#51     Compiler.run.<anonymous closure> (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/compiler.dart:223:20)
#52     CompilerTask.measureSubtask (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/common/tasks.dart:179:35)
#53     Compiler.run (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/compiler.dart:220:41)
#54     CompilerImpl.run.<anonymous closure>.<anonymous closure> (file:///usr/local/google/home/sstrickl/dart/sdk/pkg/compiler/lib/src/apiimpl.dart:91:22)
#55     _RootZone.runUnary (dart:async/zone.dart:1379:54)
#56     _FutureListener.handleValue (dart:async/future_impl.dart:126:18)
#57     Future._propagateToListeners.handleValueCallback (dart:async/future_impl.dart:639:45)
#58     Future._propagateToListeners (dart:async/future_impl.dart:668:32)
#59     Future._completeWithValue (dart:async/future_impl.dart:483:5)
#60     Future._asyncComplete.<anonymous closure> (dart:async/future_impl.dart:513:7)
#61     _microtaskLoop (dart:async/schedule_microtask.dart:41:21)
#62     _startMicrotaskLoop (dart:async/schedule_microtask.dart:50:5)
#63     _runPendingImmediateCallback (dart:isolate-patch/isolate_patch.dart:115:13)
#64     _RawReceivePortImpl._handleMessage (dart:isolate-patch/isolate_patch.dart:172:5)


Tested a few release versions, and found this was introduced between 2.2.1-dev.1.1 and 2.2.1-dev.2.0.
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `3e12bdd717a5169ee3fa3565a97de62a2bbbd83c` and the full history behind it is present.
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
