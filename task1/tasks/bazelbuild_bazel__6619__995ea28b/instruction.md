# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Documentation for certain rules is missing

### Description of the problem / feature request:

Documentation for certain rules (for example `java_toolchain`) is missing on latest docs.build.bazel.

### Feature requests: what underlying problem are you trying to solve with this feature?

Read the docs.

### Bugs: what's the simplest, easiest way to reproduce this bug? Please provide a minimal example if possible.

https://docs.bazel.build/versions/master/be/java.html

<img width="359" alt="screen shot 2018-11-07 at 1 32 02 pm" src="https://user-images.githubusercontent.com/33242106/48106906-91db3e00-e291-11e8-8eaf-d2b19662cbb5.png">

Note the missing `java_toolchain`, compare with:

https://web.archive.org/web/20181021162843/https://docs.bazel.build/versions/master/be/java.html

<img width="438" alt="screen shot 2018-11-07 at 1 32 10 pm" src="https://user-images.githubusercontent.com/33242106/48106927-a6b7d180-e291-11e8-9b61-5b0cbc64e8e4.png">





```
jingwen@jingwen:/tmp
$ curl http://localhost:12345/versions/master/be/overview.html | grep java_runtime
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--100 37307  100 37307    0     0  2602k      0 --:--:-- --:--:-- --:--:-- 2802k
```



```
jingwen@jingwen:/tmp
$ curl http://localhost:12345/versions/master/be/overview.html | grep java_runtime
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--100 37666  100 37666    0     0  2627k      0 --:--:-                <a href="  java.html#java_runtime">
-             java_runtime
--:--:-- --:--:-- 2627k
```
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `91e0bae6143e39f60e9d62e8b61854cbc8d7a4f4` and the full history behind it is present.
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
