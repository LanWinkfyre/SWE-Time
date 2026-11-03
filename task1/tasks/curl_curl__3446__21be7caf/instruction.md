# Locate the commit that introduced this regression

A regression was reported against `curl/curl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
7.64 regression: curl_multi_fdset() returns a write fd instead of read fd

This is a complicated issue so bear with me.

__update__: see here for the test program: https://github.com/curl/curl/issues/3446#issuecomment-452369484

## Summary
I have a unit test that __`CURLMOPT_MAX_TOTAL_CONNECTIONS`__ and __`CURLMOPT_MAX_HOST_CONNECTIONS`__ work as expected, by making a bunch of request and inspecting __`curl_multi_fdset()`__ throughout.

## What the test does

 1. Create a multi handle and set __`CURLMOPT_MAX_TOTAL_CONNECTIONS = 4`__ and  __`CURLMOPT_PIPELINING = CURLPIPE_NOTHING`__. (we disable multiplexing for this test).
3. Add a bunch of requests. My unit test uses `"https://eu.httpbin.org/delay/" + x` where `x` equals `[4,3,2,1,0,1,2,3,4]` (so 9 request in total). 
4. Repeatedly call `curl_multi_perform()`. Every time a request has finished (`CURLMSG_DONE`) do:
    1. Call `curl_multi_fdset()` and read `read_fd_set` to get the open connections.
    2. The number of fd's in `read_fd_set` must be equal to `MIN(CURLMOPT_MAX_TOTAL_CONNECTIONS, running_handles)` where `running_handles` is the number of pending connections returned by `curl_multi_perform()`. 

So basically we test that at any given point, the number of open connections (read fd's) is never more than `CURLMOPT_MAX_TOTAL_CONNECTIONS` or the number of outstanding requests. 

The test passed for many versions up and till version 7.63 (so even after http/2 is enabled by default) but fails in `7.64.0-DEV` (master). 


## Previous behavior

At each of the 9 checks, the fd count in `write_fd_set` is 0 and the fd count in `read_fd_set` is equal to `min(4, running_handles)`.

## In master

At the first check we expect the fd count in `read_fd_set` to be 4. However instead, it is only 3, but now we also have 1 fd in `write_fd_set` ?!



OK this is what git bisect says:
```

## What you have

- `/testbed/repo` is a git clone of `curl/curl` truncated just after the regression was
  reported.  `HEAD` is `dea3f94298ac0859464768959488938c4e104545` and the full history behind it is present.
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
