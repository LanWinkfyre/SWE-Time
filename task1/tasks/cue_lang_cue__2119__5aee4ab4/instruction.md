# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
encoding/yaml.Marshal: assertion failed: no BaseValue: state: finalized; requested: partial

<!--
Please answer these questions before submitting your issue. Thanks!
For questions please use one of our forums: https://cuelang.slack.com/
-->

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version


       -compiler gc
     CGO_ENABLED 1
          GOARCH arm64
            GOOS darwin
</pre>

<!--
If you built from source, specify what git tag or commit was used.
-->

### Does this issue reproduce with the latest release?

I initially produced it on the v0.5.0-beta.1 and then reproduced it with the latest commit.
I can reproduce it on the v0.5.0-alpha.1.
I cannot reproduce it on the last stable release v0.4.3

### What did you do?

<!--
If possible, provide a recipe for reproducing the error.

For advice on how to create a good reproducer, please see:

https://github.com/cue-lang/cue/wiki/Creating-test-or-performance-reproducers
-->

```
cue export - <<EOF
import (
        "encoding/yaml"
        "regexp"
)

#testableRegexp: R={
        string

        #test: close({
                in:  string
                out: regexp.FindSubmatch("^"+R+"$", in)[1]
        })
}

rule: {
        #patterns: {
                bar: #testableRegexp & {
                        "(.*)"
                        #test: {in: "testcontent", out: "testcontent"}
                }
        }
}
out: yaml.Marshal(rule)
EOF
```


### What did you expect to see?

```
{
    "rule": {},
    "out": "{}\n"
}
```



### What did you see instead?

```
out: error in call to encoding/yaml.Marshal: assertion failed: no BaseValue: state: finalized; requested: partial:
    -:23:6
```

### Notes

If I merely replace `yaml.Marshal` with `json.Marshal`, it works fine.

Thanks @mxey.  Marking as v0.5.0. 

### What did you do?

```
exec cue export x.cue
cmp stdout stdout.golden

-- x.cue --
import (
	"encoding/yaml"
	"regexp"
)

#testableRegexp: R={
	string

	#test: close({
		in:  string
		out: regexp.FindSubmatch("^"+R+"$", in)[1]
	})
}

rule: {
	#patterns: {
		bar: #testableRegexp & {
			"(.*)"
			#test: {in: "testcontent", out: "testcontent"}
		}
	}
}
out: yaml.Marshal(rule)
-- stdout.golden --
{
    "rule": {},
    "out": "{}\n"
}
```

### What did you expect to see?

Passing test. Passes with v0.4.3

### What did you see instead?

```
> go run cuelang.org/go/cmd/cue export x.cue
[stderr]
out: error in call to encoding/yaml.Marshal: assertion failed: no BaseValue: state: finalized; requested: partial:
    ./x.cue:23:6
exit status 1

[exit status 1]
FAIL: /tmp/testscript1999356098/repro.txtar/script.txtar:2: unexpected go command failure
```
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `32bfffd0aa538d63757efeef393bc37a06c8c9a4` and the full history behind it is present.
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
