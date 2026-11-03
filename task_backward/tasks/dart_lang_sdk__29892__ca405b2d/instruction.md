# Locate the commit that introduced this regression

A regression was reported against `dart-lang/sdk`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Access to File.readAsBytes result is slower than expected

Can't provide a small repro atm, but here is my observation:

Data access in this code
```dart
// Load data from file
final bytes = new File('data.bin').readAsBytesSync() as Uint8List;
// Do lots of random access with different aligned typed views (Float32, Uint16)
```
is about 2 times slower than here:
```dart
// Load data from file
final bytes = new Uint8List.fromList(new File('data.bin').readAsBytesSync());
// Do lots of random access with different aligned typed views (Float32, Uint16)
```

Same applies to async version of `File.readAsBytes`.



In `Uint8ArrayView.operator[]` we have a polymorphic call to `_TypedList._getUint8` with receivers `_Uint8List` and `_ExternalUint8Array`. To reach good performance we need to polymorphically inline it. Those methods are natives and have no Dart bodies, so their inlining is handled by `FlowGraphInliner::TryInlineRecognizedMethod`. 

However in the polymorphic inliner we only reach recognized method inlining if we have a single cid call target: 

```cpp
bool PolymorphicInliner::TryInliningPoly(const TargetInfo& target_info) {
  if ((!FLAG_precompiled_mode ||
       owner_->inliner_->use_speculative_inlining()) &&
      target_info.IsSingleCid() &&
      TryInlineRecognizedMethod(target_info.cid_start, *target_info.target)) {
    owner_->inlined_ = true;
    return true;
  }
  // ...
```

 

@ErikCorryGoogle - please take a look.
```

## What you have

- `/testbed/repo` is a git clone of `dart-lang/sdk` truncated just after the regression was
  reported.  `HEAD` is `07725f3dfa71cd0bb056dfd275dad98ac3ae065c` and the full history behind it is present.
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
