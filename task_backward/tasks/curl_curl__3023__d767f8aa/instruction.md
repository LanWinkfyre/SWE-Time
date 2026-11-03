# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
curl 7.60.0 can list & work with openssl engines while curl 7.61.1 can't

In the following, openssl is openssl @1.0.2p_0. The same openssl.cnf is used for both test

### I did this
```
$ sudo port installed curl
The following ports are currently installed:
  curl @7.59.0_0+ssl
  curl @7.60.0_0+ssl (active)
  curl @7.61.0_0+ssl 
$ curl --version
curl 7.60.0 (x86_64-apple-darwin17.5.0) libcurl/7.60.0 OpenSSL/1.0.2p zlib/1.2.11 libidn2/2.0.5 libpsl/0.20.2 (+libidn2/2.0.5)
Release-Date: 2018-05-16
Protocols: dict file ftp ftps gopher http https imap imaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
Features: AsynchDNS IDN IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP UnixSockets HTTPS-proxy PSL 
$ curl --engine list
Build-time engines:
  rdrand
  dynamic
  pkcs11

$ sudo port activate curl @7.61.0_0+ssl
--->  Computing dependencies for curl
--->  Deactivating curl @7.60.0_0+ssl
--->  Cleaning curl
--->  Activating curl @7.61.0_0+ssl
--->  Cleaning curl
$ curl --version
curl 7.61.0 (x86_64-apple-darwin17.6.0) libcurl/7.61.0 OpenSSL/1.0.2p zlib/1.2.11 libidn2/2.0.5 libpsl/0.20.2 (+libidn2/2.0.5)
Release-Date: 2018-07-11
Protocols: dict file ftp ftps gopher http https imap imaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
Features: AsynchDNS IDN IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP UnixSockets HTTPS-proxy PSL
$ curl --engine list
Build-time engines:
  <none>

```
### I expected the following
```
$ curl --version
curl 7.61.0 (x86_64-apple-darwin17.6.0) libcurl/7.61.0 OpenSSL/1.0.2p zlib/1.2.11 libidn2/2.0.5 libpsl/0.20.2 (+libidn2/2.0.5)
Release-Date: 2018-07-11
Protocols: dict file ftp ftps gopher http https imap imaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp 
Features: AsynchDNS IDN IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP UnixSockets HTTPS-proxy PSL
$ curl --engine list
Build-time engines:
  rdrand
  dynamic
  pkcs11

```

### operating system
Mac OS 10.13.6 & MacPorts 2.5.3


You are right, sorry. Mistake was on my side because I did not run buildconf between each bisect.



 SSL engine list is still empty after this commit.
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `ba782baac3009e44295589743bb8ae8220793e74` and the full history behind it is present.
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
