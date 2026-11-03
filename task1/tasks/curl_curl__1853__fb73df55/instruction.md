# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Using an HTTPS proxy hangs curl

### I did this

```
curl -v --proxy-insecure -x https://localhost:8080 http://google.com/
```

### I expected the following

```
<response from http://google.com>
```

### What actually happened

```
*   Trying ::1...
* TCP_NODELAY set
* Connected to localhost (::1) port 8080 (#0)
* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
* successfully set certificate verify locations:
*   CAfile: /usr/local/etc/openssl/cert.pem
  CApath: /usr/local/etc/openssl/certs
* TLSv1.2 (OUT), TLS header, Certificate Status (22):
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Client hello (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS change cipher, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Finished (20):
* SSL connection using TLSv1.2 / ECDHE-RSA-AES256-GCM-SHA384
* Proxy certificate:
*  subject: C=AU; ST=Some-State; O=Internet Widgits Pty Ltd
*  start date: Dec  7 19:02:52 2016 GMT
*  expire date: Dec  7 19:02:52 2017 GMT
*  issuer: C=AU; ST=Some-State; O=Internet Widgits Pty Ltd
*  SSL certificate verify result: self signed certificate (18), continuing anyway.
```

_**...hangs at this point**_

### curl/libcurl version

```
curl 7.55.1 (x86_64-apple-darwin16.7.0) libcurl/7.55.1 OpenSSL/1.0.2l zlib/1.2.8 nghttp2/1.25.0
Release-Date: 2017-08-14
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp smb smbs smtp smtps telnet tftp
Features: AsynchDNS IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP HTTP2 UnixSockets HTTPS-proxy
```

### operating system

macOS Sierra 10.12.6

---

This is the same behaviour as: https://github.com/curl/curl/issues/1156

I am using [the same gist](https://gist.github.com/agl/2da9e61528f0d373894d8c919abfb518) to run a basic HTTPS proxy.

 I didn't use the gist script for reasons noted below, instead I manually monitored socat output to see when the ~~CONNECT~~ GET lines would show (if they did `bisect good`, if they didn't `bisect bad`).
`socat openssl-listen:4433,reuseaddr,fork,cert=yourcerthere.pem,verify=0 -`

The reason I didn't use the gist script is because that was a very narrow example written to help us reproduce an issue with a proxytunnel to google's server. if you look in the script you'll see that. Technically you could repurpose it by changing the line in the script to `net.Dial("tcp", "www.google.com:80")` and then add curl option `--proxytunnel` since curl by default won't tunnel http connections, but the bug is not reproducible then.
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `5bae72734b45a01c6337eb3b2c40020c4e904415` and the full history behind it is present.
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
