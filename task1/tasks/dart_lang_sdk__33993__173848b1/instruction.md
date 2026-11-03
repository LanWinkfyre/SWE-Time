# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Fasta crashing when building flutter_tools

When rolling the Dart SDK into Flutter, running `flutter doctor` with `$FLUTTER_ROOT/bin/internal/engine.version` set to `503ba7c4103d2cd40161019d94a15c74ad06eaad` produces the multiple failures similar to the one below:

```
Building flutter tool...
Failed to precompile coverage:run_and_collect:
Crash when compiling file:///usr/local/google/home/bkonyi/.pub-cache/hosted/pub.dartlang.org/async-2.0.8/lib/src/future_group.dart,
at character offset 2308:
NoSuchMethodError: Closure call with mismatched arguments: function 'name'
Receiver: null
Tried calling: name
#0      Object.noSuchMethod (dart:core-patch/dart:core/object_patch.dart:46)
#1      TypeInferrerImpl.findInterfaceMember (package:front_end/src/fasta/type_inference/type_inferrer.dart:866)
#2      TypeInferrerImpl.findMethodInvocationMember (package:front_end/src/fasta/type_inference/type_inferrer.dart:882)
#3      ComplexAssignmentJudgment._inferRhs (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:585)
#4      PropertyAssignmentJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:2422)
#5      ShadowTypeInferrer.inferExpression (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:3342)
#6      ExpressionStatementJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:974)
#7      ShadowTypeInferrer.inferStatement (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:3421)
#8      BlockJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:299)
#9      ShadowTypeInferrer.inferStatement (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:3421)
#10     TypeInferrerImpl.inferLocalFunction (package:front_end/src/fasta/type_inference/type_inferrer.dart:1595)
#11     FunctionNodeJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:1376)
#12     FunctionExpressionJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:1432)
#13     ShadowTypeInferrer.inferExpression (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:3342)
#14     TypeInferrerImpl.inferInvocation.<anonymous closure> (package:front_end/src/fasta/type_inference/type_inferrer.dart:1362)
#15     TypeInferrerImpl._forEachArgument (package:front_end/src/fasta/type_inference/type_inferrer.dart:2013)
#16     TypeInferrerImpl.inferInvocation (package:front_end/src/fasta/type_inference/type_inferrer.dart:1355)
#17     TypeInferrerImpl.inferMethodInvocation (package:front_end/src/fasta/type_inference/type_inferrer.dart:1690)
#18     MethodInvocationJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:2168)
#19     ShadowTypeInferrer.inferExpression (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:3342)
#20     TypeInferrerImpl.inferMethodInvocation (package:front_end/src/fasta/type_inference/type_inferrer.dart:1671)
#21     MethodInvocationJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:2168)
#22     ShadowTypeInferrer.inferExpression (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:3342)
#23     ExpressionStatementJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:974)
#24     ShadowTypeInferrer.inferStatement (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:3421)
#25     BlockJudgment.infer (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:299)
#26     ShadowTypeInferrer.inferStatement (package:front_end/src/fasta/kernel/kernel_shadow_ast.dart:3421)
#27     TypeInferrerImpl.inferFunctionBody (package:front_end/src/fasta/type_inference/type_inferrer.dart:1280)
#28     BodyBuilder.finishFunction (package:front_end/src/fasta/kernel/body_builder.dart:709)
#29     DietListener.listenerFinishFunction (package:front_end/src/fasta/source/diet_listener.dart:697)
#30     DietListener.parseFunctionBody (package:front_end/src/fasta/source/diet_listener.dart:731)
#31     DietListener.buildFunctionBody (package:front_end/src/fasta/source/diet_listener.dart:575)
#32     DietListener.endMethod (package:front_end/src/fasta/source/diet_listener.dart:532)
#33     Parser.parseMethod (package:front_end/src/fasta/parser/parser.dart:2862)
#34     Parser.parseClassMemberImpl (package:front_end/src/fasta/parser/parser.dart:2738)
#35     Parser.parseClassBody (package:front_end/src/fasta/parser/parser.dart:2550)
#36     Parser.parseClass (package:front_end/src/fasta/parser/parser.dart:1688)
#37     Parser.parseClassOrNamedMixinApplication (package:front_end/src/fasta/parser/parser.dart:1648)
#38     Parser.parseTopLevelKeywordDeclaration (package:front_end/src/fasta/parser/parser.dart:545)
#39     Parser.parseTopLevelDeclarationImpl (package:front_end/src/fasta/parser/parser.dart:448)
#40     Parser.parseUnit (package:front_end/src/fasta/parser/parser.dart:328)
#41     SourceLoader.buildBody (package:front_end/src/fasta/source/source_loader.dart:207)
<asynchronous suspension>
#42     Loader.buildBodies (package:front_end/src/fasta/loader.dart:164)
<asynchronous suspension>
#43     KernelTarget.buildComponent.<anonymous closure> (package:front_end/src/fasta/kernel/kernel_target.dart:289)
<asynchronous suspension>
#44     withCrashReporting (package:front_end/src/fasta/deprecated_problems.dart:69)
<asynchronous suspension>
#45     KernelTarget.buildComponent (package:front_end/src/fasta/kernel/kernel_target.dart:286)
<asynchronous suspension>
#46     generateKernelInternal.<anonymous closure> (package:front_end/src/kernel_generator_impl.dart:150)
<asynchronous suspension>
#47     withCrashReporting (package:front_end/src/fasta/deprecated_problems.dart:69)
<asynchronous suspension>
#48     generateKernelInternal (package:front_end/src/kernel_generator_impl.dart:57)
<asynchronous suspension>
#49     generateKernel.<anonymous closure> (package:front_end/src/kernel_generator_impl.dart:42)
<asynchronous suspension>
#50     CompilerContext.runWithOptions.<anonymous closure> (package:front_end/src/fasta/compiler_context.dart:131)
<asynchronous suspension>
#51     CompilerContext.runInContext.<anonymous closure>.<anonymous closure> (package:front_end/src/fasta/compiler_context.dart:120)
#52     new Future.sync (dart:async/future.dart:224)
#53     CompilerContext.runInContext.<anonymous closure> (package:front_end/src/fasta/compiler_context.dart:120)
#54     _rootRun (dart:async/zone.dart:1124)
#55     _CustomZone.run (dart:async/zone.dart:1021)
#56     _runZoned (dart:async/zone.dart:1516)
#57     runZoned (dart:async/zone.dart:1463)
#58     CompilerContext.runInContext (package:front_end/src/fasta/compiler_context.dart:119)
#59     CompilerContext.runWithOptions (package:front_end/src/fasta/compiler_context.dart:129)
#60     generateKernel (package:front_end/src/kernel_generator_impl.dart:41)
<asynchronous suspension>
#61     kernelForComponent (package:front_end/src/api_prototype/kernel_generator.dart:83)
<asynchronous suspension>
#62     SingleShotCompilerWrapper.compileInternal (file:///b/build/slave/Linux_Engine/build/src/third_party/dart/pkg/vm/bin/kernel_service.dart:186)
<asynchronous suspension>
#63     Compiler.compile.<anonymous closure> (file:///b/build/slave/Linux_Engine/build/src/third_party/dart/pkg/vm/bin/kernel_service.dart:134)
#64     new Future.<anonymous closure> (dart:async/future.dart:176)
#65     _rootRun (dart:async/zone.dart:1120)
#66     _CustomZone.run (dart:async/zone.dart:1021)
#67     _CustomZone.runGuarded (dart:async/zone.dart:923)
#68     _CustomZone.bindCallbackGuarded.<anonymous closure> (dart:async/zone.dart:963)
#69     _rootRun (dart:async/zone.dart:1124)
#70     _CustomZone.run (dart:async/zone.dart:1021)
#71     _CustomZone.bindCallback.<anonymous closure> (dart:async/zone.dart:947)
#72     Timer._createTimer.<anonymous closure> (dart:async-patch/dart:async/timer_patch.dart:21)
#73     _Timer._runTimers (dart:isolate-patch/dart:isolate/timer_impl.dart:382)
#74     _Timer._handleMessage (dart:isolate-patch/dart:isolate/timer_impl.dart:416)
#75     _RawReceivePortImpl._handleMessage (dart:isolate-patch/dart:isolate/isolate_patch.dart:165)


#0      DietListener.parseFunctionBody (package:front_end/src/fasta/source/diet_listener.dart:738)
#1      DietListener.buildFunctionBody (package:front_end/src/fasta/source/diet_listener.dart:575)
#2      DietListener.endMethod (package:front_end/src/fasta/source/diet_listener.dart:532)
#3      Parser.parseMethod (package:front_end/src/fasta/parser/parser.dart:2862)
#4      Parser.parseClassMemberImpl (package:front_end/src/fasta/parser/parser.dart:2738)
#5      Parser.parseClassBody (package:front_end/src/fasta/parser/parser.dart:2550)
#6      Parser.parseClass (package:front_end/src/fasta/parser/parser.dart:1688)
#7      Parser.parseClassOrNamedMixinApplication (package:front_end/src/fasta/parser/parser.dart:1648)
#8      Parser.parseTopLevelKeywordDeclaration (package:front_end/src/fasta/parser/parser.dart:545)
#9      Parser.parseTopLevelDeclarationImpl (package:front_end/src/fasta/parser/parser.dart:448)
#10     Parser.parseUnit (package:front_end/src/fasta/parser/parser.dart:328)
#11     SourceLoader.buildBody (package:front_end/src/fasta/source/source_loader.dart:207)
<asynchronous suspension>
#12     Loader.buildBodies (package:front_end/src/fasta/loader.dart:164)
<asynchronous suspension>
#13     KernelTarget.buildComponent.<anonymous closure> (package:front_end/src/fasta/kernel/kernel_target.dart:289)
<asynchronous suspension>
#14     withCrashReporting (package:front_end/src/fasta/deprecated_problems.dart:69)
<asynchronous suspension>
#15     KernelTarget.buildComponent (package:front_end/src/fasta/kernel/kernel_target.dart:286)
<asynchronous suspension>
#16     generateKernelInternal.<anonymous closure> (package:front_end/src/kernel_generator_impl.dart:150)
<asynchronous suspension>
#17     withCrashReporting (package:front_end/src/fasta/deprecated_problems.dart:69)
<asynchronous suspension>
#18     generateKernelInternal (package:front_end/src/kernel_generator_impl.dart:57)
<asynchronous suspension>
#19     generateKernel.<anonymous closure> (package:front_end/src/kernel_generator_impl.dart:42)
<asynchronous suspension>
#20     CompilerContext.runWithOptions.<anonymous closure> (package:front_end/src/fasta/compiler_context.dart:131)
<asynchronous suspension>
#21     CompilerContext.runInContext.<anonymous closure>.<anonymous closure> (package:front_end/src/fasta/compiler_context.dart:120)
#22     new Future.sync (dart:async/future.dart:224)
#23     CompilerContext.runInContext.<anonymous closure> (package:front_end/src/fasta/compiler_context.dart:120)
#24     _rootRun (dart:async/zone.dart:1124)
#25     _CustomZone.run (dart:async/zone.dart:1021)
#26     _runZoned (dart:async/zone.dart:1516)
#27     runZoned (dart:async/zone.dart:1463)
#28     CompilerContext.runInContext (package:front_end/src/fasta/compiler_context.dart:119)
#29     CompilerContext.runWithOptions (package:front_end/src/fasta/compiler_context.dart:129)
#30     generateKernel (package:front_end/src/kernel_generator_impl.dart:41)
<asynchronous suspension>
#31     kernelForComponent (package:front_end/src/api_prototype/kernel_generator.dart:83)
<asynchronous suspension>
#32     SingleShotCompilerWrapper.compileInternal (file:///b/build/slave/Linux_Engine/build/src/third_party/dart/pkg/vm/bin/kernel_service.dart:186)
<asynchronous suspension>
#33     Compiler.compile.<anonymous closure> (file:///b/build/slave/Linux_Engine/build/src/third_party/dart/pkg/vm/bin/kernel_service.dart:134)
#34     new Future.<anonymous closure> (dart:async/future.dart:176)
#35     _rootRun (dart:async/zone.dart:1120)
#36     _CustomZone.run (dart:async/zone.dart:1021)
#37     _CustomZone.runGuarded (dart:async/zone.dart:923)
#38     _CustomZone.bindCallbackGuarded.<anonymous closure> (dart:async/zone.dart:963)
#39     _rootRun (dart:async/zone.dart:1124)
#40     _CustomZone.run (dart:async/zone.dart:1021)
#41     _CustomZone.bindCallback.<anonymous closure> (dart:async/zone.dart:947)
#42     Timer._createTimer.<anonymous closure> (dart:async-patch/dart:async/timer_patch.dart:21)
#43     _Timer._runTimers (dart:isolate-patch/dart:isolate/timer_impl.dart:382)
#44     _Timer._handleMessage (dart:isolate-patch/dart:isolate/timer_impl.dart:416)
#45     _RawReceivePortImpl._handleMessage (dart:isolate-patch/dart:isolate/isolate_patch.dart:165)
```

Running `$FLUTTER_ROOT/bin/cache/dart-sdk/bin/dart --packages=../packages/flutter_tools/.packages ../packages/flutter_tools/bin/flutter_tools.dart --help` also produces similar crashes.

This issue is blocking the Dart SDK roll into Flutter, so please make this a priority.

cc @a-siva
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `8c8a211c6e69f13271bc1ac0fa4f80d800be208f` and the full history behind it is present.
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
