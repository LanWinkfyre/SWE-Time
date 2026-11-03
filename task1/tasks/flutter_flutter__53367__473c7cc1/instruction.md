# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Bad state: Future already completed error when displaying any HtmlElementView [web]

Minimal example using HtmlElementView, run using `flutter run -d chrome`

```
// ignore: avoid_web_libraries_in_flutter
import 'dart:html';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';

void main() async {
  runApp(MyHomePage());
}

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return HtmlWidget();
  }
}

class HtmlWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final viewType = 'someViewType';
    // ignore:undefined_prefixed_name
    ui.platformViewRegistry.registerViewFactory(viewType, (int viewId) {
      final div = DivElement();
      return div;
    });

    return HtmlElementView(viewType: viewType);
  }
}
```
Error report in terminal and browser console.

```
══╡ EXCEPTION CAUGHT BY SERVICES LIBRARY ╞══════════════════════════════════════════════════════════
The following StateError was thrown during a platform message response callback:
Bad state: Future already completed

When the exception was thrown, this was the stack:
dart-sdk/lib/_internal/js_dev_runtime/private/ddc_runtime/errors.dart 195:49  throw_
dart-sdk/lib/async/future_impl.dart 42:79                                     complete
packages/flutter/src/services/binding.dart 176:18                             <fn>
lib/_engine/engine/window.dart 259:17                                         <fn>
dart-sdk/lib/async/zone.dart 1402:54                                          runUnary
dart-sdk/lib/async/future_impl.dart 141:18                                    handleValue
dart-sdk/lib/async/future_impl.dart 682:44                                    handleValueCallback
dart-sdk/lib/async/future_impl.dart 711:32                                    _propagateToListeners
dart-sdk/lib/async/future_impl.dart 516:7                                     [_complete]
dart-sdk/lib/async/future.dart 315:15                                         <fn>
dart-sdk/lib/_internal/js_dev_runtime/private/isolate_helper.dart 50:19       internalCallback
════════════════════════════════════════════════════════════════════════════════════════════════════
Another exception was thrown: Bad state: Future already completed
Another exception was thrown: Bad state: Future already completed
```

 



Flutter doctor -v output
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `c9f999278cf3d7e1fb3d36feea36664325834095` and the full history behind it is present.
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
