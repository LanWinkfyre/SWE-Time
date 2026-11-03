# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
systemd-networkd not running when expected

### systemd version the issue has been seen with

252

### Used distribution

Fedora 36

### Linux kernel version used

6.0.8-200.fc36.x86_64

### CPU architectures issue was seen on

x86_64

### Component

systemd-networkd

### Expected behaviour you didn't see

At multi-user.target, systemd-networkd should be running.

### Unexpected behaviour you saw

Weirdly, this is platform dependent. Using exactly the same image (nfs root) a laptop boots OK. A desktop on the same network booting the same image consistently fails.

In both cases, systemd-networkd starts properly in initrd, and then deactivates before switch-root. In the laptop case, networkd starts again, almost immediately, after switchroot. In the desktop case, networkd never starts again without intervention. You can manually start it OK (and it stays running).

If left not running, the network connection is eventually lost when the lease expires. In the case of IPv6, after about 10 minutes (I'm not sure why it happens quicker with IPv6 - maybe something to do with route advertisements).

 Running `systemctl list-dependencies multi-user.target` shows systemd-networkd is definitely a dependency.

### Steps to reproduce the problem

_No response_

### Additional program output to the terminal or log subsystem illustrating the issue

I have captured logs,  but they don't show much. I have a drop-in file for systemd-networkd to set SYSTEMD_LOG_LEVEL=debug but that doesn't change the first run (inside initrd) and the run which doesn't happen after switch-root doesn't happen! In short, the logs look fine, except for the absence of systemd-networkd being started after switch-root.

I don't know how this can happen and satisfy the dependency, but there is no timeout or unusual delay. I can only think that somehow systemd thinks networkd is still active when it is not, or perhaps a timing issue where networkd is still shutting down.

I'm running systemd 250.8-1 from Fedora 36 but in an attempt to solve the problem, changed to systemd-networkd, systemd-network-wait-online and systemd-network-generator built from main/HEAD.

I can confirm that it is the version of systemd in initrd which matters, not the version which runs after switch-root. I've managed to complete a git-bisect, building a new initrd at each stage.  The result is


I haven't yet looked into this commit to try understand what is going on.
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `fe5779cf3f939d8e1ed21ab621dddde0b6699874` and the full history behind it is present.
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
