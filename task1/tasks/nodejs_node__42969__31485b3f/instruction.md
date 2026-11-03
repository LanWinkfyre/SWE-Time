# Locate the commit that introduced this regression

A regression was reported against `nodejs/node`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
building `master` on macOS ARM64 fails

### Version

master

### Platform

_No response_

### Subsystem

_No response_

### What steps will reproduce the bug?

```console
$> git fetch upstream
$> git checkout upstream/master
$> make -j8
```

### How often does it reproduce? Is there a required condition?

_No response_

### What is the expected behavior?

_No response_

### What do you see instead?

```
Undefined symbols for architecture arm64:
  "node::shadow_realm::HostCreateShadowRealmContextCallback(v8::Local<v8::Context>)", referenced from:
      node::SetIsolateMiscHandlers(v8::Isolate*, node::IsolateSettings const&) in libnode.a(libnode.environment.o)
ld: symbol(s) not found for architecture arm64
```

### Additional information





(which makes sense)
```

## What you have

- `/testbed/repo` is a git clone of `nodejs/node` truncated just after the regression was
  reported.  `HEAD` is `a5b87305255f4757545b1d9f60a5e6f94cb742c8` and the full history behind it is present.
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
