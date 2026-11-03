# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
curl aborts after half of the connection timeout



### I did this

```
time curl --connect-timeout 10 http://my-server:11223/
```

`my-server` is a special system that drops everything on port 11223. iptables rule on this server: `iptables -A INPUT -p tcp --destination-port 11223 -j DROP`. It has an IPv4 address and an IPv6 address.

**Before the mentioned commit (curl <= 7.69.1):**
```
curl: (28) Connection timed out after 10001 milliseconds

real	0m10.004s
user	0m0.002s
sys	0m0.001s
```
-> that's expected

**After the mentioned commit**:

```
curl: (28) Failed to connect to my-server port 11223: Connection timed out

real	0m5.205s
user	0m0.000s
sys	0m0.003s
```

5.2 seconds = (connection timeout) / 2 + (happy eyeballs timeout)

**Current master:**
```
curl: (28) Failed to connect to my-server port 11223 after 5000 ms: Timeout was reached

real	0m5.002s
user	0m0.000s
sys	0m0.003s
```

### I expected the following

curl aborts after the connection timeout (10 seconds) and not after half of the connection timeout (5 seconds)

### curl/libcurl version

curl 7.87.1-DEV (x86_64-pc-linux-gnu) libcurl/7.87.1-DEV nghttp2/1.51.0
Release-Date: [unreleased]
Protocols: dict file ftp gopher http imap mqtt pop3 rtsp smtp telnet tftp
Features: alt-svc AsynchDNS HTTP2 IPv6 Largefile threadsafe UnixSockets

### operating system

Linux myhost 6.1.10-100.fc36.x86_64 #1 SMP PREEMPT_DYNAMIC Mon Feb  6 19:58:39 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `964ff76863b63516fce94d547adbbbb7d0d5c7b2` and the full history behind it is present.
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
