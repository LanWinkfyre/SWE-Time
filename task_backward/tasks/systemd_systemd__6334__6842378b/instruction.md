# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
/etc/systemd/system/default.target.wants is no longer checked for unit files

### Submission type

<!-- Delete the inappropriate option below: -->

 - Bug report

<!-- **NOTE:** Do not submit anything other than bug reports or RFEs via the issue tracker! -->

> systemd-233-6.fc26.x86_64

> Fedora 26

### In case of bug report: Expected behaviour you didn't see

> The service should be running, and the same service worked fine in Fedora <= 25.

### In case of bug report: Unexpected behaviour you saw

> The service does not start.  It is marked as "inactive (dead)" with no other explanation.

```
$ cat /usr/lib/systemd/system/guestfs-firstboot.service
[Unit]
Description=libguestfs firstboot service
After=network.target
Before=prefdm.service

[Service]
Type=oneshot
ExecStart=/usr/lib/virt-sysprep/firstboot.sh start
RemainAfterExit=yes
StandardOutput=journal+console
StandardError=inherit

[Install]
WantedBy=default.target
```

The service is enabled, but it just never runs.
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `cd2d4c7f689cc02b5a592e9212b30e46c516b676` and the full history behind it is present.
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
