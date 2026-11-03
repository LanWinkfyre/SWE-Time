# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
evaluator: infinite loop on cycle with embeddings

<!--
Please answer these questions before submitting your issue. Thanks!
To ask questions, see https://github.com/cue-lang/cue#contact.
-->

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version
cue version v0.5.0-rc.1

go version go1.20.2
      -buildmode exe
       -compiler gc
       -trimpath true
     CGO_ENABLED 0
          GOARCH amd64
            GOOS linux
         GOAMD64 v1
</pre>
Also loops on tags `v0.6.0-beta.1` and `v0.6.0-rc.1`, but not `v0.4.3`.




### What did you do?

```
x
x: {
	y
	y: x
}
```


### What did you expect to see?

Something like
`x.y: structural cycle`

### What did you see instead?

Apparently a non terminating evaluation.
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `da3ee7dc7b27de85bbfb0a4104dfb22bcb18ef68` and the full history behind it is present.
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
