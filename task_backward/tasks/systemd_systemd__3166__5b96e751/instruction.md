# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Service doesn't enter the "failed" state

How to reproduce:

```
# cat <<'EOF' >/etc/systemd/system/fail-on-restart.service
[Service]
ExecStart=/bin/false
Restart=always
EOF

# systemctl daemon-reload

# systemctl start fail-on-restart

# systemctl status --no-pager -n0 fail-on-restart
● fail-on-restart.service
   Loaded: loaded (/etc/systemd/system/fail-on-restart.service; static; vendor preset: enabled)
   Active: inactive (dead)

# journalctl -u fail-on-restart --no-pager --no-hostname
-- Logs begin at Sun 2016-05-01 17:01:22 UTC, end at Sun 2016-05-01 17:03:36 UTC. --
May 01 17:03:05 systemd[1]: Started fail-on-restart.service.
May 01 17:03:05 systemd[522]: fail-on-restart.service: Executing: /bin/false
May 01 17:03:06 systemd[1]: fail-on-restart.service: Main process exited, code=exited, status=1/FAILURE
May 01 17:03:06 systemd[1]: fail-on-restart.service: Unit entered failed state.
May 01 17:03:06 systemd[1]: fail-on-restart.service: Failed with result 'exit-code'.
May 01 17:03:06 systemd[1]: fail-on-restart.service: Service hold-off time over, scheduling restart.
May 01 17:03:08 systemd[1]: Stopped fail-on-restart.service.
May 01 17:03:08 systemd[1]: Started fail-on-restart.service.
May 01 17:03:08 systemd[537]: fail-on-restart.service: Executing: /bin/false
May 01 17:03:08 systemd[1]: fail-on-restart.service: Main process exited, code=exited, status=1/FAILURE
May 01 17:03:08 systemd[1]: fail-on-restart.service: Unit entered failed state.
May 01 17:03:08 systemd[1]: fail-on-restart.service: Failed with result 'exit-code'.
May 01 17:03:08 systemd[1]: fail-on-restart.service: Service hold-off time over, scheduling restart.
May 01 17:03:08 systemd[1]: Stopped fail-on-restart.service.
May 01 17:03:08 systemd[1]: Started fail-on-restart.service.
May 01 17:03:08 systemd[542]: fail-on-restart.service: Executing: /bin/false
May 01 17:03:09 systemd[1]: fail-on-restart.service: Child 542 belongs to fail-on-restart.service
May 01 17:03:09 systemd[1]: fail-on-restart.service: Main process exited, code=exited, status=1/FAILURE
May 01 17:03:09 systemd[1]: fail-on-restart.service: Changed running -> failed
May 01 17:03:09 systemd[1]: fail-on-restart.service: Unit entered failed state.
May 01 17:03:09 systemd[1]: fail-on-restart.service: Failed with result 'exit-code'.
May 01 17:03:09 systemd[1]: fail-on-restart.service: Changed failed -> auto-restart
May 01 17:03:09 systemd[1]: fail-on-restart.service: cgroup is empty
May 01 17:03:09 systemd[1]: fail-on-restart.service: Service hold-off time over, scheduling restart.
May 01 17:03:09 systemd[1]: fail-on-restart.service: Trying to enqueue job fail-on-restart.service/restart/fail
May 01 17:03:09 systemd[1]: fail-on-restart.service: Installed new job fail-on-restart.service/restart as 339
May 01 17:03:09 systemd[1]: fail-on-restart.service: Enqueued job fail-on-restart.service/restart as 339
May 01 17:03:09 systemd[1]: fail-on-restart.service: Scheduled restart job.
May 01 17:03:09 systemd[1]: fail-on-restart.service: Changed auto-restart -> dead
May 01 17:03:09 systemd[1]: fail-on-restart.service: Job fail-on-restart.service/restart finished, result=done
May 01 17:03:09 systemd[1]: Stopped fail-on-restart.service.
May 01 17:03:09 systemd[1]: fail-on-restart.service: Converting job fail-on-restart.service/restart -> fail-on-restart.service/start
May 01 17:03:09 systemd[1]: fail-on-restart.service: About to execute: /bin/false
May 01 17:03:09 systemd[1]: fail-on-restart.service: Forked /bin/false as 548
May 01 17:03:09 systemd[1]: fail-on-restart.service: Changed dead -> running
May 01 17:03:09 systemd[1]: fail-on-restart.service: Job fail-on-restart.service/start finished, result=done
May 01 17:03:09 systemd[1]: Started fail-on-restart.service.
May 01 17:03:10 systemd[1]: fail-on-restart.service: Child 548 belongs to fail-on-restart.service
May 01 17:03:10 systemd[1]: fail-on-restart.service: Main process exited, code=exited, status=1/FAILURE
May 01 17:03:10 systemd[1]: fail-on-restart.service: Changed running -> failed
May 01 17:03:10 systemd[1]: fail-on-restart.service: Unit entered failed state.
May 01 17:03:10 systemd[1]: fail-on-restart.service: Failed with result 'exit-code'.
May 01 17:03:10 systemd[1]: fail-on-restart.service: Changed failed -> auto-restart
May 01 17:03:10 systemd[1]: fail-on-restart.service: cgroup is empty
May 01 17:03:10 systemd[1]: fail-on-restart.service: Service hold-off time over, scheduling restart.
May 01 17:03:10 systemd[1]: fail-on-restart.service: Trying to enqueue job fail-on-restart.service/restart/fail
May 01 17:03:10 systemd[1]: fail-on-restart.service: Installed new job fail-on-restart.service/restart as 388
May 01 17:03:10 systemd[1]: fail-on-restart.service: Enqueued job fail-on-restart.service/restart as 388
May 01 17:03:10 systemd[1]: fail-on-restart.service: Scheduled restart job.
May 01 17:03:11 systemd[1]: fail-on-restart.service: Changed auto-restart -> dead
May 01 17:03:11 systemd[1]: fail-on-restart.service: Job fail-on-restart.service/restart finished, result=done
May 01 17:03:11 systemd[1]: Stopped fail-on-restart.service.
May 01 17:03:11 systemd[1]: fail-on-restart.service: Converting job fail-on-restart.service/restart -> fail-on-restart.service/start
May 01 17:03:11 systemd[1]: fail-on-restart.service: About to execute: /bin/false
May 01 17:03:11 systemd[1]: fail-on-restart.service: Forked /bin/false as 554
May 01 17:03:11 systemd[1]: fail-on-restart.service: Changed dead -> running
May 01 17:03:11 systemd[1]: fail-on-restart.service: Job fail-on-restart.service/start finished, result=done
May 01 17:03:11 systemd[1]: Started fail-on-restart.service.
May 01 17:03:11 systemd[554]: fail-on-restart.service: Executing: /bin/false
May 01 17:03:11 systemd[1]: fail-on-restart.service: Child 554 belongs to fail-on-restart.service
May 01 17:03:11 systemd[1]: fail-on-restart.service: Main process exited, code=exited, status=1/FAILURE
May 01 17:03:11 systemd[1]: fail-on-restart.service: Changed running -> failed
May 01 17:03:11 systemd[1]: fail-on-restart.service: Unit entered failed state.
May 01 17:03:11 systemd[1]: fail-on-restart.service: Failed with result 'exit-code'.
May 01 17:03:11 systemd[1]: fail-on-restart.service: Changed failed -> auto-restart
May 01 17:03:11 systemd[1]: fail-on-restart.service: cgroup is empty
May 01 17:03:12 systemd[1]: fail-on-restart.service: Service hold-off time over, scheduling restart.
May 01 17:03:12 systemd[1]: fail-on-restart.service: Trying to enqueue job fail-on-restart.service/restart/fail
May 01 17:03:12 systemd[1]: fail-on-restart.service: Installed new job fail-on-restart.service/restart as 437
May 01 17:03:12 systemd[1]: fail-on-restart.service: Enqueued job fail-on-restart.service/restart as 437
May 01 17:03:12 systemd[1]: fail-on-restart.service: Scheduled restart job.
May 01 17:03:12 systemd[1]: fail-on-restart.service: Changed auto-restart -> dead
May 01 17:03:12 systemd[1]: fail-on-restart.service: Job fail-on-restart.service/restart finished, result=done
May 01 17:03:12 systemd[1]: Stopped fail-on-restart.service.
May 01 17:03:12 systemd[1]: fail-on-restart.service: Converting job fail-on-restart.service/restart -> fail-on-restart.service/start
May 01 17:03:12 systemd[1]: fail-on-restart.service: Start request repeated too quickly.
May 01 17:03:12 systemd[1]: fail-on-restart.service: Job fail-on-restart.service/start finished, result=failed
May 01 17:03:12 systemd[1]: Failed to start fail-on-restart.service.
May 01 17:03:12 systemd[1]: fail-on-restart.service: Collecting.
May 01 17:03:27 systemd[1]: fail-on-restart.service: Collecting.
May 01 17:03:27 systemd[1]: fail-on-restart.service: Collecting.
```
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `7178cd76f225a1c48911c68f2ae1855e97ff1397` and the full history behind it is present.
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
