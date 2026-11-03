# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
segmentation fault with threaded resolver

### I did this

I built a package for `curl` `7.20.0` earlier today and pushed it to Arch's testing repositories.

With that package installed `pacman` started to misbehave, crashing with segmentation faults. Easiest way is to run `pacstrap`, which is a shell script and runs `pacman` to bootstrap an installation:
```
pacstrap /path/to/empty/directory/ base
```



CC @christian-heusel @kode54 @icing 

### I expected the following

Things should just work, without crashing. 😉️

### curl/libcurl version

curl 8.20.0 (x86_64-pc-linux-gnu) libcurl/8.20.0 OpenSSL/3.6.2 zlib/1.3.1.zlib-ng brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.69.0 ngtcp2/1.22.1 nghttp3/1.15.0 mit-krb5/1.21.3
Release-Date: 2026-04-29
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns mqtt mqtts pop3 pop3s rtsp scp sftp smtp smtps telnet tftp ws wss
Features: alt-svc brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz PSL SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd

### operating system

Arch Linux
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `a05f34973e6c4bb629d018f7cb51487be1c904d8` and the full history behind it is present.
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
