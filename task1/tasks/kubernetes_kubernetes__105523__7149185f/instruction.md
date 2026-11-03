# Locate the commit that introduced this regression

A regression was reported against `kubernetes/kubernetes`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Kubelet is reporting OutOfCpu on previously running workloads after restart

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


#### What happened:

Restart: Always pods went into OutOfCpu error state after kubelet restart.

#### What you expected to happen:

Pods should remain running as node had sufficient capacity for them. Completed, RestartNever pod should not revert from Completed to OutOfCpu.

#### How to reproduce it (as minimally and precisely as possible):

Launch kubelet with:

```bash
# kube-reserved setting allows my 16-core machine to have 8 cores allocatable
LOG_LEVEL=6 KUBELET_FLAGS="--kube-reserved=cpu=8000m" ./hack/local-up-cluster.sh
```

Run the following script against the local cluster:

<details>

```bash
#!/bin/bash

i=1

create_completed() {
  local i=1
  local podname status

  while test $i -le 8
  do
    podname=complete$i
  
    cluster/kubectl.sh create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: $podname
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["echo",  "ok"]
    resources:
      limits:
        cpu: "1"
        memory: "40Mi"
  restartPolicy: Never
EOF
  
    while true
    do
      status=$(cluster/kubectl.sh get pods complete$i -o json | jq '.status.phase')
      echo $status
      test "$status" = '"Succeeded"' && break
      sleep 1
    done
  
    ((i++))
  done
}

create_running() {
  local i=1
  local podname status

  while test $i -le 6
  do
    podname=running$i
  
    cluster/kubectl.sh create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: $podname
spec:
  containers:
  - name: busybox
    image: busybox
    command: ["sleep",  "inf"]
    resources:
      limits:
        cpu: "1"
        memory: "40Mi"
  restartPolicy: Always
EOF
  
    ((i++))
  done
}

create_completed
create_running
```
</details>

Observe pod status:
```
ehashman@fedora:~/src/k8s$ cluster/kubectl.sh get pod
NAME        READY   STATUS      RESTARTS   AGE
complete1   0/1     Completed   0          80s
complete2   0/1     Completed   0          78s
complete3   0/1     Completed   0          75s
complete4   0/1     Completed   0          71s
complete5   0/1     Completed   0          68s
complete6   0/1     Completed   0          66s
complete7   0/1     Completed   0          62s
complete8   0/1     Completed   0          59s
running1    1/1     Running     0          56s
running2    1/1     Running     0          56s
running3    1/1     Running     0          56s
running4    1/1     Running     0          55s
running5    1/1     Running     0          55s
running6    1/1     Running     0          55s
```

Restart the kubelet:

```bash
kill `pidof kubelet`
START_MODE=kubeletonly  KUBELET_FLAGS="--kube-reserved=cpu=8000m" hack/local-up-cluster.sh
```

Observe pods:

```
ehashman@fedora:~/src/k8s$ cluster/kubectl.sh get pod
NAME        READY   STATUS      RESTARTS      AGE
complete1   0/1     Completed   0             2m30s
complete2   0/1     Completed   0             2m28s
complete3   0/1     Completed   0             2m25s
complete4   0/1     Completed   0             2m21s
complete5   0/1     Completed   0             2m18s
complete6   0/1     Completed   0             2m16s
complete7   0/1     Completed   0             2m12s
complete8   0/1     OutOfcpu    0             2m9s
running1    0/1     Error       1             2m6s
running2    0/1     Error       1 (70s ago)   2m6s
running3    0/1     Error       1 (70s ago)   2m6s
running4    0/1     Error       1 (70s ago)   2m5s
running5    1/1     OutOfcpu    1 (70s ago)   2m5s
running6    0/1     Error       1 (70s ago)   2m5s
```

[kubelet.log](https://github.com/kubernetes/kubernetes/files/7296430/kubelet.log)

#### Anything else we need to know?:

xref https://bugzilla.redhat.com/show_bug.cgi?id=2011513

/sig node

#### Environment:

- Cloud provider or hardware configuration: Local machine
- OS (e.g: `cat /etc/os-release`) & Kernel (e.g. `uname -a`):
```
ehashman@fedora:~/src/k8s$ cat /etc/os-release 
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
ehashman@fedora:~/src/k8s$ uname -a
Linux fedora 5.10.0-8-amd64 #1 SMP Debian 5.10.46-4 (2021-08-03) x86_64 GNU/Linux
```
- Install tools: local-up-cluster.sh
- Network plugin and version (if this is a network-related bug): N/A
- Others:
```

## What you have

- `/testbed/repo` is a git clone of `kubernetes/kubernetes` truncated just after the regression was
  reported.  `HEAD` is `a861de6d162f6197971dffbf09ae101545a9c2e7` and the full history behind it is present.
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
