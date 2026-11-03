# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Bazel @HEAD frequently kills the server process

### Description of the bug:


When running Bazel in a loop, it occasionally kills the server for no good reason, on about every second invocation, with the error message `Killed non-responsive server process (pid=<number>)`


### Which category does this issue belong to?


_No response_

### What's the simplest, easiest way to reproduce this bug? Please provide a minimal example if possible.


```
touch WORKSPACE
cat > BUILD <<'EOF'
genrule(
    name = "gg",
    outs = ["go"],
    cmd = "sleep 1; echo O > $@",
)
EOF
for i in $(seq 1 20); do bazel build //:gg; done
```

Looping 20 times is usually enough to reproduce the issue frequently.

### Which operating system are you running Bazel on?


Linux

### What is the output of `bazel info release`?


development version

### If `bazel info release` returns `development version` or `(@non-git)`, tell us how you built Bazel.




This issue doesn't seem to happen with 7.0.0rc4.

### What's the output of `git remote get-url origin; git rev-parse master; git rev-parse HEAD` ?


```text
See the commithash above.
```


### Is this a regression? If yes, please try to identify the Bazel commit where the bug was introduced.


 I haven't done the bisection.

### Have you found anything relevant by searching the web?

_No response_

### Any other information, logs, or outputs that you want to share?

_No response_

 I'm pretty certain: after this change, I got 2/20 restarts, before, 0/50 .
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `08407743e903627d7e64c669f27b3f2b81316e33` and the full history behind it is present.
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
