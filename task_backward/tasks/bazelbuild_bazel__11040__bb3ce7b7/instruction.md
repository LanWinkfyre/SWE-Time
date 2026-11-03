# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Warning: Rule '<every remote repository rule>' indicated that a canonical reproducible form can be obtained by dropping arguments ["generator_name", "generator_function"]



Here are the warnings for [gitiles](https://gerrit.googlesource.com/gitiles) repository:

```
  $ bazel build :gitiles
Starting local Bazel server and connecting to it...
INFO: Invocation ID: 0e7d47af-ed3f-4882-8129-8ead508a664b
DEBUG: Rule 'com_googlesource_gerrit_bazlets' indicated that a canonical reproducible form can be obtained by modifying arguments shallow_since = "1581093008 -0500" and dropping ["generator_name", "generator_function"]
DEBUG: Repository com_googlesource_gerrit_bazlets instantiated at:
  no stack (--record_rule_instantiation_callstack not enabled)
Repository rule git_repository defined at:
  /home/davido/.cache/bazel/_bazel_davido/9fdffb7f2a398de2e1a63eaee2ea7c50/external/bazel_tools/tools/build_defs/repo/git.bzl:195:18: in <toplevel>
DEBUG: Rule 'rules_java' indicated that a canonical reproducible form can be obtained by dropping arguments ["generator_name", "generator_function"]
DEBUG: Repository rules_java instantiated at:
  no stack (--record_rule_instantiation_callstack not enabled)
Repository rule http_archive defined at:
  /home/davido/.cache/bazel/_bazel_davido/9fdffb7f2a398de2e1a63eaee2ea7c50/external/bazel_tools/tools/build_defs/repo/http.bzl:336:16: in <toplevel>
DEBUG: Rule 'rules_cc' indicated that a canonical reproducible form can be obtained by dropping arguments ["generator_name", "generator_function"]
DEBUG: Repository rules_cc instantiated at:
  no stack (--record_rule_instantiation_callstack not enabled)
Repository rule http_archive defined at:
  /home/davido/.cache/bazel/_bazel_davido/9fdffb7f2a398de2e1a63eaee2ea7c50/external/bazel_tools/tools/build_defs/repo/http.bzl:336:16: in <toplevel>
DEBUG: Rule 'remote_java_tools_linux' indicated that a canonical reproducible form can be obtained by dropping arguments ["generator_name", "generator_function"]
DEBUG: Repository remote_java_tools_linux instantiated at:
  no stack (--record_rule_instantiation_callstack not enabled)
Repository rule http_archive defined at:
  /home/davido/.cache/bazel/_bazel_davido/9fdffb7f2a398de2e1a63eaee2ea7c50/external/bazel_tools/tools/build_defs/repo/http.bzl:336:16: in <toplevel>
DEBUG: Rule 'rules_proto' indicated that a canonical reproducible form can be obtained by dropping arguments ["generator_name", "generator_function"]
DEBUG: Repository rules_proto instantiated at:
  no stack (--record_rule_instantiation_callstack not enabled)
Repository rule http_archive defined at:
  /home/davido/.cache/bazel/_bazel_davido/9fdffb7f2a398de2e1a63eaee2ea7c50/external/bazel_tools/tools/build_defs/repo/http.bzl:336:16: in <toplevel>
DEBUG: Rule 'remotejdk11_linux' indicated that a canonical reproducible form can be obtained by dropping arguments ["generator_name", "generator_function"]
DEBUG: Repository remotejdk11_linux instantiated at:
  no stack (--record_rule_instantiation_callstack not enabled)
Repository rule http_archive defined at:
  /home/davido/.cache/bazel/_bazel_davido/9fdffb7f2a398de2e1a63eaee2ea7c50/external/bazel_tools/tools/build_defs/repo/http.bzl:336:16: in <toplevel>
```

Bisecting the problem:




//CC @alandonovan
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `5c1c0d1ed8643c90fba239d1bc642e4ebd044c2c` and the full history behind it is present.
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
