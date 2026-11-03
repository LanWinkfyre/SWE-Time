# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Can't `pub publish` with version of dart-sdk in Flutter master

The current version of flutter `master` contains a version of `pub` that is not able to publish packages. It fails with the following error:

**Invalid argument(s) (sdkPath): Must not be null**

See [this issue](https://github.com/dart-lang/pub/issues/2563) for more details.

This seems to be [breaking CI in the `flutter/plugins` repo](https://github.com/flutter/plugins/pulls) already (see the `publishable` checks on the latest PRs).

## Steps to Reproduce

<!-- Please tell us exactly how to reproduce the problem you are running into. -->

1. Go to flutter master channel
2. Ensure you're using the dart-sdk coming from flutter
3. `pub publish --dry-run` on any package

## Logs

```
$ which pub
/usr/local/google/home/dit/github/flutter/bin/cache/dart-sdk/bin/pub
```

pub error:

```
$ pub publish --dry-run
Publishing extension_google_sign_in_as_googleapis_auth 1.0.0 to https://pub.dartlang.org:
|-- .gitignore
...
|-- pubspec.yaml
'-- test
    '-- extension_google_sign_in_as_googleapis_auth_test.dart
Invalid argument(s) (sdkPath): Must not be null
dart:core                                                      ArgumentError.checkNotNull
package:analyzer/src/dart/analysis/context_builder.dart 49:19  ContextBuilderImpl.createContext
package:pub/src/dart.dart 115:36                               AnalysisContextManager.createContextsForDirectory
package:pub/src/validator/strict_dependencies.dart 27:28       new StrictDependenciesValidator
package:pub/src/validator.dart 135:7                           Validator.runAll
package:pub/src/command/lish.dart 165:21                       LishCommand._validate
package:pub/src/command/lish.dart 141:15                       LishCommand.run
package:args/command_runner.dart 197:27                        CommandRunner.runCommand
package:pub/src/command_runner.dart 193:39                     PubCommandRunner.runCommand.<fn>
dart:async                                                     new Future.sync
package:pub/src/utils.dart 113:12                              captureErrors.wrappedCallback
dart:async                                                     runZoned
package:pub/src/utils.dart 130:5                               captureErrors
package:pub/src/command_runner.dart 193:13                     PubCommandRunner.runCommand
This is an unexpected error. Please run

    pub --trace publish --dry-run

and include the logs in an issue on https://github.com/dart-lang/pub/issues/new

```


doctor:




(Labeling as P0 to prevent this from going to `dev`, which is not exhibiting the issue yet!)

Issue reproducible easily by running `flutter clean && pub publish --dry-run` on some random pkg and observing the pub output.



<details>
<summary><tt>git bisect</tt> log</summary>



</details>



Bisected further (into dart-lang). More details [here](https://github.com/dart-lang/pub/issues/2563#issuecomment-660290245).
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `2a063fc6c06063d1b4686703f094e489baca6cee` and the full history behind it is present.
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
