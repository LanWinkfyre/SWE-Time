# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
"--tls1.2" flag causes connection to fail in macOS starting with curl 7.54.0

The command `curl --tlsv1.2 https://tlstest.paypal.com/` works in curl 7.53.1 but does not work in curl 7.54.0 or later when built with SecureTransport. Tested on macOS Sierra 10.12.6 (16G29).

* The macOS Sierra 10.12.6 update updates the `curl` version from 7.51.0 to 7.54.0, so this behavior regresses when updating from macOS 10.12.5 to 10.12.6
* Omitting the `--tlsv1.2` flag and calling `curl https://tlstest.paypal.com/` works in all cases
* Flag works when built with OpenSSL rather than SecureTransport

## 7.53.1-DEV (built locally; works)
`curl -V && curl --tlsv1.2 https://tlstest.paypal.com/`:

```
curl 7.53.1-DEV (x86_64-apple-darwin16.7.0) libcurl/7.53.1-DEV SecureTransport zlib/1.2.8
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
Features: Debug TrackMemory IPv6 Largefile NTLM NTLM_WB SSL libz UnixSockets 
PayPal_Connection_OK%
```

## 7.54.0 (included in macOS Sierra 10.12.6; does not work)
`curl -V && curl --tlsv1.2 https://tlstest.paypal.com/`:

```
curl 7.54.0 (x86_64-apple-darwin16.0) libcurl/7.54.0 SecureTransport zlib/1.2.8
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
Features: AsynchDNS IPv6 Largefile GSS-API Kerberos SPNEGO NTLM NTLM_WB SSL libz UnixSockets 
curl: (35) Server aborted the SSL handshake
```

## 7.54.1-DEV (built locally; does not work)
`curl -V && curl --tlsv1.2 https://tlstest.paypal.com/`:

```
curl 7.54.1-DEV (x86_64-apple-darwin16.7.0) libcurl/7.54.1-DEV SecureTransport zlib/1.2.8
Release-Date: [unreleased]
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
Features: Debug TrackMemory IPv6 Largefile NTLM NTLM_WB SSL libz UnixSockets 
curl: (35) unsupported max version passed via CURLOPT_SSLVERSION
```

## 7.54.1 (installed using `brew`; works)
`curl -V && curl --tlsv1.2 https://tlstest.paypal.com/`:

```
curl 7.54.1 (x86_64-apple-darwin16.7.0) libcurl/7.54.1 OpenSSL/1.0.2l zlib/1.2.8
Release-Date: 2017-06-14
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
Features: IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP UnixSockets HTTPS-proxy 
PayPal_Connection_OK% 
```



Here's the result of the bisect:



I also confirmed manually that the commit immediately before this (with the patch applied) does work correctly.
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `02c7a2ccabf3b21f881faacf286b4308c4ace1bc` and the full history behind it is present.
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
