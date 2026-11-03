# Locate the commit that introduced this regression

A regression was reported against `kubernetes/kubernetes`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
daemonset.status.desiredNumberScheduled=0 for some time in v1.26.0-beta.0

### What happened?

I test that daemonset.status.desiredNumberScheduled==daemonset.status.numberReady as part of my test-env start sequence. But in `v1.26.0-beta.0` (and master) daemonset.status.desiredNumberScheduled==0 for a fairly long time.



### What did you expect to happen?

I expect daemonset.status.desiredNumberScheduled to equals the number of nodes where the daemonset can be scheduled right from start.

This is the behaivor prior to v1.26.x.

### How can we reproduce it (as minimally and precisely as possible)?

Monitor daemonset.status.desiredNumberScheduled during start of a daemonset in `v1.26.0-beta.0`

### Anything else we need to know?

I can quite easily adapt my startup check to the described behaivor (I already have), but there may be others that would be taken by suprise.

It works as expected in v1.25.3 (I haven't tested v1.25.4).

### Kubernetes version

```
# kubectl version --short
Flag --short has been deprecated, and will be removed in the future. The --short output will become the default.
Client Version: v1.26.0-beta.0
Kustomize Version: v4.5.7
Server Version: v1.26.0-beta.0
```

### Cloud provider

None


### OS version

<details>

```
Linux 6.0.0 #4 SMP PREEMPT_DYNAMIC Tue Nov 8 15:43:41 CET 2022
```

</details>


### Install tools

None

### Container runtime (CRI) and version (if applicable)

crio version 1.25.0

### Related plugins (CNI, CSI, ...) and versions (if applicable)

N/A





As mentioned, I have no problem adapting my startup so if the new behavior is expected, please close this issue.
```

## What you have

- `/testbed/repo` is a git clone of `kubernetes/kubernetes` truncated just after the regression was
  reported.  `HEAD` is `cf12a74b18b66efc577ec819c78a0c68f6d49225` and the full history behind it is present.
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
