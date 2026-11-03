# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
7.65.3: "Send failure: Broken pipe" error when existing connection has died 

__[updated]__ After Debian upgraded to curl 7.65.3, a unit tests from the R bindings that has been stable for the last years, started failing intermittently with this error: `Send failure: Broken pipe`.

The bug is that curl does not always detect a died connection.

The unit test performs a series of requests to a local http server, each in a separate easy handle but using one and the same multi-handle that keep track of existing connections. However in between each request the http server is restarted, which obviously kills the existing connections.

## Correct behavior (7.65.1)

Before each request curl correctly detects that the existing connection is dead:

```
* Connection #2 to host 127.0.0.1 left intact
* Found bundle for host 127.0.0.1: 0x7f945eda56c0 [serially]
* Connection 2 seems to be dead!
* Closing connection 2
* Hostname 127.0.0.1 was found in DNS cache
*   Trying 127.0.0.1:9359...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 9359 (#3)
```

We do this many times and each time curl recognizes when a connection has died and starts a new one, and then succeeds in the request.

## New behavior (7.65.3)

Full example below. Note that it has not noticed that the `Connection #0` has died until after it has tried to send the second request (`Recv failure: Connection reset by peer`). It then recovers with `Connection died, retrying a fresh connect`. 

However when it happens again later at `Re-using existing connection! (#2) with host 127.0.0.1` it seems to fail completely with `Send failure: Broken pipe`.


```
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 9359 (#0)
> POST / HTTP/1.1
Host: 127.0.0.1:9359
User-Agent: R (3.6.1 x86_64-apple-darwin15.6.0 x86_64 darwin15.6.0)
Accept: */*
Accept-Encoding: deflate, gzip
Content-Length: 26300858
Content-Type: multipart/form-data; boundary=------------------------b48be84cafc652cc

* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Tue, 20 Aug 2019 14:26:16 GMT
< Content-Type: text/plain
< Content-Length: 0
< 
* Connection #0 to host 127.0.0.1 left intact
* Found bundle for host 127.0.0.1: 0x7fc0015b9f90 [serially]
* Re-using existing connection! (#0) with host 127.0.0.1
* Connected to 127.0.0.1 (127.0.0.1) port 9359 (#0)
> POST / HTTP/1.1
Host: 127.0.0.1:9359
User-Agent: R (3.6.1 x86_64-apple-darwin15.6.0 x86_64 darwin15.6.0)
Accept: */*
Accept-Encoding: deflate, gzip
Content-Length: 25193058
Content-Type: multipart/form-data; boundary=------------------------ae32bd27cbda0f89

* Recv failure: Connection reset by peer
* Connection died, retrying a fresh connect
* Closing connection 0
* Issue another request to this URL: 'http://127.0.0.1:9359/'
* Hostname 127.0.0.1 was found in DNS cache
*   Trying 127.0.0.1:9359...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 9359 (#1)
> POST / HTTP/1.1
Host: 127.0.0.1:9359
User-Agent: R (3.6.1 x86_64-apple-darwin15.6.0 x86_64 darwin15.6.0)
Accept: */*
Accept-Encoding: deflate, gzip
Content-Length: 25193058
Content-Type: multipart/form-data; boundary=------------------------f1c8bb9f687fb628

* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Tue, 20 Aug 2019 14:26:17 GMT
< Content-Type: text/plain
< Content-Length: 0
< 
* Connection #1 to host 127.0.0.1 left intact
* Connection 1 seems to be dead!
* Closing connection 1
* Hostname 127.0.0.1 was found in DNS cache
*   Trying 127.0.0.1:9359...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 9359 (#2)
> POST / HTTP/1.1
Host: 127.0.0.1:9359
User-Agent: R (3.6.1 x86_64-apple-darwin15.6.0 x86_64 darwin15.6.0)
Accept: */*
Accept-Encoding: deflate, gzip
Content-Length: 25994122
Content-Type: multipart/form-data; boundary=------------------------b732842d3a248b04

* We are completely uploaded and fine
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Tue, 20 Aug 2019 14:26:18 GMT
< Content-Type: text/plain
< Content-Length: 0
< 
* Connection #2 to host 127.0.0.1 left intact
* Found bundle for host 127.0.0.1: 0x7fc0014471a0 [serially]
* Re-using existing connection! (#2) with host 127.0.0.1
* Connected to 127.0.0.1 (127.0.0.1) port 9359 (#2)
> POST / HTTP/1.1
Host: 127.0.0.1:9359
User-Agent: R (3.6.1 x86_64-apple-darwin15.6.0 x86_64 darwin15.6.0)
Accept: */*
Accept-Encoding: deflate, gzip
Content-Length: 26011426
Content-Type: multipart/form-data; boundary=------------------------3fcc55e2d2db469e

* Send failure: Broken pipe
* Closing connection 2
```

Here is my bisect result:
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `862393243d16870347e56195e93dc47274e32601` and the full history behind it is present.
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
