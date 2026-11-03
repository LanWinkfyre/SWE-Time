# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
bazel crash on windows with `java.nio.file.InvalidPathException: Illegal char <*> at index ...`

### Description of the bug:

Bazel crashed as follows:

```
FATAL: bazel crashed due to an internal error. Printing stack trace:
java.nio.file.InvalidPathException: Illegal char <*> at index 43: C:/users/cloud/workspaces/rules_cuda/bazel-*
        at java.base/sun.nio.fs.WindowsPathParser.normalize(Unknown Source)
        at java.base/sun.nio.fs.WindowsPathParser.parse(Unknown Source)
        at java.base/sun.nio.fs.WindowsPathParser.parse(Unknown Source)
        at java.base/sun.nio.fs.WindowsPath.parse(Unknown Source)
        at java.base/sun.nio.fs.WindowsFileSystem.getPath(Unknown Source)
        at java.base/java.nio.file.Path.of(Unknown Source)
        at com.google.devtools.build.lib.skyframe.LocalDiffAwareness$Factory.lambda$maybeCreate$0(LocalDiffAwareness.java:113)
        at java.base/java.util.stream.ReferencePipeline$3$1.accept(Unknown Source)
        at java.base/java.util.Spliterators$ArraySpliterator.forEachRemaining(Unknown Source)
        at java.base/java.util.stream.AbstractPipeline.copyInto(Unknown Source)
        at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(Unknown Source)
        at java.base/java.util.stream.ReduceOps$ReduceOp.evaluateSequential(Unknown Source)
        at java.base/java.util.stream.AbstractPipeline.evaluate(Unknown Source)
        at java.base/java.util.stream.ReferencePipeline.collect(Unknown Source)
        at com.google.devtools.build.lib.skyframe.LocalDiffAwareness$Factory.maybeCreate(LocalDiffAwareness.java:113)
        at com.google.devtools.build.lib.skyframe.DiffAwarenessManager.maybeGetDiffAwarenessState(DiffAwarenessManager.java:169)
        at com.google.devtools.build.lib.skyframe.DiffAwarenessManager.getDiff(DiffAwarenessManager.java:108)
        at com.google.devtools.build.lib.skyframe.SkyframeExecutor.handleDiffs(SkyframeExecutor.java:3138)
        at com.google.devtools.build.lib.skyframe.SequencedSkyframeExecutor.sync(SequencedSkyframeExecutor.java:285)
        at com.google.devtools.build.lib.runtime.CommandEnvironment.syncPackageLoading(CommandEnvironment.java:737)
        at com.google.devtools.build.lib.runtime.BlazeCommandDispatcher.execExclusively(BlazeCommandDispatcher.java:567)
        at com.google.devtools.build.lib.runtime.BlazeCommandDispatcher.exec(BlazeCommandDispatcher.java:244)
        at com.google.devtools.build.lib.server.GrpcServerImpl.executeCommand(GrpcServerImpl.java:550)
        at com.google.devtools.build.lib.server.GrpcServerImpl.lambda$run$1(GrpcServerImpl.java:621)
        at io.grpc.Context$1.run(Context.java:566)
        at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)
        at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)
        at java.base/java.lang.Thread.run(Unknown Source)
```

### Which category does this issue belong to?

Core

### What's the simplest, easiest way to reproduce this bug? Please provide a minimal example if possible.

See https://github.com/bazel-contrib/rules_cuda/actions/runs/7531757668/job/20501002440#step:7:21

To reproduce locally:

[rules_cuda-cloudhan-v7.zip](https://github.com/bazelbuild/bazel/files/13944192/rules_cuda-cloudhan-v7.zip)
```
# to repo root
cd rules_cuda-cloudhan-v7

# out of repo @examples build with --noenable_bzlmod crashes bazel
bazelisk build --noenable_bzlmod @rules_cuda_examples//basic:all

# the following works correctly however...
cd examples
bazelisk build --noenable_bzlmod @rules_cuda_examples//basic:all
```

### Which operating system are you running Bazel on?

Windows 11 and Windows Server 2019

### What is the output of `bazel info release`?

release 7.0.0, `bazel info` (no ` release`) crashed with the same error

### Any other information, logs, or outputs that you want to share?

`bazel info` crashed with the same error



Cc @sushain97
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `cddec1247571f1cda9939ffb7546e089e528c76e` and the full history behind it is present.
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
