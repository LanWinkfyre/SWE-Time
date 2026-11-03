# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Truncated output in Journald since v244 when producing output in sub-processes

**systemd version the issue has been seen with**
Since 244.1

I was comparing the Ubuntu versions that were built for 20.04 in the past and got:

- 245.4-4ubuntu3 bad
- 245.2-1ubuntu1 bad
- 244.3-1ubuntu1 bad
- 244.1-0ubuntu3 bad
- 243-3ubuntu1 good
- 242-7ubuntu3 good

**Used distribution**
Ubuntu 20.04
But it was now also reported to trigger on recent Fedora.

**Expected behaviour you didn't see**
Output like

> Apr 30 18:56:40 f systemd[1]: Stopping Test Truncate...
> Apr 30 18:56:40 f test.sh[1165]: This will
> Apr 30 18:56:40 f test.sh[1167]: usually fail
> Apr 30 18:56:40 f test.sh[1168]: and be truncate
> Apr 30 18:56:40 f systemd[1]: test.service: Succeeded.
> Apr 30 18:56:40 f systemd[1]: Stopped Test Truncate.
> 

**Unexpected behaviour you saw**

> Apr 30 18:56:40 f systemd[1]: Stopping Test Truncate...
> Apr 30 18:56:40 f test.sh[1165]: T
> Apr 30 18:56:40 f test.sh[1167]: T
> Apr 30 18:56:40 f test.sh[1167]: sually fai
> Apr 30 18:56:40 f test.sh[1165]: s
> Apr 30 18:56:40 f test.sh[1168]: s
> Apr 30 18:56:40 f test.sh[1168]: nd be truncate
> Apr 30 18:56:40 f test.sh[1165]: n
> Apr 30 18:56:40 f systemd[1]: test.service: Succeeded.
> Apr 30 18:56:40 f systemd[1]: Stopped Test Truncate.

**Steps to reproduce the problem**
Use a test service like /etc/systemd/system/test.service:
```
[Unit]
Description=Test Truncate
After=network.target

[Service]
ExecStart=/usr/lib/test.sh long-test-for-start
ExecStop=/usr/lib/test.sh long-test-for-stop
Type=oneshot
RemainAfterExit=yes
StandardOutput=journal+console
TimeoutStopSec=0

[Install]
WantedBy=multi-user.target
```

And a test script like /usr/lib/test.sh:
```
#!/bin/sh
gettext "This will"
echo
gettext "usually fail"
echo
gettext "and be truncated"
echo
```

Note, this is simplified for testing - in real life this affects libvirts helper to shutdown guests on host shutdown - see [LP 1875708](https://bugs.launchpad.net/ubuntu/+source/libvirt/+bug/1875708).

I [reported this to libvirt trying to fix the behavior](https://www.redhat.com/archives/libvir-list/2020-April/msg01474.html) by ensuring the subprograms do NOT emit to stdout directly. This works, but we don't understand why and wondered if it might be a bug in journald instead.

Daniel did some [debugging on this](https://www.redhat.com/archives/libvir-list/2020-April/msg01527.html) and found:

> I strace'd systemd-journald and the data it receives looks fine,
> but the data systemd-journald writes into the journal, however, is
> completely fubar:

```
recvmsg(32, {msg_name=NULL, msg_namelen=0, msg_iov=[{iov_base="Resuming guest core1: ", iov_len=2054}], msg_iovlen=1, msg_control=[{cmsg_len=28, cmsg_level=SOL_SOCKET, cmsg_type=SCM_CREDENTIALS, cmsg_data={pid=70624, uid=0, gid=0}}], msg_controllen=32, msg_flags=MSG_CTRUNC|MSG_CMSG_CLOEXEC}, MSG_DONTWAIT|MSG_CMSG_CLOEXEC) = 22
writev(33, [{iov_base="[ 2741.146550] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70605]: ", iov_len=9}, {iov_base="R", iov_len=1}, {iov_base="\n", iov_len=1}], 5) = 43
writev(33, [{iov_base="[ 2741.163787] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70624]: ", iov_len=9}, {iov_base="R", iov_len=1}, {iov_base="\n", iov_len=1}], 5) = 43
writev(33, [{iov_base="[ 2742.518626] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70624]: ", iov_len=9}, {iov_base="esuming guest core1:", iov_len=20}, {iov_base="\n", iov_len=1}], 5) = 62
writev(33, [{iov_base="[ 2742.531644] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70655]: ", iov_len=9}, {iov_base="esum", iov_len=4}, {iov_base="\n", iov_len=1}], 5) = 46
recvmsg(32, {msg_name=NULL, msg_namelen=0, msg_iov=[{iov_base="Resuming guest core2: ", iov_len=2054}], msg_iovlen=1, msg_control=[{cmsg_len=28, cmsg_level=SOL_SOCKET, cmsg_type=SCM_CREDENTIALS, cmsg_data={pid=70662, uid=0, gid=0}}], msg_controllen=32, msg_flags=MSG_CTRUNC|MSG_CMSG_CLOEXEC}, MSG_DONTWAIT|MSG_CMSG_CLOEXEC) = 22

writev(33, [{iov_base="[ 2742.687436] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70605]: ", iov_len=9}, {iov_base="e", iov_len=1}, {iov_base="\n", iov_len=1}], 5) = 43
writev(33, [{iov_base="[ 2742.690716] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70662]: ", iov_len=9}, {iov_base="e", iov_len=1}, {iov_base="\n", iov_len=1}], 5) = 43
writev(33, [{iov_base="[ 2744.015012] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70662]: ", iov_len=9}, {iov_base="esuming guest core2:", iov_len=20}, {iov_base="\n", iov_len=1}], 5) = 62
writev(33, [{iov_base="[ 2744.019848] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70694]: ", iov_len=9}, {iov_base="esum", iov_len=4}, {iov_base="\n", iov_len=1}], 5) = 46
writev(33, [{iov_base="[ 2744.036819] ", iov_len=15}, {iov_base="libvirt-guests.sh", iov_len=17}, {iov_base="[70605]: ", iov_len=9}, {iov_base="e", iov_len=1}, {iov_base="\n", iov_len=1}], 5) = 43
```

Does that ring any bell of related systemd changes or known issues?
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `9dcd43b14927fe6f9182a252213dbf182d9d8e01` and the full history behind it is present.
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
