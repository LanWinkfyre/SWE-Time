# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
validateFramebufferWithRenderPipelineState fails with MTLPixelFormatInvalid on iOS

On master channel, running https://github.com/flutter/samples/tree/master/add_to_app/multiple_flutters on iOS throws the below error:

```
2021-03-05 10:32:49.828511-0800 MultipleFluttersIos[939:475166] -[MTLDebugRenderCommandEncoder validateFramebufferWithRenderPipelineState:], line 1288: error 'Framebuffer With Render Pipeline State Validation
For stencil attachment, the render pipeline's pixelFormat (MTLPixelFormatInvalid) does not match the framebuffer's pixelFormat (MTLPixelFormatStencil8).
'
-[MTLDebugRenderCommandEncoder validateFramebufferWithRenderPipelineState:]:1288: failed assertion `Framebuffer With Render Pipeline State Validation
For stencil attachment, the render pipeline's pixelFormat (MTLPixelFormatInvalid) does not match the framebuffer's pixelFormat (MTLPixelFormatStencil8).
```
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `565e48777ab207c1cce241f704f14b20b4e258f3` and the full history behind it is present.
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
