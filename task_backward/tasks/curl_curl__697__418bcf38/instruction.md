# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
cURL looses Cookie information when CURLOPT_FOLLOWLOCATION is true

### I did this

On Debian 7.9 with cURL 7.26.0-1+wheezy13 and PHP 5.3.3-7+squeeze19 we can succesfully login into Siemens C470/N300 DECT base stations. After upgrading to Debian 8 and cURL 7.38.0 this no longer works. I've also tested this on Debian 9 (Stretch/sid) with cURL 7.47.0 and the problem exists there still.

No cookies were saved to the Cookie JAR on either of these occasions.

After debugging somewhat I appear to have found the issue, the authentication is succesful, and the host returns a cookie with a 303 redirect. This cookie is then lost for any subsequent request, nor is it written to the cookie jar.

Apparently there has been a change since cURL 7.26 that no longer saves the cookie on redirect. Unfortunate. It appears I was not the only one that ran into this issue.
- FOLLOWLOCATION is true: It does not even write a cookie jar header. The file is 0 bytes.
- FOLLOWLOCATION is false: we only get a cookie header in the cookie jar.
### I expected the following

I expected a successful login where the cookie is saved to the jar when the login page redirects as 7.26.0 previously did. Perhaps this was changed for security reasons but with a side effect. I could not find a option for cURL to save this cookie on redirect.
### curl/libcurl version

seth@lsautom:~$ curl --version
curl 7.47.0 (x86_64-pc-linux-gnu) libcurl/7.47.0 GnuTLS/3.4.9 zlib/1.2.8 libidn/1.32 libssh2/1.5.0 nghttp2/1.7.1 librtmp/2.3
Protocols: dict file ftp ftps gopher http https imap imaps ldap ldaps pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp
Features: AsynchDNS IDN IPv6 Largefile GSS-API Kerberos SPNEGO NTLM NTLM_WB SSL libz TLS-SRP HTTP2 UnixSockets
### operating system

Debian Stretch/sid ~02-03-2016

```
seth@lsautom:~$ php -v
PHP 5.6.17-3 (cli)
Copyright (c) 1997-2015 The PHP Group
Zend Engine v2.6.0, Copyright (c) 1998-2015 Zend Technologies
    with Zend OPcache v7.0.6-dev, Copyright (c) 1999-2015, by Zend Technologies

```

Example output:

```
seth@lsautom:~$ php -f curltest.php |more
cookie jar /tmp/telecookieYrUzx4
Authentication Error: HTTP/1.1 303 See Other
Connection: Keep-Alive
Location: http://10.9.43.20/home.html
Server:
**Set-Cookie: key=14683720; path=/; expires=Sat, 21-12-2037 00:00:00 GMT**
Content-Type: text/html
Content-Length: 736

**HTTP/1.1 303 See Other**
Connection: Keep-Alive
Location: http://10.9.43.20/login.html
Server:
Content-Type: text/html
Content-Length: 738

HTTP/1.1 200 OK
Cache-Control: no-store
Connection: Keep-Alive
Pragma: no-cache
Transfer-Encoding: chunked
ETag: /login.html
Server:
Content-Type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <title>N300A IP</title>
```

Login not succesful after redirect. The cookie file is empty.

```
seth@lsautom:~$ ls -l /tmp/telecookieYrUzx4
-rw------- 1 seth Automatisering 0 mrt  2 15:48 /tmp/telecookieYrUzx4
```

Example PHP code

```
<?php
        //$USERNAME = 'guest';
        $PASSWORD = '0000';
        $SERVERURL = 'http://10.9.43.20/login.html';
        $cookiejar = tempnam('/tmp/', 'telecookie');                                            # will have to change path for windows
        echo "cookie jar {$cookiejar}\n";

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $SERVERURL . '#');
        curl_setopt($ch, CURLOPT_HEADER, 1);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($ch, CURLOPT_COOKIEFILE, $cookiejar);                                       # reads cookies from this file, but more importantly turns on cookie engine
        curl_setopt($ch, CURLOPT_COOKIEJAR, $cookiejar);                                        # writes cookies to this file on cleanup, probably not necessary
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);                                        # the Fiery uses a self-signed, non fqdn ssl cert
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);                                        # the Fiery uses a self-signed, non fqdn ssl cert

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                         # allows curl_exec to send to a variable
        curl_setopt($ch, CURLOPT_POST, true);

        # these are what gets posted to the REST API to login - it sets a session cookie that gets used for future requests
        $loginpostfields = 'language=1' . '&password=' . $PASSWORD;

        curl_setopt($ch, CURLOPT_POSTFIELDS, $loginpostfields);
        $curlout = curl_exec($ch);
        if(curl_errno($ch)) {
    echo 'Connection Error: ' . curl_error($ch);
    exit;
        }
        elseif('{"authenticated":true}' != $curlout) {
                echo 'Authentication Error: ' . $curlout;
                exit;
        }


        curl_setopt($ch, CURLOPT_POST, false);
        //curl_setopt($ch, CURLOPT_URL, $SERVERURL . 'consumables');
        $curlout = curl_exec($ch);
        $consumables = json_decode($curlout, true);
        print_r($consumables);


        curl_close($ch);
        unlink($cookiejar);
?>



```




```

curl -v -b cookies.txt -c cookies.txt -d "language=1&password=0000" -L http://127.0.0.1:8000/login.html

HTTP/1.1 302 Found
Connection: Keep-Alive
Location: http://127.0.0.1:8000/login.html
Server: 
Set-Cookie: key=14683720; path=/; expires=Sat, 21-12-2037 00:00:00 GMT
Content-Type: text/html
Content-Length: 730

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXX



```
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `3c2ef2a610814028a8dc9469b350d291327c673f` and the full history behind it is present.
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
