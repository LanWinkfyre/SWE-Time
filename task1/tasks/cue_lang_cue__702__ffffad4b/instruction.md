# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cmd/cue: disjunction regression 

_Originally opened by @myitcv in https://github.com/cuelang/cue/issues/702_


<!--
Please answer these questions before submitting your issue. Thanks!
For questions please use one of our forums: https://cuelang.slack.com/
-->

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version

</pre>

<!--
If you built from source, specify what git tag or commit was used.
-->

### Does this issue reproduce with the latest release?

Yes

### What did you do?

```
testscript -v <<'EOD'
exec cue eval 

-- x.cue --
package p

x: {
	name: "Hello"
}

y: *x.ops | x
EOD
```

### What did you expect to see?

```
> exec cue eval
[stdout]
x: {
    name: "Hello"
}
y: {
    name: "Hello"
}
```


### What did you see instead?


```
> exec cue eval
[stdout]
x: {
    name: "Hello"
}
y: _|_ // y: undefined field ops
```
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `06484a39d8d44c656212ac2d3b5589f8aa9db033` and the full history behind it is present.
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
