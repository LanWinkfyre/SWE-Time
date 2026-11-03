# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
SSL session reuse does not work with TLS1.2 with OpenSSL since 7.77.0

### I did this

I'm looking at the Client Hello messages in Wireshark when running the following command:

`curl -v -I --tls-max 1.2 --http1.1 "https://example.com/[1-3]" -H "Connection:close"`

### I expected the following

I've expected to see reused Session IDs, but they are not.

### curl/libcurl version



```
curl 7.77.0-DEV (x86_64-pc-linux-gnu) libcurl/7.77.0-DEV OpenSSL/1.1.1k zlib/1.2.11 brotli/1.0.9 zstd/1.4.9 libidn2/2.3.0 libpsl/0.21.0 (+libidn2/2.3.0) nghttp2/1.41.0 OpenLDAP/2.4.57
Release-Date: [unreleased]
Protocols: dict file ftp ftps gopher gophers http https imap imaps ldap ldaps mqtt pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
Features: alt-svc AsynchDNS brotli HSTS HTTP2 HTTPS-proxy IDN IPv6 Largefile libz NTLM NTLM_WB PSL SSL TLS-SRP UnixSockets zstd
```

### operating system

I've checked on Linux x64, but there is a bug report in the `curl-library` mailing list with topic `TLS session ID re-use broken in 7.77.0` that uses the https://curl.se/windows/dl-7.77.0_2/curl-7.77.0_2-win64-mingw.zip version on Windows.
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `92c588f04b2da0e6e96d5b9640e83a8efc4bf281` and the full history behind it is present.
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
