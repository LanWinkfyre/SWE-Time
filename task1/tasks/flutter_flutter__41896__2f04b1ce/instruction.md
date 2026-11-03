# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[web] release build fails due to missing generated_plugin_registrant.dart

Debug builds still work.

```
$ flutter build web --release

#0      Dart2JSTarget.build (package:flutter_tools/src/build_system/targets/web.dart:150:7)
<asynchronous suspension>
#1      _BuildInstance._invokeInternal (package:flutter_tools/src/build_system/build_system.dart:527:25)
<asynchronous suspension>
#2      _BuildInstance.invokeTarget.<anonymous closure> (package:flutter_tools/src/build_system/build_system.dart:482:35)
#3      new Future.sync (dart:async/future.dart:224:31)
#4      AsyncMemoizer.runOnce (package:async/src/async_memoizer.dart:43:45)
#5      _BuildInstance.invokeTarget (package:flutter_tools/src/build_system/build_system.dart:482:21)
<asynchronous suspension>
<asynchronous suspension>
#6      BuildSystem.build (package:flutter_tools/src/build_system/build_system.dart:420:36)
#7      _AsyncAwaitCompleter.start (dart:async-patch/async_patch.dart:43:6)
#8      BuildSystem.build (package:flutter_tools/src/build_system/build_system.dart:401:28)
#9      buildWeb (package:flutter_tools/src/web/compile.dart:32:56)
#10     _AsyncAwaitCompleter.start (dart:async-patch/async_patch.dart:43:6)
#11     buildWeb (package:flutter_tools/src/web/compile.dart:24:22)
#12     BuildWebCommand.runCommand (package:flutter_tools/src/commands/build_web.dart:56:11)
#13     _AsyncAwaitCompleter.start (dart:async-patch/async_patch.dart:43:6)
#14     BuildWebCommand.runCommand (package:flutter_tools/src/commands/build_web.dart:46:42)
#15     FlutterCommand.verifyThenRunCommand (package:flutter_tools/src/runner/flutter_command.dart:553:18)
#16     _asyncThenWrapperHelper.<anonymous closure> (dart:async-patch/async_patch.dart:71:64)
#17     _rootRunUnary (dart:async/zone.dart:1132:38)
#18     _CustomZone.runUnary (dart:async/zone.dart:1029:19)
#19     _FutureListener.handleValue (dart:async/future_impl.dart:137:18)
#20     Future._propagateToListeners.handleValueCallback (dart:async/future_impl.dart:678:45)
#21     Future._propagateToListeners (dart:async/future_impl.dart:707:32)
#22     Future._completeWithValue (dart:async/future_impl.dart:522:5)
#23     Future._asyncComplete.<anonymous closure> (dart:async/future_impl.dart:552:7)
#24     _rootRun (dart:async/zone.dart:1124:13)
#25     _CustomZone.run (dart:async/zone.dart:1021:19)
#26     _CustomZone.runGuarded (dart:async/zone.dart:923:7)
#27     _CustomZone.bindCallbackGuarded.<anonymous closure> (dart:async/zone.dart:963:23)
#28     _microtaskLoop (dart:async/schedule_microtask.dart:41:21)
#29     _startMicrotaskLoop (dart:async/schedule_microtask.dart:50:5)
#30     _runPendingImmediateCallback (dart:isolate-patch/isolate_patch.dart:116:13)
#31     _RawReceivePortImpl._handleMessage (dart:isolate-patch/isolate_patch.dart:173:5)


Exception: .dart_tool/flutter_build/61f7a30d1a3dbdc8a1baebbf511a0b79/main.dart:5:8:
Error: Error when reading '.dart_tool/flutter_build/61f7a30d1a3dbdc8a1baebbf511a0b79/generated_plugin_registrant.dart': Error reading
'.dart_tool/flutter_build/61f7a30d1a3dbdc8a1baebbf511a0b79/generated_plugin_registrant.dart'  (No such file or directory)
import 'generated_plugin_registrant.dart';
       ^
.dart_tool/flutter_build/61f7a30d1a3dbdc8a1baebbf511a0b79/main.dart:9:3:
Error: Method not found: 'registerPlugins'.
  registerPlugins(webPluginRegistry);
  ^^^^^^^^^^^^^^^
Error: Compilation failed.


Failed to compile application for the Web.
```

```
Doctor summary (to see all details, run flutter doctor -v):
[✓] Flutter (Channel master, v1.10.8-pre.21, on Mac OS X 10.14.6 18G95, locale en-CH)

[✓] Android toolchain - develop for Android devices (Android SDK version 28.0.3)
[✓] Xcode - develop for iOS and macOS (Xcode 11.0)
[✓] Chrome - develop for the web
[✓] Android Studio (version 3.5)
[✓] VS Code (version 1.31.1)
[✓] Connected device (3 available)

• No issues found!
```
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `fa7340a328cbfbe745748cfcd5d5fe08c401c64c` and the full history behind it is present.
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
