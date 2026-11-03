# Locate the commit that introduced this regression

A regression was reported against `nodejs/node`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
dns.lookup('localhost', { all: true}) returns only ::1 with Node.js v22.12, while v22.11 returned both ::1 and 127.0.0.1

### Version

v22.12.0

### Platform

```text
Windows 11 (Microsoft Windows NT 10.0.26100.0 x64)
```


### Subsystem

dns

### What steps will reproduce the bug?

On my Windows 11 system, the `localhost` hostname resolves to both `::1` and `127.0.0.1`, as confirmed by PowerShell `Resolve-DnsName`:

```PowerShell
PS> Resolve-DnsName localhost
Name             Type   TTL   Section    IPAddress
----             ----   ---   -------    ---------
localhost        AAAA   1200  Question   ::1
localhost        A      1200  Question   127.0.0.1
```

And with Node.js v22.11 (and v20, and v18), both addresses are returned by a DNS lookup, as expected:

```PowerShell
PS> node -v
v22.11.0
PS> node -e "require('dns').lookup('localhost', {all: true}, (err, addresses) => console.log(JSON.stringify(addresses, null, '  ')))"
[
  {
    "address": "::1",
    "family": 6
  },
  {
    "address": "127.0.0.1",
    "family": 4
  }
]
```

However with Node.js v22.12, only `::1` is returned:

```PowerShell
PS> node -v
v22.12.0
PS> node -e "require('dns').lookup('localhost', {all: true}, (err, addresses) => console.log(JSON.stringify(addresses, null, '  ')))"
[
  {
    "address": "::1",
    "family": 6
  }
]
```

### How often does it reproduce? Is there a required condition?

It repros consistently on Windows.

I do not see the same problem on Linux: after editing `/etc/hosts` to include dual mappings for `localhost`, I do see both addresses returned from the Node.js DNS lookup, and it is consistent between Node.js v22.11 and v22.12.

### What is the expected behavior? Why is that the expected behavior?

I found this bug because we have some Node.js test code that needs to connect to a port on localhost without knowing whether the local server is listening on the IPv4 or IPv6 localhost. It actually uses `net.createConection({..., autoSelectFamily: true })`, but the problem seems to be with the DNS resolution before the "happy eyeballs" algorithm gets a chance to auto-select an address family. Because only ::1 is tried, the connection fails if the local server was actually listening on IPv4.

### What do you see instead?

```
Error: connect ECONNREFUSED ::1:51793
```

...when the server was actually listening on `127.0.0.1:51793`

### Additional information

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `nodejs/node` truncated just after the regression was
  reported.  `HEAD` is `c4aa34aa4dc5accb100be07b4aceded83eeb3956` and the full history behind it is present.
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
