# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Severe regression of BinaryPrinter.writeComponentFile performance




 
Repro:

* Apply the following change to measure time:
```patch
diff --git a/pkg/kernel/lib/binary/ast_to_binary.dart b/pkg/kernel/lib/binary/ast_to_binary.dart
index eba37ecd6a5..630e8c63c80 100644
--- a/pkg/kernel/lib/binary/ast_to_binary.dart
+++ b/pkg/kernel/lib/binary/ast_to_binary.dart
@@ -581,6 +581,7 @@ class BinaryPrinter implements Visitor<void>, BinarySink {
   }
 
   void writeComponentFile(Component component) {
+    Stopwatch timer = new Stopwatch()..start();
     Timeline.timeSync("BinaryPrinter.writeComponentFile", () {
       compilationMode = component.mode;
       _computeCanonicalNames(component);
@@ -623,6 +624,7 @@ class BinaryPrinter implements Visitor<void>, BinarySink {
 
       _flush();
     });
+    print("writeComponentFile took ${timer.elapsedMilliseconds}ms");
   }
 
   void writeListOfStrings(List<String>? strings) {
```
* Run
```
dart pkg/vm/bin/protobuf_aware_treeshaker.dart --aot --platform vm_platform_strong.dill --remove-source input.dill output.dill
```






fyi @johnniwinther @jensjoha @rakudrama @rmacnak-google
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `204c03a98ed42afe65068e3efe931ff5b890158c` and the full history behind it is present.
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
