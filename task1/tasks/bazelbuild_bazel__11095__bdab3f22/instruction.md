# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
//src/main/java/com/google/devtools/build/lib:gen_command-line-reference is broken



```
$ bazel build //src/main/java/com/google/devtools/build/lib:gen_command-line-reference --verbose_failures
...

INFO: Analyzed target //src/main/java/com/google/devtools/build/lib:gen_command-line-reference (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
ERROR: /Users/jingwen/bazels/github/src/main/java/com/google/devtools/build/lib/BUILD:756:1: Executing genrule //src/main/java/com/google/devtools/build/lib:gen_command-line-reference failed (Exit 37): bash failed: error executing command

...

  /bin/bash -c 'source external/bazel_tools/tools/genrule/genrule-setup.sh; cat site/command-line-reference-prefix.html > bazel-out/darwin-fastbuild/bin/src/main/java/com/google/devtools/build/lib/command-line-reference.html && TMP=`mktemp -d /tmp/tmp.XXXXXXXXXX` && bazel-out/host/bin/src/main/java/com/google/devtools/build/lib/bazel/BazelServer --jvm_flag=-Dio.bazel.EnableJni=0 --batch --install_base=${TMP} --output_base=${TMP}/output/ --output_user_root=${TMP} help everything-as-html >> bazel-out/darwin-fastbuild/bin/src/main/java/com/google/devtools/build/lib/command-line-reference.html 2>/dev/null && cat site/command-line-reference-suffix.html >> bazel-out/darwin-fastbuild/bin/src/main/java/com/google/devtools/build/lib/command-line-reference.html')
Execution platform: //:default_host_platform

Use --sandbox_debug to see verbose messages from the sandbox bash failed: error executing command
  /bin/bash -c 'source external/bazel_tools/tools/genrule/genrule-setup.sh; cat site/command-line-reference-prefix.html > bazel-out/darwin-fastbuild/bin/src/main/java/com/google/devtools/build/lib/command-line-reference.html && TMP=`mktemp -d /tmp/tmp.XXXXXXXXXX` && bazel-out/host/bin/src/main/java/com/google/devtools/build/lib/bazel/BazelServer --jvm_flag=-Dio.bazel.EnableJni=0 --batch --install_base=${TMP} --output_base=${TMP}/output/ --output_user_root=${TMP} help everything-as-html >> bazel-out/darwin-fastbuild/bin/src/main/java/com/google/devtools/build/lib/command-line-reference.html 2>/dev/null && cat site/command-line-reference-suffix.html >> bazel-out/darwin-fastbuild/bin/src/main/java/com/google/devtools/build/lib/command-line-reference.html')
Execution platform: //:default_host_platform

Use --sandbox_debug to see verbose messages from the sandbox
Target //src/main/java/com/google/devtools/build/lib:gen_command-line-reference failed to build
INFO: Elapsed time: 1.082s, Critical Path: 0.88s
INFO: 0 processes.
FAILED: Build did NOT complete successfully
```

Same error is happening on the Cloud Build job for docs.bazel.build. 

https://pantheon.corp.google.com/cloud-build/builds/90b4bb72-5e19-4379-948e-79267dec30fb?project=bazel-public
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `09924273efc7050a2e342cd89b823a619ca073f8` and the full history behind it is present.
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
