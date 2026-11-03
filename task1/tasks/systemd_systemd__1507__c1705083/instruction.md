# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[227 regression] user systemd instances try to unmount system mounts on boot

https://bugs.debian.org/801361 reported that 227 introduced a regression with the user systemd instances: They now try to unmount system mounts at startup:

```
systemd[1653]: Reached target Default.
systemd[1653]: boot.mount: Mount process exited, code=exited status=1
systemd[1653]: Failed unmounting /boot.
systemd[1653]: run-user-1000.mount: Mount process exited, code=exited status=1
systemd[1653]: Failed unmounting /run/user/1000.
systemd[1653]: dev-dm\x2d2.swap: Unit entered failed state.
systemd[1653]: sys-kernel-debug.mount: Mount process exited, code=exited status=1
systemd[1653]: Failed unmounting /sys/kernel/debug.
[...]
umount[1657]: umount: /boot: umount failed: Operation not permitted
umount[1658]: umount: /run/user/1000: umount failed: Operation not permitted
swapoff[1659]: swapoff: Not superuser.
```

This is mostly cosmetical for non-root logins, but it was reported that for root logins this actually does unmount stuff.

Investigation is ongoing.


  Admittedly I don't understand this at all yet, but I figure this should be very simple to reproduce on a desktop system.
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `3a3f71e5f09073552dd9b0de2058d8894e1bb4f9` and the full history behind it is present.
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
