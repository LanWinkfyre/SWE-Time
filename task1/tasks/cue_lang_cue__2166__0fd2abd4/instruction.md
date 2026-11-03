# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
evaluator: using let in field comprehension causes 'invalid interpolation: conflicting values' error

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version
cue version v0.5.0-beta.2

       -compiler gc
        -ldflags -s -w
     CGO_ENABLED 0
          GOARCH amd64
            GOOS linux
         GOAMD64 v1

</pre>

### Does this issue reproduce with the latest release?

Yes, this applies to 0.5.0 beta2
Both 0.4.3 and 0.5.0 beta1 work as expected

### What did you do?

```
exec cue eval -c t.cue
cmp stdout stdout.golden

-- t.cue --
_i: {
  a: "d"
  b: "e"
}

for _, v in _i {
    let T = v
    "\(T)": "x"
}
-- stdout.golden --
d: "x"
e: "x"
```

### What did you expect to see?

Passing test.

### What did you see instead?
```
T: invalid interpolation: conflicting values "e" and "d":
    ./t.cue:8:5
    ./t.cue:2:6
    ./t.cue:3:6
    ./t.cue:6:1
    ./t.cue:7:13
```
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `959dc46d5ac976bd2fc9b6f4bf0cd596c00fd0c5` and the full history behind it is present.
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
