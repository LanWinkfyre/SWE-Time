# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Long delay running pop3 LIST

### I did this

`curl --ssl-reqd --insecure -u username:password pop3s://pop.gmx.net`

### I expected the following

I expect a list of message IDs and message size. The list does indeed shows, but only up to message number 96. Then the display stops in the middle of the line, like here:

```
[previous lines skipped]
90 8157
91 7650
92 7888
93 7779
94 19238
95 19218
9
```

Surprisingly, after at least 30 seconds of inactivity, curl continues. It completes the truncated line and writes all remaining lines with no further delay (up to message 222, in my case).

I have seen the same delay in other pop3 contexts, but I am not able to reproduce it there. I hope you can see my findings.

### curl/libcurl version

curl 8.8.0 (x86_64-w64-mingw32) libcurl/8.8.0 LibreSSL/3.9.2 zlib/1.3.1 brotli/1.1.0 zstd/1.5.6 WinIDN libpsl/0.21.5 libssh2/1.11.0 nghttp2/1.62.1 ngtcp2/1.6.0 nghttp3/1.4.0
Release-Date: 2024-05-22
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS brotli HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM PSL SPNEGO SSL SSPI threadsafe UnixSockets zstd

Note: This is the curl 8.8.0 binary from https://curl.se/windows/dl-8.8.0_3/curl-8.8.0_3-win64-mingw.zip.

### operating system

Windows 11, 64 bit.

I was able to build from GIT with schannel. The patch does not fix the delay.

Some observations:

* The function `data_pending()`, which the patch modifies, is not called before the delay but only much later, and only once, almost at the very end of the operation.

* During the delay,



is called literally thousands of times and always returns 0. Outside the delay, it almost never returns 0.



Maybe this helps.
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `bae555359979016999a9425a2d489f219a78abdd` and the full history behind it is present.
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
