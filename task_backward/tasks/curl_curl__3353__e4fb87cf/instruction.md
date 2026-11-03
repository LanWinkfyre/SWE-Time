# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
HTTP digest authentication with GET parameters no longer sending the right uri

I am hosting an HTTP server with Apache2 version 2.4.37-1 from Debian with mod_digest and trying to query it with curl 7.62.0-1 and libcurl4 7.62.0-1 from Debian. With this curl version, I am getting an error 400 when querying the server on URLs that include GET parameters:

```
$ curl --digest -u a3nm 'https://git.a3nm.net/enum2/info/refs?service=git-upload-pack' 
Enter host password for user 'a3nm':              
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
</p>
</body></html>
```

Here is the `curl -V` of this curl version:

```
$ curl -V                            
curl 7.62.0 (x86_64-pc-linux-gnu) libcurl/7.62.0 OpenSSL/1.1.1a zlib/1.2.11 libidn2/2.0.5 libpsl/0.20.2 (+libidn2/2.0.5) libssh2/1.8.0 nghttp2/1.34.0 librtmp/2.3
Release-Date: 2018-10-31
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp 
Features: AsynchDNS IDN IPv6 Largefile GSS-API Kerberos SPNEGO NTLM NTLM_WB SSL libz TLS-SRP HTTP2 UnixSockets HTTPS-proxy PSL 
```

By contrast, when downgrading to libcurl3 7.52.1-5+deb9u8 and curl version 7.52.1-5+deb9u8 from Debian, doing the same thing works fine:

```
$ curl --digest -u a3nm 'https://git.a3nm.net/enum2/info/refs?service=git-upload-pack'
Enter host password for user 'a3nm':
[actual response here]
```

Here is the `curl -V` of this curl version:

```
$ curl -V
curl 7.52.1 (x86_64-pc-linux-gnu) libcurl/7.52.1 OpenSSL/1.0.2q zlib/1.2.11 libidn2/2.0.5 libpsl/0.20.2 (+libidn2/2.0.5) libssh2/1.8.0 nghttp2/1.34.0 librtmp/2.3
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp 
Features: AsynchDNS IDN IPv6 Largefile GSS-API Kerberos SPNEGO NTLM NTLM_WB SSL libz TLS-SRP HTTP2 UnixSockets HTTPS-proxy PSL 
```

In the Apache2 error log, the problem with the bad curl version (using libcurl4) is reported as:

```
[Sun Dec 09 10:39:49.805530 2018] [auth_digest:error] [pid 8691:tid 281471445082528] [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] AH01786: uri mismatch - </enum2/info/refs> does not match request-uri </enum2/info/refs?service=git-upload-pack>
````

And indeed, during authentication, this is what is exchanged between Apache2 and the bad curl version, according to mod_dumpio. Note that, in the `uri` parameter of the `Authorization` header, the GET parameters do not appear, which is what Apache complains about:

```
[Sun Dec 09 10:39:49.804225 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_in [init-blocking] 0 readbytes
[Sun Dec 09 10:39:49.804334 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:39:49.804523 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): 55 bytes
[Sun Dec 09 10:39:49.804563 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): GET /enum2/info/refs?service=git-upload-pack HTTP/1.1\r\n
[Sun Dec 09 10:39:49.804620 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:39:49.804656 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): 20 bytes
[Sun Dec 09 10:39:49.804688 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): Host: git.a3nm.net\r\n
[Sun Dec 09 10:39:49.804722 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:39:49.804755 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): 299 bytes
[Sun Dec 09 10:39:49.804786 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): Authorization: Digest username="REDACTED", realm="a3nm.net version control", nonce="REDACTED", uri="/enum2/info/refs", cnonce="REDACTED", nc=00000001, qop=auth, response="REDACTED", algorithm="MD5"\r\n
[Sun Dec 09 10:39:49.804834 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:39:49.804867 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): 25 bytes
[Sun Dec 09 10:39:49.804898 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): User-Agent: curl/7.62.0\r\n
[Sun Dec 09 10:39:49.804935 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:39:49.804968 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): 13 bytes
[Sun Dec 09 10:39:49.804999 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): Accept: */*\r\n
[Sun Dec 09 10:39:49.805097 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:39:49.805133 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): 2 bytes
[Sun Dec 09 10:39:49.805164 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_in (data-TRANSIENT): \r\n
[Sun Dec 09 10:39:49.805530 2018] [auth_digest:error] [pid 8691:tid 281471445082528] [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] AH01786: uri mismatch - </enum2/info/refs> does not match request-uri </enum2/info/refs?service=git-upload-pack>
[Sun Dec 09 10:39:49.805660 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(164): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_out
[Sun Dec 09 10:39:49.805697 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_out (data-HEAP): 166 bytes
[Sun Dec 09 10:39:49.805729 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_out (data-HEAP): HTTP/1.1 400 Bad Request\r\nDate: Sun, 09 Dec 2018 10:39:49 GMT\r\nServer: Apache\r\nContent-Length: 226\r\nConnection: close\r\nContent-Type: text/html; charset=iso-8859-1\r\n\r\n
[Sun Dec 09 10:39:49.805774 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(164): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_out
[Sun Dec 09 10:39:49.805804 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_out (data-HEAP): 226 bytes
[Sun Dec 09 10:39:49.805835 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_out (data-HEAP): <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n<html><head>\n<title>400 Bad Request</title>\n</head><body>\n<h1>Bad Request</h1>\n<p>Your browser sent a request that this server could not understand.<br />\n</p>\n</body></html>\n
[Sun Dec 09 10:39:49.805877 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_out (metadata-EOS): 0 bytes
[Sun Dec 09 10:39:49.806142 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(164): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_out
[Sun Dec 09 10:39:49.806181 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_out (metadata-EOR): 0 bytes
[Sun Dec 09 10:39:49.806353 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(164): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio: dumpio_out
[Sun Dec 09 10:39:49.806388 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_out (metadata-FLUSH): 0 bytes
[Sun Dec 09 10:39:49.806422 2018] [dumpio:trace7] [pid 8691:tid 281471445082528] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34026] mod_dumpio:  dumpio_out (metadata-EOC): 0 bytes
```

Compare this to what happens between Apache2 and the good curl version. Note that, in the `Authorization` header, the uri correctly includes the GET parameter:

```
[Sun Dec 09 10:35:48.123520 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_in [init-blocking] 0 readbytes
[Sun Dec 09 10:35:48.123617 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:35:48.123866 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): 55 bytes
[Sun Dec 09 10:35:48.123907 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): GET /enum2/info/refs?service=git-upload-pack HTTP/1.1\r\n
[Sun Dec 09 10:35:48.123963 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:35:48.123999 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): 20 bytes
[Sun Dec 09 10:35:48.124031 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): Host: git.a3nm.net\r\n
[Sun Dec 09 10:35:48.124065 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:35:48.124097 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): 323 bytes
[Sun Dec 09 10:35:48.124129 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): Authorization: Digest username="REDACTED", realm="a3nm.net version control", nonce="REDACTED", uri="/enum2/info/refs?service=git-upload-pack", cnonce="REDACTED", nc=00000001, qop=auth, response="REDACTED", algorithm="MD5"\r\n
[Sun Dec 09 10:35:48.124178 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:35:48.124211 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): 25 bytes
[Sun Dec 09 10:35:48.124242 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): User-Agent: curl/7.52.1\r\n
[Sun Dec 09 10:35:48.124279 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:35:48.124311 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): 13 bytes
[Sun Dec 09 10:35:48.124342 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): Accept: */*\r\n
[Sun Dec 09 10:35:48.124375 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(140): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_in [getline-blocking] 0 readbytes
[Sun Dec 09 10:35:48.124408 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): 2 bytes
[Sun Dec 09 10:35:48.124439 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_in (data-TRANSIENT): \r\n
[Sun Dec 09 10:35:48.138238 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(164): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_out
[Sun Dec 09 10:35:48.138440 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_out (data-HEAP): 413 bytes
[Sun Dec 09 10:35:48.138480 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_out (data-HEAP): HTTP/1.1 200 OK\r\nDate: Sun, 09 Dec 2018 10:35:48 GMT\r\nServer: Apache\r\nExpires: Fri, 01 Jan 1980 00:00:00 GMT\r\nPragma: no-cache\r\nCache-Control: no-cache, max-age=0, must-revalidate\r\nAuthentication-Info: rspauth="REDACTED", cnonce="REDACTED", nc=00000001, qop=auth\r\nTransfer-Encoding: chunked\r\nContent-Type: application/x-git-upload-pack-advertisement\r\n\r\n
[Sun Dec 09 10:35:48.138555 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(164): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio: dumpio_out
[Sun Dec 09 10:35:48.138588 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_out (data-TRANSIENT): 4 bytes
[Sun Dec 09 10:35:48.138622 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(103): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_out (data-TRANSIENT): 22\r\n
[Sun Dec 09 10:35:48.138656 2018] [dumpio:trace7] [pid 8691:tid 281471487046048] mod_dumpio.c(63): [client 2001:660:330f:cc:6600:6aff:fe7c:7854:34014] mod_dumpio:  dumpio_out (data-HEAP): 34 bytes
[...]
```

It seems to me that Apache2 is right in rejecting authentication by recent versions of curl (using libcurl4), according to https://tools.ietf.org/html/rfc2617#section-3.2.2.5. Would you have any idea of why this was broken from libcurl3 to libcurl4?

Many thanks for your help!

(PS: as might be apparent from the URLs, I got bitten by this problem because `git` is using libcurl and accessing git repositories with HTTP Digest authentication is no longer working for me at all. For the benefit of anyone else who might be running into the issue from git, when using git the problem manifests itself as the following message when accessing the repository (e.g., when doing `git pull`): `fatal: unable to access '[repository URL]': The requested URL returned error: 400`.)
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `d997aa0e963c5be5de100dccdc5208d39bd3d62b` and the full history behind it is present.
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
