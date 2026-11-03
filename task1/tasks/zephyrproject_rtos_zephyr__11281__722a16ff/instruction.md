# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
uart shell: ring buffer usage bug

I had test http_server example on frdm_k64f/custom SAME70 board, Zephyr board has the default ipv4 config: 192.0.2.1, the host(ubuntu) computer's ip address is 192.0.2.2.

1. After power up, ping Zephyr from Ubuntu successful.
```
➜  ~ ping 192.0.2.1 
PING 192.0.2.1 (192.0.2.1) 56(84) bytes of data.
64 bytes from 192.0.2.1: icmp_seq=1 ttl=64 time=0.282 ms
64 bytes from 192.0.2.1: icmp_seq=2 ttl=64 time=0.209 ms
```

2. Ping Ubuntu from Zephyr, failed.
```
uart:~$ net ping 192.0.2.2
Sent a pinSg to 192.0.2.2
Ping timeout
uart:~$ 
```

(Please notice the **S** in Send a ping**S**g to, I don't know where it comes)

3. Ping Zephyr from Ubuntu again, failed.


Check the first commit which broke net by using 'git bisect', next is the log:



 @nordic-krch  Could you please double check this commit?
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `a8b742362e1986fea7300ab73b774cdaba0d7066` and the full history behind it is present.
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
