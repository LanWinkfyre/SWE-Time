# Locate the commit that introduced this regression

A regression was reported against `openssl/openssl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
SSL_read returns SSL_ERROR_WANT_READ forever on a closed socket

My application uses SSL on nonblocking sockets on FreeBSD.  After the remote side closes its socket, `poll()` returns 1 to indicate that the socket is readable.  Then `read()` returns 0 to indicate EOF.  From the command line, `netstat` reports that the socket is in the `CLOSE_WAIT`  condition, indicating that the other side has closed it.  But at the SSL level, `SSL_read` returns -1, indicating an error.  Then `SSL_get_error` returns `SSL_ERROR_WANT_READ`, indicating that there isn't any application level data available, and the application should poll the socket and try again.  But the exact same thing happens when we try again.  This loop repeats forever.

Versions Affected
==============

| FreeBSD version | OpenSSL version  | OpenSSL source | Result |
| --------------- | ---------------- | -------------- | ------ |
| 15.0            | 3.5.4            | FreeBSD        | Buggy  |
| 15.0            | 3.3.6            | ports          | Buggy  |
| 15.0            | 3.2.5            | ports          | Buggy  |
| 15.0            | 3.2.0            | ports          | Buggy  |


| 15.0            | 3.1.8            | ports          | Good   |
| 15.0            | 3.1.4            | ports          | Good   |
| 14.3            | 3.0.16           | FreeBSD        | Good   |

Root Cause
=========








Steps to Reproduce
================

Unfortunately, I only know how to reproduce this problem using my own proprietary application.

See Also
=======

At least two other users have reported the same problem:
* https://github.com/openssl/openssl/discussions/21924
* https://github.com/openssl/openssl/discussions/25323
```

## What you have

- `/testbed/repo` is a git clone of `openssl/openssl` truncated just after the regression was
  reported.  `HEAD` is `d3951537462175218d1e8a553e93fffb7cc1facb` and the full history behind it is present.
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
