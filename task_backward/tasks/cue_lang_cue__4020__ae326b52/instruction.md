# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
eval: "cycle with field" regression



<!--
Please answer these questions before submitting your issue. Thanks!
For questions please use one of our forums: https://cuelang.slack.com/
-->

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version


go version go1.24.2
      -buildmode exe
       -compiler gc
  DefaultGODEBUG gotestjsonbuildtext=1,multipathtcp=0,randseednop=0,rsa1024min=0,tlsmlkem=0,x509rsacrt=0,x509usepolicies=0
     CGO_ENABLED 1
          GOARCH arm64
            GOOS linux
         GOARM64 v8.0
             vcs git

        vcs.time 2025-08-06T19:28:08Z
    vcs.modified false
cue.lang.version v0.15.0
</pre>

<!--
If you built from source, specify what git tag or commit was used.
-->

### Does this issue reproduce with the latest release?

Yes

### What did you do?

```
env CUE_EXPERIMENT=evalv3=1
exec cue export x.cue

-- x.cue --
package github

deploymentEnv: {
	envScript: [
		for v in _env let v = _env["RECAPTCHA_SITE_KEY"] {"\(v)"},
	]

	_env: {
		RECAPTCHA_SITE_KEY: *"" | _
	}
}
```



### What did you expect to see?

Passing test

### What did you see instead?

```
> env CUE_EXPERIMENT=evalv3=1
> exec cue export x.cue
[stderr]
deploymentEnv.envScript.0: invalid interpolation: cycle with field: v:
    ./x.cue:5:53
    ./x.cue:5:56
[exit status 1]
FAIL: repro.txtar:2: unexpected command failure
```

Note that removing the interpolation the problem goes away:

```diff
--- before      2025-08-06 21:16:57.630735929 +0100
+++ after       2025-08-06 21:17:06.362748712 +0100
@@ -6,7 +6,7 @@

 deploymentEnv: {
        envScript: [
-               for v in _env let v = _env["RECAPTCHA_SITE_KEY"] {"\(v)"},
+               for v in _env let v = _env["RECAPTCHA_SITE_KEY"] {v},
        ]

        _env: {
```
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `8bcd577f27b2f86bcb7143717520924c6c96ffe1` and the full history behind it is present.
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
