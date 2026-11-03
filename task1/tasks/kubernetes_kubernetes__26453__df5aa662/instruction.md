# Locate the commit that introduced this regression

A regression was reported against `kubernetes/kubernetes`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cluster/kubectl.sh yells about "cluster/gce/util.sh: line 37: gcloud: command not found" for local clusters



sudo NET_PLUGIN=kubenet hack/local-up-cluster.sh -o _output/local/bin/linux/amd64/
cluster/kubectl.sh config set-cluster local --server=http://127.0.0.1:8080 --insecure-skip-tls-verify=true

but now cluster/kubectl.sh errors out with:
cluster/../cluster/../cluster/gce/util.sh: line 37: gcloud: command not found






```

```
```

## What you have

- `/testbed/repo` is a git clone of `kubernetes/kubernetes` truncated just after the regression was
  reported.  `HEAD` is `1cca499e9222e8a44cce7b637ac2ff7031c6f290` and the full history behind it is present.
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
