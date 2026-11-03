# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
### I did this

```
# curl http://google.de -v
* Uses proxy env variable NO_PROXY == 'localhost,.siemens.net,.siemens.com,.siemens.de,.siemens.cloud,.innomotics.net,.innomotics.com'
* timeout on name lookup is not supported
* Host google.de:80 was resolved.
* IPv6: 2a00:1450:4001:809::2003
* IPv4: 172.217.18.99
*   Trying 172.217.18.99:80...
* Connected to google.de () port 80
> GET / HTTP/1.1
> Host: google.de
```
The actual IP address is not displayed anymore.

Bisected it down to:


While it seems to be a visual issue only, I cannot assess whether anything else is affected.

@icing

### I expected the following

Display the actually used IP address at "Connected to ..."

### curl/libcurl version

curl 8.10.0 (ia64-hp-hpux11.31) libcurl/8.10.0 OpenSSL/3.0.15 zlib/1.3.1
Release-Date: 2024-09-11
Protocols: file http https ipfs ipns smtp smtps
Features: GSS-API HSTS HTTPS-proxy IPv6 Kerberos Largefile libz SPNEGO SSL UnixSockets


### operating system

HP-UX deblndw0 B.11.31 U ia64 HP-UX
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `e70c22b6226badf167463029a2e1c3fe44095a64` and the full history behind it is present.
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
