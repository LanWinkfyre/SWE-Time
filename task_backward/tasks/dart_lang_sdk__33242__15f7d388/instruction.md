# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Partial stacktrace:

```
00:16 +117: /home/travis/build/flutter/flutter sdk/packages/flutter/test/cupertino/scrollbar_paint_test.dart: - Paints iOS spec
The following TestFailure object was thrown running a test:
  Expected: Object or closure painting: 'a rounded rectangle with Color(0x99777777),
  RRect.fromLTRBR(795.0, 4.0, 797.5, 86.0, 1.3)'
  Actual: ?:<exactly one widget with type "CupertinoScrollbar" (ignoring offstage widgets):
  CupertinoScrollbar(state: _CupertinoScrollbarState#d8c59(tickers: tracking 1 ticker))>
   Which: threw the following exception:
          '': error: native function 'Canvas_translate' (3 arguments) cannot be found
          #0      _GlowingOverscrollIndicatorPainter._paintSide (package:flutter/src/widgets/overscroll_indicator.dart:493:16)
          #1      _GlowingOverscrollIndicatorPainter.paint (package:flutter/src/widgets/overscroll_indicator.dart:518:5)
          #2      RenderCustomPaint._paintWithPainter (package:flutter/src/rendering/custom_paint.dart:520:13)
          #3      RenderCustomPaint.paint (package:flutter/src/rendering/custom_paint.dart:563:7)
          #4      TestRecordingPaintingContext.paintChild (file:///home/travis/build/flutter/flutter%20sdk/packages/flutter/test/rendering/recording_canvas.dart:102:11)
          #5      _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.paint (package:flutter/src/rendering/proxy_box.dart:127:15)
          #6      TestRecordingPaintingContext.paintChild (file:///home/travis/build/flutter/flutter%20sdk/packages/flutter/test/rendering/recording_canvas.dart:102:11)
          #7      _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.paint (package:flutter/src/rendering/proxy_box.dart:127:15)
          #8      TestRecordingPaintingContext.paintChild (file:///home/travis/build/flutter/flutter%20sdk/packages/flutter/test/rendering/recording_canvas.dart:102:11)
          #9      _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.paint (package:flutter/src/rendering/proxy_box.dart:127:15)
          #10     RenderCustomPaint.paint (package:flutter/src/rendering/custom_paint.dart:561:11)
          #11     TestRecordingPaintingContext.paintChild (file:///home/travis/build/flutter/flutter%20sdk/packages/flutter/test/rendering/recording_canvas.dart:102:11)
          #12     _RenderProxyBox&RenderBox&RenderObjectWithChildMixin&RenderProxyBoxMixin.paint (package:flutter/src/rendering/proxy_box.dart:127:15)
          #13     _evaluatePainter (file:///home/travis/build/flutter/flutter%20sdk/packages/flutter/test/rendering/mock_canvas.dart:501:20)
          #14     _TestRecordingCanvasMatcher.matches (file:///home/travis/build/flutter/flutter%20sdk/packages/flutter/test/rendering/mock_canvas.dart:518:12)
          #15     _expect (package:test/src/frontend/expect.dart:155:17)
          #16     expect (package:test/src/frontend/expect.dart:69:3)
```


Travis: https://travis-ci.org/flutter/flutter/jobs/383847021
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `57d256377c7ec99ada943cd2c8e5855557ea2405` and the full history behind it is present.
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
