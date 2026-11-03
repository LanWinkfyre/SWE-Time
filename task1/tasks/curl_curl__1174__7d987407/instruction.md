# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Connection timeout on https streams



 Such errors did not happen in prior commits.

This does not occur for http streams.

@MaxKellerman may be interested.

I'm running Gentoo.


Running hiperfifo from docs/examples exhibits the same behavior, with every HTTPS server I've tried. I get the following output:

	Adding easy 0x20a1150 to multi 0x206c8a0 (https://startpage.com)
	multi_timer_cb: Setting timeout to 0 ms
	* Rebuilt URL to: https://startpage.com/
	*   Trying 37.0.87.15...
	* TCP_NODELAY set
	Progress: https://startpage.com (0/0)
	Progress: https://startpage.com (0/0)
	socket callback: s=7 e=0x20a1150 what=OUT Adding data: OUT
	multi_timer_cb: Setting timeout to 0 ms
	REMAINING: 1
	Progress: https://startpage.com (0/0)
	multi_timer_cb: Setting timeout to 199 ms
	REMAINING: 1
	* Connected to startpage.com (37.0.87.15) port 443 (#0)
	Progress: https://startpage.com (0/0)
	* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
	* successfully set certificate verify locations:
	*   CAfile: /etc/ssl/certs/ca-certificates.crt
	  CApath: none
	Progress: https://startpage.com (0/0)
	socket callback: s=7 e=0x20a1150 what=REMOVE 
	REMAINING: 1
	Progress: https://startpage.com (0/0)
	REMAINING: 1

and after that curl waits indefinitely (well, at least 15 minutes). If I add

    curl_easy_setopt(conn->easy, CURLOPT_CONNECTTIMEOUT, 10L);

like mpd, then curl aborts the connection after 10 s:

	* Operation timed out after 10010 milliseconds with 0 out of 0 bytes received
	Progress: https://startpage.com (0/0)
	* Closing connection 0
	REMAINING: 0
	DONE: https://startpage.com/ => (28) Operation timed out after 10010 milliseconds with 0 out of 0 bytes received

Tested on Debian Jessie (using OpenSSL/1.0.1t and zlib/1.2.8) and Gentoo (using OpenSSL/1.0.2j and zlib/1.2.8). The bug appears to be specific to openssl - the gnutls backend works.  The command-line client works in all cases.
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `00c817068ed9e73974b3fedf6b9d7cb085db69f4` and the full history behind it is present.
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
