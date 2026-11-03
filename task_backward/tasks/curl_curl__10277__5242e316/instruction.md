# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
libcurl 7.87 is crashing when used with curl_multi_exec

<!-- Only file bugs here! Ask questions on the mailing lists https://curl.se/mail/

     SECURITY RELATED? Post it here: https://hackerone.com/curl

     There are collections of known issues to be aware of:
     https://curl.se/docs/knownbugs.html
     https://curl.se/docs/todo.html       -->

### I did this
We're running multiple requests using https://github.com/php-curl-class/php-curl-class 

At some point, the script goes to Segmentation fault.
gdb gives the following backtrace
```
(gdb) run [.... php app]
Starting program: /opt/cpanel/ea-php74/root/usr/bin/php / [.... php app]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
[2023-01-11 04:15:58] Preparing tables for saving data...
[2023-01-11 04:15:58] Total records in selected_hotels: 998;
[2023-01-11 04:15:58] Total uuids for getting data: 993;
[2023-01-11 04:15:58] Start saving data...
[New Thread 0x7fffdcbff700 (LWP 265285)]
[New Thread 0x7fffdc3fe700 (LWP 265286)]
[New Thread 0x7fffdbbfd700 (LWP 265287)]
[New Thread 0x7fffdb3fc700 (LWP 265288)]
[New Thread 0x7fffdabfb700 (LWP 265289)]
[Thread 0x7fffdb3fc700 (LWP 265288) exited]
[Thread 0x7fffdabfb700 (LWP 265289) exited]
[Thread 0x7fffdcbff700 (LWP 265285) exited]
[Thread 0x7fffdc3fe700 (LWP 265286) exited]
[Thread 0x7fffdbbfd700 (LWP 265287) exited]
[>                                                  ] 1%  5/993  
Program received signal SIGSEGV, Segmentation fault.
0x00007fffed3bb671 in ?? () from /opt/cpanel/libcurl/lib64/libcurl.so.4
(gdb) bt
#0  0x00007fffed3bb671 in ?? () from /opt/cpanel/libcurl/lib64/libcurl.so.4
#1  0x00007ffff65607bf in ssl3_get_record () from /opt/cpanel/ea-openssl11/lib/libssl-ea.so.1.1
#2  0x00007ffff655df33 in ssl3_read_bytes () from /opt/cpanel/ea-openssl11/lib/libssl-ea.so.1.1
#3  0x00007ffff6565bea in ssl3_read () from /opt/cpanel/ea-openssl11/lib/libssl-ea.so.1.1
#4  0x00007ffff657153d in ssl_read_internal () from /opt/cpanel/ea-openssl11/lib/libssl-ea.so.1.1
#5  0x00007ffff6571723 in SSL_read () from /opt/cpanel/ea-openssl11/lib/libssl-ea.so.1.1
#6  0x00007fffed3bc8ef in ?? () from /opt/cpanel/libcurl/lib64/libcurl.so.4
#7  0x00007fffed3c0a48 in ?? () from /opt/cpanel/libcurl/lib64/libcurl.so.4
#8  0x00007fffed381c02 in ?? () from /opt/cpanel/libcurl/lib64/libcurl.so.4
#9  0x00007fffed39aaf7 in ?? () from /opt/cpanel/libcurl/lib64/libcurl.so.4
#10 0x00007fffed3ae425 in ?? () from /opt/cpanel/libcurl/lib64/libcurl.so.4
#11 0x00007fffed3937d6 in ?? () from /opt/cpanel/libcurl/lib64/libcurl.so.4
#12 0x00007fffed394376 in curl_multi_perform () from /opt/cpanel/libcurl/lib64/libcurl.so.4
#13 0x00007fffed5fc78a in zif_curl_multi_exec () from /opt/cpanel/ea-php74/root/usr/lib64/php/modules/curl.so
#14 0x00007fffe17394b3 in zif_ddtrace_curl_multi_exec (execute_data=0x7ffff4a152b0, return_value=0x7fffffffa760) at /root/datadog/tmp/build_extension/ext/php7/handlers_curl.c:424
#15 0x00007fffe17237f8 in zai_interceptor_execute_internal_impl (prev=false, return_value=0x7fffffffa760, execute_data=0x7ffff4a152b0)
    at /root/datadog/tmp/build_extension/zend_abstract_interface/interceptor/php7/interceptor.c:415
#16 zai_interceptor_execute_internal_no_prev (execute_data=0x7ffff4a152b0, return_value=0x7fffffffa760) at /root/datadog/tmp/build_extension/zend_abstract_interface/interceptor/php7/interceptor.c:421
#17 0x00000000006c8293 in execute_ex ()
#18 0x00000000006375b0 in zend_call_function ()
#19 0x0000000000577d0b in zif_call_user_func_array ()
#20 0x00007fffe17237f8 in zai_interceptor_execute_internal_impl (prev=false, return_value=0x7ffff4a14480, execute_data=0x7ffff4a14490)
    at /root/datadog/tmp/build_extension/zend_abstract_interface/interceptor/php7/interceptor.c:415
#21 zai_interceptor_execute_internal_no_prev (execute_data=0x7ffff4a14490, return_value=0x7ffff4a14480) at /root/datadog/tmp/build_extension/zend_abstract_interface/interceptor/php7/interceptor.c:421
#22 0x00000000006ca3b7 in execute_ex ()
#23 0x00000000006caf40 in zend_execute ()
#24 0x0000000000645e93 in zend_execute_scripts ()
#25 0x00000000005e4250 in php_execute_script ()
#26 0x00000000006ccf0a in do_cli ()
#27 0x0000000000444b30 in main ()
(gdb) print (char *)executor_globals.current_execute_data.prev_execute_data.func.common.scope.name.val
$1 = 0x7fffdd4ca298 "Curl\\MultiCurl"
(gdb) print (char *)executor_globals.current_execute_data.prev_execute_data.func.common.function_name.val
$2 = 0x7fffdd58dc78 "start"
(gdb) print (char *)executor_globals.current_execute_data.func.common.function_name.val
$3 = 0xc88128 "curl_multi_exec"
(gdb) 
```

### I expected the following
With previous versions, everything worked fine.

**Important** 
When we turn the verbose mode on - it works.
Or when we set the following option
```
$multiCurl->setOpt(CURLINFO_HEADER_OUT, false);
```

It also works.
We’ve spent a few days debugging. So far, it seems that nothing was changed on our side, except the update to 7.87 version.

### curl/libcurl version
```
Array
(
    [version_number] => 481024
    [age] => 10
    [features] => 296731549
    [ssl_version_number] => 0
    [version] => 7.87.0
    [host] => x86_64-redhat-linux-gnu
    [ssl_version] => OpenSSL/1.1.1s
    [libz_version] => 1.2.7
    [protocols] => Array
        (
            [0] => dict
            [1] => file
            [2] => ftp
            [3] => ftps
            [4] => gopher
            [5] => gophers
            [6] => http
            [7] => https
            [8] => imap
            [9] => imaps
            [10] => mqtt
            [11] => pop3
            [12] => pop3s
            [13] => rtsp
            [14] => scp
            [15] => sftp
            [16] => smb
            [17] => smbs
            [18] => smtp
            [19] => smtps
            [20] => telnet
            [21] => tftp
        )

    [ares] => 
    [ares_num] => 0
    [libidn] => 
    [iconv_ver_num] => 0
    [libssh_version] => libssh2/1.8.0
    [brotli_ver_num] => 16777225
    [brotli_version] => 1.0.9
)

```
### operating system
Linux [hostname] 3.10.0-1160.53.1.el7.x86_64 #1 SMP Fri Jan 14 13:59:45 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux

cat /etc/os-release
```
NAME="CentOS Linux"
VERSION="7 (Core)"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="7"
PRETTY_NAME="CentOS Linux 7 (Core)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:centos:centos:7"
HOME_URL="https://www.centos.org/"
BUG_REPORT_URL="https://bugs.centos.org/"

CENTOS_MANTISBT_PROJECT="CentOS-7"
CENTOS_MANTISBT_PROJECT_VERSION="7"
REDHAT_SUPPORT_PRODUCT="centos"
REDHAT_SUPPORT_PRODUCT_VERSION="7"

```


<!-- On Unix please post the output of "uname -a" -->


I did a bisect between curl-7_86_0 and curl-7_87_0, and crashes starts appearing from the following commit
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `5cf5bfcd134c1378af6dbae723abf88e309117df` and the full history behind it is present.
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
