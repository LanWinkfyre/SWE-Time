# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Keyboard Freezing on Samsung Galaxy J Max Tab - 32bit device with beta v1.12.13+hotfix.2

@timsneath 

## Steps to Reproduce

<!--

--> 

1. Open the app.
2. Start typing on any text field. 
3. After some inputs, the keyboard freezes, you can still hear the ticking sound but it freezes with the OS at least for few mins.

 The problem is happening with the Samsung Galaxy J Max tab with Android 5.1.1. Just FYI It has 32 Bit ARM-based CPUs.

I tried it with other channels. The build is working fine then. 

<!--
   
-->


## Logs

<!--
      Run your application with `flutter run --verbose` and attach all the
      log output below between the lines with the backticks. If there is an
      exception, please see if the error message includes enough information
      to explain how to solve the issue.
-->

```
```

<!--
     Run `flutter analyze` and attach any output of that command below.
     If there are any analysis errors, try resolving them before filing this issue.
-->

```
```

<!-- Finally, paste the output of running `flutter doctor -v` here. -->
[✓] Flutter (Channel beta, v1.12.13+hotfix.2, on Mac OS X 10.15.1 19B88, locale
    en-GB)
    • Flutter version 1.12.13+hotfix.2 at /Users/pawankumar/flutter

    • Engine revision 6955b06ced
    • Dart version 2.7.0


[✓] Android toolchain - develop for Android devices (Android SDK version 29.0.2)
    • Android SDK at /Users/pawankumar/Library/Android/sdk
    • Android NDK location not configured (optional; useful for native profiling
      support)
    • Platform android-29, build-tools 29.0.2
    • Java binary at: /Applications/Android
      Studio.app/Contents/jre/jdk/Contents/Home/bin/java
    • Java version OpenJDK Runtime Environment (build
      1.8.0_202-release-1483-b49-5587405)
    • All Android licenses accepted.

[✓] Xcode - develop for iOS and macOS (Xcode 11.2.1)
    • Xcode at /Applications/Xcode.app/Contents/Developer
    • Xcode 11.2.1, Build version 11B500
    • CocoaPods version 1.8.4

[✓] Android Studio
    • Android Studio at /Applications/Android Studio 3.6 Preview.app/Contents
    • Flutter plugin version 41.2.3
    • Dart plugin version 192.7761
    • Java version OpenJDK Runtime Environment (build
      1.8.0_212-release-1586-b4-5784211)

[✓] Android Studio (version 3.5)
    • Android Studio at /Applications/Android Studio.app/Contents
    • Flutter plugin version 41.1.2
    • Dart plugin version 191.8593
    • Java version OpenJDK Runtime Environment (build
      1.8.0_202-release-1483-b49-5587405)

[✓] Android Studio
    • Android Studio at /Applications/Android Studio 4.0 Preview.app/Contents
    • Flutter plugin version 41.2.3
    • Dart plugin version 192.7761
    • Java version OpenJDK Runtime Environment (build
      1.8.0_212-release-1586-b4-5784211)

[✓] IntelliJ IDEA Ultimate Edition (version 2019.2.4)
    • IntelliJ at /Applications/IntelliJ IDEA.app
    • Flutter plugin version 41.1.4
    • Dart plugin version 192.7761

[✓] VS Code (version 1.40.2)
    • VS Code at /Applications/Visual Studio Code.app/Contents
    • Flutter extension version 3.6.0

[!] Connected device
    ! No devices available

! Doctor found issues in 1 category.

```
```


Hi, @tvolkert @dnfield I found the commit. Also, thanks for recommending these commands. I didn't know about it.  Also, is there any way of doing this without downloading the SDK and build tools and running the app again and again.
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `649e188562e45338daef56e336620a6f13e73ad5` and the full history behind it is present.
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
