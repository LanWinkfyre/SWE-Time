# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
evalv3: or operator confuses the new evaluator, leading to incomplete evaluation

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version
CUE language version v0.15.3

Go version go1.25.5 X:nodwarf5
      -buildmode exe
       -compiler gc
  DefaultGODEBUG containermaxprocs=0,decoratemappings=0,tlssha1=1,updatemaxprocs=0,x509sha256skid=0
     CGO_ENABLED 1
          GOARCH amd64
    GOEXPERIMENT nodwarf5
            GOOS linux
         GOAMD64 v1

</pre>

### Does this issue reproduce with the latest stable release?

Yes

### What did you do?

Ran the following test script:

```
-- main.cue --
#AWSRegion: or(["eu-west-1", "us-east-1"])

#AWSTFState: {
	accountRegion: #AWSRegion
}

#AWSAccountTree: {
	region:     #AWSRegion
	propertyA?: [...#AWSTFState]
	propertyB?: #AWSTFState
}

tree: [REGION=string]: [ACCOUNT_ID=string]: #AWSAccountTree & {
	region:          #AWSRegion & REGION
}

#fnAWSAccountWithPropertyB: {
	tree: {...}
	out: [
		for region, v in tree
		for account, details in v
		if details.propertyB != _|_ {
			accountRegion: details.propertyB.accountRegion
		},
	]
}

TREE=tree: "eu-west-1": {
	"account-a": #AWSAccountTree & {
		propertyA: (#fnAWSAccountWithPropertyB & {tree: TREE}).out
	}
	"account-b": #AWSAccountTree & {
		propertyB: {
			accountRegion: "eu-west-1"
		}
	}
}
```


### What did you expect to see?

The following output is correct and generated with Cue 0.12 running the old evaluator:

```
{
    "tree": {
        "eu-west-1": {
            "account-a": {
                "region": "eu-west-1",
                "propertyA": [
                    {
                        "accountRegion": "eu-west-1"
                    }
                ]
            },
            "account-b": {
                "region": "eu-west-1",
                "propertyB": {
                    "accountRegion": "eu-west-1"
                }
            }
        }
    }
}

```


### What did you see instead?

When the new evaluator is used (with any Cue version), `account-a.propertyA` is not filled :

```
{
    "tree": {
        "eu-west-1": {
            "account-a": {
                "region": "eu-west-1",
                "propertyA": []
            },
            "account-b": {
                "region": "eu-west-1",
                "propertyB": {
                    "accountRegion": "eu-west-1"
                }
            }
        }
    }
}
```

If instead of defining `#AWSRegion` with the `or` operator, it is defined as a simple disjunction like this:

```
#AWSRegion: "eu-west-1" | "us-east-1"
```

then the new evaluator output is correct, `account-a.propertyA` contains the region.
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `af0cfc15a7ab6e8ef67c10750c986100c12a4b96` and the full history behind it is present.
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
