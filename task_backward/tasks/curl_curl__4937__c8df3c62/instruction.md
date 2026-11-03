# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
parallel downloaded files with some of them to be 0 byte

<!-- Only file bugs here! Ask questions on the mailing lists https://curl.haxx.se/mail/

     SECURITY RELATED? Post it here: https://hackerone.com/curl

     There are collections of known issues to be aware of:
     https://curl.haxx.se/docs/knownbugs.html
     https://curl.haxx.se/docs/todo.html       -->

### I did this
When I tried to download some html files with this command `curl --config config.txt`,the last 4 downloaded html files are 0 byte,and other files are all right.
However it will be allright without `--parallel-max 3` in config.txt.
The config.txt content:

> --remote-name-all
--location
--compressed
--user-agent "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3"
--url https://xing.911cha.com/xing_%E3%91%8E.html
--url https://xing.911cha.com/xing_%E3%92%92.html
--url https://xing.911cha.com/xing_%E3%94%A9.html
--url https://xing.911cha.com/xing_%E3%9C%A8.html
--url https://xing.911cha.com/xing_%E3%A1%93.html
--url https://xing.911cha.com/xing_%E3%A4%A9.html
--url https://xing.911cha.com/xing_%E3%A8%85.html
--url https://xing.911cha.com/xing_%E3%AC%A5.html
--url https://xing.911cha.com/xing_%E3%AF%81.html
--url https://xing.911cha.com/xing_%E3%B2%BB.html
--url https://xing.911cha.com/xing_%E3%B5%9F.html
--parallel
--parallel-max 3

### I expected the following
I expect all downloaded files are OK in parallel mode,with no 0 byte files.
curl 7.66 does not have this problem.
### curl/libcurl version
`curl 7.68.0 (x86_64-pc-win32) libcurl/7.68.0 OpenSSL/1.1.1d (Schannel) zlib/1.2.11 brotli/1.0.7 WinIDN libssh2/1.9.0 nghttp2/1.40.0
Release-Date: 2020-01-08
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtsp scp sftp smb smbs smtp smtps telnet tftp
Features: AsynchDNS HTTP2 HTTPS-proxy IDN IPv6 Kerberos Largefile MultiSSL NTLM SPNEGO SSL SSPI TLS-SRP brotli libz`
### operating system
Windows 10 17134
<!-- On Unix please post the output of "uname -a" -->


> I hope this information would be helpful.

Thanks it is.

 @bagder queued handles seem to be indefinitely skipped at the beginning of parallel transfers, was there a reason for that?
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `4a4b63daaa01ef59b131d91e8e6e6dfe275c0f08` and the full history behind it is present.
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
