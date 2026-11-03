# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
SMTP with GMail fails with out of memory error in 7.69.1 (works OK in 7.68.0)

### I did this
```
curl -s -S -4 -v --interface eth0 \
--ssl-reqd \
--url smtp://smtp.gmail.com:587 \
--mail-auth "user@gmail.com" \
--user "user@gmail.com:MyPassword" \
--mail-from "user@gmail.com" \
--mail-rcpt "user@gmail.com" \
--upload-file /jffs/mail.txt
```

### I expected the following
After the early authentication bits, this is a successful session under 7.68.0:
```
(snip)
< 235 2.7.0 Accepted
} [5 bytes data]
> MAIL FROM:<user@gmail.com> AUTH=user@gmail.com SIZE=135
{ [5 bytes data]
< 250 2.1.0 OK i127sm4454764qkc.93 - gsmtp
} [5 bytes data]
> RCPT TO:<user@gmail.com>
{ [5 bytes data]
< 250 2.1.5 OK i127sm4454764qkc.93 - gsmtp
} [5 bytes data]
> DATA
{ [5 bytes data]
< 354  Go ahead i127sm4454764qkc.93 - gsmtp
} [5 bytes data]
* We are completely uploaded and fine
} [5 bytes data]
< 250 2.0.0 OK  1587760481 i127sm4454764qkc.93 - gsmtp
* Connection #0 to host smtp.gmail.com left intact
```

However with 7.69.1, it returns this:

```
(snip)
< 235 2.7.0 Accepted
} [5 bytes data]
> QUIT
{ [5 bytes data]
< 221 2.0.0 closing connection h13sm2593942qti.32 - gsmtp
* Closing connection 0
} [5 bytes data]
* TLSv1.2 (OUT), TLS alert, close notify (256):
} [2 bytes data]
curl: (27) Out of memory
```

1) Instead of jumping into the MAIL FROM portion, it immediately issues QUIT
2) As the process exits, it reports an Out of memory.

mail.txt contains a very short test file with a From, To,Date, and two lines of content.

This might be server-specific, as my own ISP's server seems to work fine with a similar request.

### curl/libcurl version
curl 7.69.1 (arm-unknown-linux-gnu) libcurl/7.69.1 OpenSSL/1.0.2u
Release-Date: 2020-03-11
Protocols: file ftp ftps http https imap imaps pop3 pop3s smb smbs smtp smtps 
Features: HTTPS-proxy IPv6 Largefile NTLM SSL TLS-SRP UnixSockets

### operating system
Asuswrt-Merlin (Linux-based router firmware).

Tested both on an older uclibc+kernel 2.6.36 and on a glibc+kernel 4.1.51 kernel.

OpenSSL 1.0.2u is used for the SSL/TLS backend.
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `ba7b94b1e74745eb8900ca4cccdec47473fc78f3` and the full history behind it is present.
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
