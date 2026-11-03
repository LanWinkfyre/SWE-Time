# Locate the commit that introduced this regression

A regression was reported against `kubernetes/kubernetes`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`kubectl get pods --sort-by` no longer sorts correctly

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!-->


**What happened**:


**What you expected to happen**:
`kubectl get pods --sort-by=.metadata.creationTimestamp` should sort by creation timestamp.

**How to reproduce it (as minimally and precisely as possible)**:
```
$ for i in {1..5}; do kubectl create deployment foobar-$i --image=nginx; sleep 5; done
deployment.apps/foobar-1 created
deployment.apps/foobar-2 created
deployment.apps/foobar-3 created
deployment.apps/foobar-4 created
deployment.apps/foobar-5 created

$ kubectl get pods --sort-by=.metadata.creationTimestamp
NAME                        READY   STATUS    RESTARTS   AGE
foobar-1-859fd647ff-72jgp   1/1     Running   0          32s
foobar-2-89d4d78b6-4tt5h    1/1     Running   0          27s
foobar-3-8b74c8cb9-w77c9    1/1     Running   0          22s
foobar-4-5c6b995944-dmx5v   1/1     Running   0          17s
foobar-5-7f79d8957f-vghlc   1/1     Running   0          12s

$ kube delete po foobar-3-8b74c8cb9-w77c9
pod "foobar-3-8b74c8cb9-w77c9" deleted

$ kubectl get pods --sort-by=.metadata.creationTimestamp
NAME                        READY   STATUS        RESTARTS   AGE
foobar-1-859fd647ff-72jgp   1/1     Running       0          47s
foobar-2-89d4d78b6-4tt5h    1/1     Running       0          42s
foobar-4-5c6b995944-dmx5v   1/1     Running       0          32s
foobar-3-8b74c8cb9-wmr4h    1/1     Running       0          3s   <-- !!! BUG !!!
foobar-5-7f79d8957f-vghlc   1/1     Running       0          27s

$ brew switch kubectl 1.12.3
Cleaning /usr/local/Cellar/kubernetes-cli/1.13.0
Cleaning /usr/local/Cellar/kubernetes-cli/1.12.3
203 links created for /usr/local/Cellar/kubernetes-cli/1.12.3

$ kubectl get pods --sort-by=.metadata.creationTimestamp
NAME                        READY   STATUS    RESTARTS   AGE
foobar-1-859fd647ff-72jgp   1/1     Running   0          1m
foobar-2-89d4d78b6-4tt5h    1/1     Running   0          1m
foobar-4-5c6b995944-dmx5v   1/1     Running   0          51s
foobar-5-7f79d8957f-vghlc   1/1     Running   0          46s
foobar-3-8b74c8cb9-wmr4h    1/1     Running   0          22s
```

**Anything else we need to know?**:
N/A

**Environment**:
- Kubernetes version (use `kubectl version`):


<!-- DO NOT EDIT BELOW THIS LINE -->
/kind bug



/assign @soltysh
```

## What you have

- `/testbed/repo` is a git clone of `kubernetes/kubernetes` truncated just after the regression was
  reported.  `HEAD` is `a0c2788249ae1582d10089e7a34bb54fc6b3879d` and the full history behind it is present.
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
