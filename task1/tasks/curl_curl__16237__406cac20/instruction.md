# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
curl dns resolution broken on x32

### I did this

Version: curl 8.12 tarball from most recent github tag

### Observed:

```
$ autoreconf -fi && ./configure --with-openssl --enable-ipv6 && make
[…]
  CC       ../lib/curl-version_win32.o
  CC       ../lib/curl-warnless.o
echo 'extern const void *curl_ca_embed; const void *curl_ca_embed;' > tool_ca_embed.c
  HUGE     tool_hugehelp.c
  CC       curl-tool_ca_embed.o
  CC       curl-tool_hugehelp.o
  CCLD     curl
make[1]: Leaving directory '/home/ej/curl-curl-8_12_0/src'
Making all in scripts
make[1]: Entering directory '/home/ej/curl-curl-8_12_0/scripts'
make[1]: Nothing to be done for 'all'.
make[1]: Leaving directory '/home/ej/curl-curl-8_12_0/scripts'
make[1]: Entering directory '/home/ej/curl-curl-8_12_0'
make[1]: Nothing to be done for 'all-am'.
make[1]: Leaving directory '/home/ej/curl-curl-8_12_0'

ej@a4:~/curl-curl-8_12_0$ ./src/curl inai.de
curl: (6) Could not resolve host: inai.de

ej@a4:~/curl-curl-8_12_0$ libtool --mode=execute gdb src/curl
(gdb) b getaddrinfo
(gdb) r inai.de
[…]
Thread 2 "curl" hit Breakpoint 1, __GI_getaddrinfo (name=0x47aa00 "inai.de", service=0xf6d65f14 "80", hints=0x47bc84, pai=0xf6d65ec0)
    at ./nss/getaddrinfo.c:2297
warning: 2297   ./nss/getaddrinfo.c: No such file or directory
(gdb) fin
Run till exit from #0  __GI_getaddrinfo (name=0x47aa00 "inai.de", service=0xf6d65f14 "80", hints=0x47bc84, pai=0xf6d65ec0)
    at ./nss/getaddrinfo.c:2297
0xf7ecf079 in Curl_getaddrinfo_ex (nodename=0x47aa00 "inai.de", servname=0xf6d65f14 "80", hints=0x47bc84, result=0x47bc80)
    at curl_addrinfo.c:121
121       error = getaddrinfo(nodename, servname, hints, &aihead);
Value returned is $1 = 0
(gdb) p aihead[0]
$2 = {ai_flags = 0, ai_family = 10, ai_socktype = 1, ai_protocol = 6, ai_addrlen = 28, ai_addr = 0xf64008a0, ai_canonname = 0x0, 
  ai_next = 0xf6400840}
(gdb) p aihead[0].ai_next[0]
$3 = {ai_flags = 0, ai_family = 2, ai_socktype = 1, ai_protocol = 6, ai_addrlen = 16, ai_addr = 0xf6400860, ai_canonname = 0x0, 
  ai_next = 0x0}
```

getaddrinfo in thread2 even succeeds, but it appears the dnscache in thread1 remains empty (h->table = NULL).


```
multi_runsingle (multi=0x47b970, nowp=0xffffd9a0, data=0x4800b0) at multi.c:2346
2346      struct Curl_message *msg = NULL;
(gdb) n
2348      bool protocol_connected = FALSE;
(gdb) 
2349      bool dophase_done = FALSE;
(gdb) 
2351      CURLcode result = CURLE_OK;
(gdb) 
2354      if(!GOOD_EASY_HANDLE(data))
(gdb) 
2357      if(multi->dead) {
(gdb) 
2371        bool stream_error = FALSE;
(gdb) 
2372        rc = CURLM_OK;
(gdb) 
2374        if(multi_ischanged(multi, TRUE)) {
(gdb) 
2379        if(data->mstate > MSTATE_CONNECT &&
(gdb) 
2380           data->mstate < MSTATE_COMPLETED) {
(gdb) 
2379        if(data->mstate > MSTATE_CONNECT &&
(gdb) 
2383          if(!data->conn)
(gdb) 
2389        if((data->mstate >= MSTATE_CONNECT) && (data->mstate < MSTATE_COMPLETED) &&
(gdb) 
2390           multi_handle_timeout(data, nowp, &stream_error, &result))
(gdb) 
2389        if((data->mstate >= MSTATE_CONNECT) && (data->mstate < MSTATE_COMPLETED) &&
(gdb) 
2394        switch(data->mstate) {
(gdb) 
2428          rc = state_resolving(multi, data, &stream_error, &result);
(gdb) s
state_resolving (multi=0x47b970, data=0x4800b0, stream_errorp=0xffffd8bf, resultp=0xffffd8c4) at multi.c:2219
2219      struct Curl_dns_entry *dns = NULL;
(gdb) n
2220      struct connectdata *conn = data->conn;
(gdb) 
2222      CURLcode result = CURLE_OK;
(gdb) 
2223      CURLMcode rc = CURLM_OK;
(gdb) 
2227      if(conn->bits.httpproxy)
(gdb) 
2231        if(conn->bits.conn_to_host)
(gdb) 
2234          hostname = conn->host.name;
(gdb) 
2237      dns = Curl_fetch_addr(data, hostname, conn->primary.remote_port);
(gdb) s
Curl_fetch_addr (data=0x4800b0, hostname=0x479b70 "inai.de", port=80) at hostip.c:360
360       struct Curl_dns_entry *dns = NULL;
(gdb) n
362       if(data->share)
(gdb) 
363         Curl_share_lock(data, CURL_LOCK_DATA_DNS, CURL_LOCK_ACCESS_SINGLE);
(gdb) 
365       dns = fetch_addr(data, hostname, port);
(gdb) s
fetch_addr (data=0x4800b0, hostname=0x479b70 "inai.de", port=80) at hostip.c:280
280       struct Curl_dns_entry *dns = NULL;
(gdb) n
284       size_t entry_len = create_hostcache_id(hostname, 0, port,
(gdb) n
288       dns = Curl_hash_pick(data->dns.hostcache, entry_id, entry_len + 1);
(gdb) s
Curl_hash_pick (h=0x47d630, key=0xffffd700, key_len=11) at hash.c:199
199       if(h->table) {
(gdb) n
212       return NULL;
(gdb) 
213     }
```

### I expected the following

succeed, given DNS *is* functioning properly.

```
ej@a4:~/curl-curl-8_12_0$ getent hosts inai.de
2a01:4f8:202:600a::a3 inai.de
```

### curl/libcurl version

https://github.com/curl/curl/archive/refs/tags/curl-8_12_0.tar.gz

### operating system

```
ej@a4:~/curl-curl-8_12_0$ cat /etc/os-release 
PRETTY_NAME="Debian GNU/Linux trixie/sid"
NAME="Debian GNU/Linux"
VERSION_CODENAME=trixie
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"

ej@a4:~/curl-curl-8_12_0$ cat /etc/apt/sources.list
deb https://deb.debian.org/debian-ports sid main
deb-src http://ftp.debian.org/debian sid main contrib non-free

ej@a4:~/curl-curl-8_12_0$ uname -a
Linux a4 6.13.0 #6 SMP PREEMPT_DYNAMIC Sat Jan 25 14:29:25 CET 2025 x86_64 GNU/Linux

ej@a4:~/curl-curl-8_12_0$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-linux-gnux32/14/lto-wrapper
Target: x86_64-linux-gnux32
Configured with: ../src/configure -v --with-pkgversion='Debian 14.2.0-16' --with-bugurl=file:///usr/share/doc/gcc-14/README.Bugs --enable-languages=c,ada,c++,go,d,fortran,objc,obj-c++,m2 --prefix=/usr --with-gcc-major-version-only --program-suffix=-14 --program-prefix=x86_64-linux-gnux32- --enable-shared --enable-linker-build-id --libexecdir=/usr/libexec --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-libstdcxx-backtrace --enable-gnu-unique-object --disable-vtable-verify --enable-plugin --with-system-zlib --enable-libphobos-checking=release --with-target-system-zlib=auto --enable-objc-gc=auto --enable-multiarch --disable-werror --enable-cet --with-abi=mx32 --with-multilib-list=mx32,m64,m32 --enable-multilib --enable-checking=release --build=x86_64-linux-gnux32 --host=x86_64-linux-gnux32 --target=x86_64-linux-gnux32
Thread model: posix
Supported LTO compression algorithms: zlib zstd
gcc version 14.2.0 (Debian 14.2.0-16)
```


```
ej@a4:~/curl-curl-8_12_0$ libtool --mode=execute ldd src/curl
        linux-vdso.so.1 (0xf7f76000)
        libcurl.so.4 => /home/ej/curl-curl-8_12_0/lib/.libs/libcurl.so.4 (0xf7e51000)
        libz.so.1 => /lib/x86_64-linux-gnux32/libz.so.1 (0xf7e29000)
        libc.so.6 => /lib/x86_64-linux-gnux32/libc.so.6 (0xf7c42000)
        libnghttp2.so.14 => /lib/x86_64-linux-gnux32/libnghttp2.so.14 (0xf7c14000)
        libidn2.so.0 => /lib/x86_64-linux-gnux32/libidn2.so.0 (0xf7be1000)
        librtmp.so.1 => /lib/x86_64-linux-gnux32/librtmp.so.1 (0xf7bc4000)
        libgsasl.so.18 => /lib/x86_64-linux-gnux32/libgsasl.so.18 (0xf7ba3000)
        libpsl.so.5 => /lib/x86_64-linux-gnux32/libpsl.so.5 (0xf7b90000)
        libssl.so.3 => /lib/x86_64-linux-gnux32/libssl.so.3 (0xf7a9e000)
        libcrypto.so.3 => /lib/x86_64-linux-gnux32/libcrypto.so.3 (0xf757e000)
        libldap.so.2 => /lib/x86_64-linux-gnux32/libldap.so.2 (0xf7522000)
        liblber.so.2 => /lib/x86_64-linux-gnux32/liblber.so.2 (0xf7512000)
        libzstd.so.1 => /lib/x86_64-linux-gnux32/libzstd.so.1 (0xf7459000)
        libbrotlidec.so.1 => /lib/x86_64-linux-gnux32/libbrotlidec.so.1 (0xf744b000)
        /libx32/ld-linux-x32.so.2 (0xf7f78000)
        libunistring.so.5 => /lib/x86_64-linux-gnux32/libunistring.so.5 (0xf7270000)
        libgnutls.so.30 => /lib/x86_64-linux-gnux32/libgnutls.so.30 (0xf706e000)
        libhogweed.so.6 => /lib/x86_64-linux-gnux32/libhogweed.so.6 (0xf7026000)
        libnettle.so.8 => /lib/x86_64-linux-gnux32/libnettle.so.8 (0xf6fd5000)
        libgmp.so.10 => /lib/x86_64-linux-gnux32/libgmp.so.10 (0xf6f50000)
        libidn.so.12 => /lib/x86_64-linux-gnux32/libidn.so.12 (0xf6f1d000)
        libntlm.so.0 => /lib/x86_64-linux-gnux32/libntlm.so.0 (0xf6f13000)
        libgssglue.so.1 => /lib/x86_64-linux-gnux32/libgssglue.so.1 (0xf6f07000)
        libsasl2.so.2 => /lib/x86_64-linux-gnux32/libsasl2.so.2 (0xf6eec000)
        libbrotlicommon.so.1 => /lib/x86_64-linux-gnux32/libbrotlicommon.so.1 (0xf6ec9000)
        libp11-kit.so.0 => /lib/x86_64-linux-gnux32/libp11-kit.so.0 (0xf6d5c000)
        libtasn1.so.6 => /lib/x86_64-linux-gnux32/libtasn1.so.6 (0xf6d48000)
        libffi.so.8 => /lib/x86_64-linux-gnux32/libffi.so.8 (0xf6d3d000)

ej@a4:~/curl-curl-8_12_0$ libtool --mode=execute src/curl -V
curl 8.12.0-DEV (x86_64-pc-linux-gnux32) libcurl/8.12.0-DEV OpenSSL/3.4.0 zlib/1.3.1 brotli/1.1.0 zstd/1.5.6 libidn2/2.3.7 libpsl/0.21.2 nghttp2/1.64.0 librtmp/2.3 libgsasl/2.2.1 OpenLDAP/2.6.9
Release-Date: [unreleased]
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtmp rtsp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AsynchDNS brotli gsasl HSTS HTTP2 HTTPS-proxy IDN IPv6 Largefile libz NTLM PSL SSL threadsafe TLS-SRP UnixSockets zstd
```

Bisection points to
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `f72b84809216657e4ad3c1a0184775c911080d63` and the full history behind it is present.
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
