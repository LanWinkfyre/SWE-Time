# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Bazel MSVC CROSSTOOL is borken on Windows

After the fix of https://github.com/bazelbuild/bazel/issues/2402, a new error surfaced:
```
ERROR: C:/jenkins/workspace/bazel-tests/BAZEL_VERSION/HEAD/PLATFORM_NAME/windows-x86_64/third_party/BUILD:519:1: Couldn't build file third_party/libgtest.a: Linking of rule '//third_party:gtest' failed: msvc_link.bat failed: error executing command 
  cd C:/bazel_ci/temp/_bazel_SYSTEM/LhCiLHCO/execroot/windows-x86_64
  SET PATH=external/local_config_cc/wrapper/bin
    SET TMPDIR=c:\bazel_ci\temp
  external/local_config_cc/wrapper/bin/msvc_link.bat: com.google.devtools.build.lib.shell.BadExitStatusException: Process exited with status 1.
Traceback (most recent call last):
  File "C:\bazel_ci\temp\_bazel_SYSTEM\LhCiLHCO\execroot\windows-x86_64\external\local_config_cc\wrapper\bin\pydir\msvc_link.py", line 132, in <module>
    sys.exit(main(sys.argv[1:]))  # need to skip the first argument
  File "C:\bazel_ci\temp\_bazel_SYSTEM\LhCiLHCO\execroot\windows-x86_64\external\local_config_cc\wrapper\bin\pydir\msvc_link.py", line 128, in main
    return MsvcLinker().Run(argv[1:])
  File "C:\bazel_ci\temp\_bazel_SYSTEM\LhCiLHCO\execroot\windows-x86_64\external\local_config_cc\wrapper\bin\pydir\msvc_link.py", line 80, in Run
    raise msvc_tools.Error('No output file name specified!')
msvc_tools.Error: No output file name specified!
```
Looking at [msvc_link.py](https://github.com/bazelbuild/bazel/blob/master/tools/cpp/wrapper/bin/pydir/msvc_link.py#L77), we can tell it's because no `/OUT:<filename>` is specified.



//cc @mhlopko @laszlocsomor
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `4e267c86afc8ce0a6c33c0cb851f519ccd20b650` and the full history behind it is present.
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
