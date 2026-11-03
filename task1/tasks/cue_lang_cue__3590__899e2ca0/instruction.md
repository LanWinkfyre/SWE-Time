# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
evaluator: conflicting values in for loop with let expressions

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version
cue version v0.11.0

go version go1.23.3
      -buildmode exe
       -compiler gc
       -trimpath true
     CGO_ENABLED 0
          GOARCH amd64
            GOOS linux
         GOAMD64 v1
cue.lang.version v0.11.0
</pre>


### Does this issue reproduce with the latest stable release?

Yes (0.11.0). 0.10.1 runs as expected

### What did you do?

```
exec cue eval -c conflicting.cue
cmp stdout stdout.golden

-- conflicting.cue --
#Result: [_]: {[string]: string}

result: #Result

#Input: {
	p: "A" | "B"
}

_input: [Parm=_]: #Input & {
	p: Parm
}

_input: {
	A: {}
	B: {}
}

for _, v in _input {
	let Var1 = v.p
	let Var2 = Var1

	let Items = {
		"item": Var2
	}

	result: "conflicting-\(v.p)": Items
}
-- stdout.golden --
result: {
    "conflicting-A": {
        item: "A"
    }
    "conflicting-B": {
        item: "B"
    }
}
```

### What did you expect to see?

Passing test

### What did you see instead?

```
[stderr]
result."conflicting-A".item: conflicting values "B" and "A":
    ./conflicting.cue:10:5
    ./conflicting.cue:18:1
    ./conflicting.cue:19:13
    ./conflicting.cue:20:13
    ./conflicting.cue:23:11
    ./conflicting.cue:26:33
[exit status 1]
```
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `407cccd9c390d7830e275e5efb60e9e7fe725e2a` and the full history behind it is present.
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
