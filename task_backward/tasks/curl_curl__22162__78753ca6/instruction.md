# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
can't specify empty username/password to ldap server

### I did this

I'm using curl to download CRL for x.509 certificates like follows.

$ curl-8.20.0 -u : 'ldap://ldap.example.com/o=xxx,c=xxx?certificateRevocationList' >CRL.ldif

This method work fine with curl-8.20.0 or prior (except for early curl-8.19.0), but does not curl-8.21.0. 

$ curl-8.21.0 -u : 'ldap://ldap.example.com/o=xxx,c=xxx?certificateRevocationList' >CRL.ldif
curl: (38) LDAP local: bind via ldap_win_bind 資格情報が無効です <-- Invalid credentials

I also tried below, but does not work as well.

$ curl-8.21.0 'ldap://:@ldap.example.com/o=xxx,c=xxx?certificateRevocationList' >CRL.ldif
curl: (38) LDAP local: bind via ldap_win_bind 資格情報が無効です <-- Invalid credentials

### I expected the following

I want to specify empty username/password to ldap server using curl.

### curl/libcurl version

curl 8.21.0 (x86_64-w64-mingw32) libcurl/8.21.0 LibreSSL/4.3.2 zlib/1.3.1.zlib-ng brotli/1.2.0 zstd/1.5.7 WinIDN libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.69.0 ngtcp2/1.23.0 nghttp3/1.16.0 WinLDAP
Release-Date: 2026-06-24

### operating system

Windows 11 Pro 25H2



 @icing







<details>
  <summary>click to expand empty auth seen in wireshark </summary>
  
~~~
Lightweight Directory Access Protocol
    LDAPMessage bindRequest(1) "<ROOT>" simple
        messageID: 1
        protocolOp: bindRequest (0)
            bindRequest
                version: 3
                name: 
                authentication: simple (0)
                    simple: 
        [Response In: 9]
~~~
</details>
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `4ce309d968cfe02c402d07b2911241c38a8adf6b` and the full history behind it is present.
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
