# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cmd/cue: fmt should always "write" to stdout from stdin (unless there is a parsing error)


<!--
Please answer these questions before submitting your issue. Thanks!
For questions please use one of our forums: https://cuelang.slack.com/
-->

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version
cue version v0.9.0-alpha.3

go version go1.22.1
      -buildmode exe
       -compiler gc
  DefaultGODEBUG httplaxcontentlength=1,httpmuxgo121=1,tls10server=1,tlsrsakex=1,tlsunsafeekm=1
     CGO_ENABLED 1
          GOARCH arm64
            GOOS linux
             vcs git

        vcs.time 2024-04-27T10:33:13Z
    vcs.modified false
</pre>

<!--
If you built from source, specify what git tag or commit was used.
-->

### Does this issue reproduce with the latest release?

Yes

### What did you do?

```
env CUE_EXPERIMENT=

stdin x.go
exec gofmt
cmp stdout x.go

stdin x.cue
exec cue fmt -
cmp stdout x.cue

-- x.cue --
x: 5
-- x.go --
package main

func main() {}
```

### What did you expect to see?

Passing test.

### What did you see instead?

```
> env CUE_EXPERIMENT=
> stdin x.go
> exec gofmt
[stdout]
package main

func main() {}
> cmp stdout x.go
> stdin x.cue
> exec cue fmt -
> cmp stdout x.cue
--- stdout
+++ x.cue
@@ -0,0 +1,1 @@
+x: 5

FAIL: /tmp/testscript530863167/repro.txtar/script.txtar:9: stdout and x.cue differ
error running repro.txtar in /tmp/testscript530863167/repro.txtar
```



cc @NoamTD @mvdan
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `ebcf2f5b054eafd05259e79bc7dd026c2d9b76bf` and the full history behind it is present.
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
