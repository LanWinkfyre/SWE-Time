# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Unable to inject values via the scripting layer when using `v0.6.0-rc.1`

### What version of CUE are you using (`cue version`)?



### Does this issue reproduce with the latest stable release?

No, confirmed working with the most stable release:

```console
$ cue version
cue version v0.5.0

go version go1.20.3
      -buildmode exe
       -compiler gc
       -trimpath true
     CGO_ENABLED 1
          GOARCH arm64
            GOOS darwin
```

### What did you do?

Given a simple tool that echoes an injected value:

```
-- echo_tool.cue --
package main

import (
	"tool/cli"
)

command: echo: cli.Print & {
	var: {
		msg: string | *"" @tag(msg,type=string)
	}

	text: var.msg
}
```

### What did you expect to see?

```console
$ cue -t msg="hello, world" echo .
hello, world
```

```console
$ cue --inject msg="hello, world" echo .
hello, world
```

### What did you see instead?

```console
$ cue -t msg="hello, world" echo .
unknown shorthand flag: 't' in -t
```

```console
$ cue --inject msg="hello, world" echo .
unknown flag: --inject
```
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `43b4674898df7e2e8758ccb6154041a98e321e40` and the full history behind it is present.
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
