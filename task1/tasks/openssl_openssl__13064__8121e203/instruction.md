# Locate the commit that introduced this regression

A regression was reported against `openssl/openssl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
chacha20 seems to be broken in OpenSSL 3.0.0alpha6

When using OpenSSL 3.0.0alpha6, OpenSSH versions > 8.2p1 fail to connect anywhere, usually resulting in a "protocol error" while establishing the connection.

Bisecting OpenSSH shows this commit is what triggers the breakage:


Defining HAVE_BROKEN_CHACHA20 in openbsd-compat/openssl-compat.h (like the openssh commit does for some versions of LibreSSL) "fixes" the problem.

Looks like EVP_chacha20 doesn't work as expected by OpenSSH.
```

## What you have

- `/testbed/repo` is a git clone of `openssl/openssl` truncated just after the regression was
  reported.  `HEAD` is `62f27ab9dcf29876b15cdae704c3a04b4c8a6344` and the full history behind it is present.
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
