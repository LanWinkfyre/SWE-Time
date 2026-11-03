# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
internal/core/export: nil pointer dereference during eval since v0.6.0

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version


go version devel go1.22-ace1494d92 Thu Sep 21 02:36:06 2023 +0000
      -buildmode exe
       -compiler gc
        -ldflags -w -s
  DefaultGODEBUG httplaxcontentlength=1,panicnil=1
     CGO_ENABLED 1
          GOARCH amd64
            GOOS linux
         GOAMD64 v3
</pre>

### Does this issue reproduce with the latest stable release?

Yes, with v0.6.0.

### What did you do?

```
exec cue eval in.cue

-- in.cue --
F1: sub1: sub2: L
F2: {
	(string): _
	L
}
D: {}
let L = D
```

### What did you expect to see?

A testscript PASS; it shouldn't panic, and it should produce some CUE syntax.

### What did you see instead?



This panic does not happen with v0.5.0; I have not bisected yet.

 Here is the result:
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `a44c805cc6f93e9fb32ef6ea81c2b1442c5b39ad` and the full history behind it is present.
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
