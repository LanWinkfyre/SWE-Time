# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
curl: (35) error:0A00010B:SSL routines::wrong version number

~~~
*   Trying 127.0.0.1:8443...
* Connect socket 5 over QUIC to 127.0.0.1:8443
* Skipped certificate verification
* Connected to 127.0.0.1 (127.0.0.1) port 8443 (#0)
* Connected to 127.0.0.1 (127.0.0.1) port 8443 (#0)
* ALPN: offers http/1.1
* TLSv1.0 (OUT), TLS header, Certificate Status (22):
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* error:0A00010B:SSL routines::wrong version number
* Connection #0 to host 127.0.0.1 left intact
curl: (35) error:0A00010B:SSL routines::wrong version number
~~~
### I did this

curl -k -v --http3 https://127.0.0.1:8443/

### I expected the following

~~~
*   Trying 127.0.0.1:8443...
* Connect socket 5 over QUIC to 127.0.0.1:8443
* Skipped certificate verification
* Connected to 127.0.0.1 (127.0.0.1) port 8443 (#0)
* h2h3 [:method: GET]
* h2h3 [:path: /]
* h2h3 [:scheme: https]
* h2h3 [:authority: 127.0.0.1:8443]
* h2h3 [user-agent: curl/7.86.1-DEV]
* h2h3 [accept: */*]
* Using HTTP/3 Stream ID: 0 (easy handle 0x55e3ba63bf40)
> GET / HTTP/3
> Host: 127.0.0.1:8443
> user-agent: curl/7.86.1-DEV
> accept: */*
>
* ngh3_stream_recv returns 0 bytes and EAGAIN
< HTTP/3 200
< server: nginx/1.23.2
< date: Thu, 17 Nov 2022 06:40:56 GMT
< content-type: text/html
< content-length: 612
< last-modified: Tue, 21 Apr 2020 14:09:01 GMT
< etag: "5e9efe7d-264"
< alt-svc: h3=":8443"; ma=86400
< accept-ranges: bytes
<
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
* Connection #0 to host 127.0.0.1 left intact
~~~
### curl/libcurl version
curl 7.87.0-DEV (x86_64-pc-linux-gnu) libcurl/7.87.0-DEV OpenSSL/3.0.0 zlib/1.2.11 ngtcp2/0.12.0-DEV nghttp3/0.8.0-DEV
Release-Date: [unreleased]
Protocols: dict file ftp ftps gopher gophers http https imap imaps mqtt pop3 pop3s rtsp smb smbs smtp smtps telnet tftp
Features: alt-svc AsynchDNS HSTS HTTP3 HTTPS-proxy IPv6 Largefile libz NTLM NTLM_WB SSL threadsafe TLS-SRP UnixSockets

[curl -V output]

~~~
*   Trying 127.0.0.1:8443...
* Connect socket 5 over QUIC to 127.0.0.1:8443
* Skipped certificate verification
* Connected to 127.0.0.1 (127.0.0.1) port 8443 (#0)
* Connected to 127.0.0.1 (127.0.0.1) port 8443 (#0)
* ALPN: offers http/1.1
* TLSv1.0 (OUT), TLS header, Certificate Status (22):
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* error:0A00010B:SSL routines::wrong version number
* Connection #0 to host 127.0.0.1 left intact
curl: (35) error:0A00010B:SSL routines::wrong version number
~~~

### operating system
Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-131-generic x86_64)
<!-- On Unix please post the output of "uname -a" -->


 /cc @icing
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `14d5589032d5330a3d8716a9f59b85951514412d` and the full history behind it is present.
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
