# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
hashing struct values to represent equality is not straightforward

<!--
Please answer these questions before submitting your issue. Thanks!
To ask questions, see https://github.com/cue-lang/cue#contact.
-->

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version
cue version v0.13.1

go version go1.24.4
      -buildmode exe
       -compiler gc
       -trimpath true
     CGO_ENABLED 0
          GOARCH arm64
            GOOS darwin
         GOARM64 v8.0
cue.lang.version v0.13.0
</pre>

### Does this issue reproduce with the latest stable release?

v0.13.1 is the latest stable


### What did you do?

We generate our K8s ConfigMap names based on their data. We then refer to the metadata.name field to get the right generated name.

With evalv3, `cue cmd build` generates YAML output where the two fields do not match, despite being a straight reference. Curiously, this only happens in `cue cmd`. `cue export` works fine.

This does not happen with evalv2. The generated name is different with evalv2 from evalv3, but it's identical in all the fields. 

It also seemed to me that having multiple CUE files made a difference here. 

testscript:

```
exec cue version

env CUE_EXPERIMENT=evalv3=0
exec cue export --out=text -e app.objects.ConfigMap.app.metadata.name
stdout app-72a88d09e6
exec cue export --out=text -e app.objects.Deployment.app.spec.template.spec.containers[0].envFrom[0].configMapRef.name
stdout app-72a88d09e6
exec cue cmd build
grep -count=2 app-72a88d09e6 output.yaml

env CUE_EXPERIMENT=evalv3=1
exec cue export --out=text -e app.objects.ConfigMap.app.metadata.name
stdout app-843db6c1f5
exec cue export --out=text -e app.objects.Deployment.app.spec.template.spec.containers[0].envFrom[0].configMapRef.name
stdout app-843db6c1f5
exec cue cmd build
grep -count=2 app-843db6c1f5 output.yaml

-- build_tool.cue --
package foo

import (
	"encoding/yaml"
	"tool/file"
)

command: build: task: {
	build: file.Create & {
		$after:   task.prepare
		filename: "output.yaml"
		contents: yaml.MarshalStream(app.objectList)
	}
}


-- instance_staging.cue --
package foo

app: {

	objects: ConfigMap: app: data: {
		KEY_JWT_ACCESS_SIGN: "foo"
	}

	objects: ConfigMap: app: data: SIGNING_KEY: "foobar"
}
-- kubernetes.cue --
package foo

import (
	"crypto/sha256"
	"strings"
	"encoding/json"
	"encoding/hex"
)

#ConfigMap: {
	apiVersion: "v1"
	kind:       "ConfigMap"

	data: [string]: string
	immutable: *true | false

	metadata: {
		#basename: string
		if immutable {
			let hash = hex.Encode(sha256.Sum256(json.Marshal([data]))[0:5])
			name: "\(#basename)-\(hash)"
		}
		if !immutable {
			name: #basename
		}
	}
}

app: {
	objectList: [
		for kind, objs in objects for name, obj in objs {
			obj
		},
	]

	objects: [KIND=string]: [NAME=string]: {
		kind: KIND
		metadata: {
			name: *NAME | strings.HasPrefix(NAME+"-")
		}
	}

	objects: ConfigMap: [NAME=string]: #ConfigMap & {metadata: #basename: NAME}

	objects: Deployment: app: spec: template: spec: containers: [{
		envFrom: [
			{configMapRef: name: objects.ConfigMap["app"].metadata.name},
		]
	}, ...]
	objects: ConfigMap: app: {
		data: {
			SIGNING_KEY!:         string
			KEY_JWT_ACCESS_SIGN!: string
		}
	}

}
```



### What did you expect to see?

PASS

### What did you see instead?

```
> exec cue version
[stdout]
cue version v0.13.1

go version go1.24.4
      -buildmode exe
       -compiler gc
       -trimpath true
     CGO_ENABLED 0
          GOARCH arm64
            GOOS darwin
         GOARM64 v8.0
cue.lang.version v0.13.0
> env CUE_EXPERIMENT=evalv3=0
> exec cue export --out=text -e app.objects.ConfigMap.app.metadata.name
[stdout]
app-72a88d09e6
> stdout app-72a88d09e6
> exec cue export --out=text -e app.objects.Deployment.app.spec.template.spec.containers[0].envFrom[0].configMapRef.name
[stdout]
app-72a88d09e6
> stdout app-72a88d09e6
> exec cue cmd build
> grep -count=2 app-72a88d09e6 output.yaml
> env CUE_EXPERIMENT=evalv3=1
> exec cue export --out=text -e app.objects.ConfigMap.app.metadata.name
[stdout]
app-843db6c1f5
> stdout app-843db6c1f5
> exec cue export --out=text -e app.objects.Deployment.app.spec.template.spec.containers[0].envFrom[0].configMapRef.name
[stdout]
app-843db6c1f5
> stdout app-843db6c1f5
> exec cue cmd build
> grep -count=2 app-843db6c1f5 output.yaml
[output.yaml]
apiVersion: v1
kind: ConfigMap
data:
  SIGNING_KEY: foobar
  KEY_JWT_ACCESS_SIGN: foo
immutable: true
metadata:
  name: app-72a88d09e6
---
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
        - envFrom:
            - configMapRef:
                name: app-843db6c1f5

FAIL: <stdin>:17: have 1 matches for `app-843db6c1f5`, want 2
failed run
```
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `c92590272bc2b44e8e58b8f7e878281ba19c067b` and the full history behind it is present.
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
