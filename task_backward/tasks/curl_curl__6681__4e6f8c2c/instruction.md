# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
CURLE_OUT_OF_MEMORY when adding large header after update to 7.71.0

### I did this
An application I'm working on uses `libcurl` to make HTTP requests to a server and uses the following code pattern to make this request:
```
    // setup
    curl_easy_reset(m_curl_handle);
    curl_easy_setopt(m_curl_handle, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
    curl_easy_setopt(m_curl_handle, CURLOPT_TIMEOUT, 0L);
    curl_easy_setopt(m_curl_handle, CURLOPT_CONNECTTIMEOUT, 1L);
    curl_easy_setopt(m_curl_handle, CURLOPT_NOSIGNAL, 1L);
    curl_easy_setopt(m_curl_handle, CURLOPT_TCP_NODELAY, 1L);
    curl_easy_setopt(m_curl_handle, CURLOPT_POST, 1L);
    curl_easy_setopt(m_curl_handle, CURLOPT_READFUNCTION, read_data); 
    curl_easy_setopt(m_curl_handle, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(m_curl_handle, CURLOPT_HEADERFUNCTION, write_header);
    curl_easy_setopt(m_curl_handle, CURLOPT_PROXY, "");
    curl_easy_setopt(m_curl_handle, CURLOPT_URL, url.c_str());

    curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "content-type: text/html");
    headers = curl_slist_append(headers, ("large-header: " + up_to_1mb_string).c_str());

    std::pair<std::string const&, size_t> ctx{payload, 0};
    aws::http::response resp;
    curl_easy_setopt(m_curl_handle, CURLOPT_WRITEDATA, &resp);
    curl_easy_setopt(m_curl_handle, CURLOPT_HEADERDATA, &resp);
    curl_easy_setopt(m_curl_handle, CURLOPT_READDATA, &ctx);
    curl_easy_setopt(m_curl_handle, CURLOPT_HTTPHEADER, headers);
    CURLcode curl_code = curl_easy_perform(m_curl_handle);

    curl_slist_free_all(headers);

    if (curl_code != CURLE_OK) {
        // log error
    }
```

We compile curl from source with:
```
 ./configure \
        --prefix $INSTALL_PREFIX \
        --disable-shared \
        --enable-debug \ # added to debug this issue (logs below)
        --without-ssl \
        --with-pic \
        --without-zlib && \
    make && \
    make install
```

Execution logs:
```
[DEBUG] [1614694131840] CURL DBG: STATE: INIT => CONNECT handle 0x14e9728; line 1771 (connection #-5000)
[DEBUG] [1614694131840] CURL DBG: Found bundle for host 127.0.0.1: 0x14f82b8 [serially]
[DEBUG] [1614694131840] CURL DBG: Re-using existing connection! (#0) with host 127.0.0.1
[DEBUG] [1614694131840] CURL DBG: Connected to 127.0.0.1 (127.0.0.1) port 9001 (#0)
[DEBUG] [1614694131840] CURL DBG: STATE: CONNECT => DO handle 0x14e9728; line 1825 (connection #0)
[DEBUG] [1614694131846] CURL DBG: multi_done
[DEBUG] [1614694131846] CURL DBG: Connection #0 to host 127.0.0.1 left intact
[DEBUG] [1614694131846] CURL DBG: Expire cleared (transfer 0x14e9728)
[DEBUG] [1614694131846] CURL returned error code 27 - Out of memory
```

### I expected the following
Before version 7.71.0 (tested up to 7.75.0), this worked fine for headers with size up to 1mb but after the update I've started seeing `CURLE_OUT_OF_MEMORY`.
 Have not confirmed this however.

### curl/libcurl version
7.71.0+

### operating system
Amazon Linux 2

```
$ uname -a
Linux 331a706e46ef 4.19.121-linuxkit #1 SMP Tue Dec 1 17:50:32 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

-----

I'd really appreciate guidance on this, thanks!



repro:
~~~
(printf "my-header-key-name-with-forty-characters: "; printf 'A%.0s' {1..300000}; printf "B") > testhdr.txt
curl -v -H @testhdr.txt http://httpbin.org/get
~~~
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `cc9bf974cd8dc53fbb24d6f7a6dc558c71bff5bd` and the full history behind it is present.
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
