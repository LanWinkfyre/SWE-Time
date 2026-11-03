# Locate the commit that introduced this regression

A regression was reported against `openssl/openssl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Using engine ciphers regression

Fetching ciphers from engine is broken since 






gost-engine grasshopper tests are failing with diagnostics

Encryption test for grasshopper ecb
00:52:A4:00:2D:7F:00:00:error:digital envelope routines:evp_generic_fetch:fetch failed:crypto/evp/evp_fetch.c:307:Default library context, Algorithm (kuznyechik-ecb), Properties ()
00:52:A4:00:2D:7F:00:00:error:digital envelope routines:EVP_CipherInit_ex:initialization error:crypto/evp/evp_enc.c:176:
/home/beldmit/upstream/engine/test_context.c:69: OpenSSL internal error: EVP_CipherInit_ex(ctx, type, NULL, K, iv, enc)

<!--
Thank you for your bug report. If this is your first one,
please take the time to read the following lines before posting it.

NOTE:

    If you're asking about how to use OpenSSL, this isn't the right 
    forum.  Please see our User Support resources:
    https://github.com/openssl/openssl/blob/master/.github/SUPPORT.md

Please remember to tell us in what OpenSSL version you found the issue.

For build issues:

    If this is a build issue, please include the configuration output
    as well as a log of all errors.  Don't forget to include the exact
    commands you typed.

    With OpenSSL before 1.1.1, the configuration output comes from the
    configuration command.  With OpenSSL 1.1.1 and on, it's the output
    of `perl configdata.pm --dump`

For other issues:

    If it isn't a build issue, example code or commands to reproduce
    the issue is highly appreciated.
    Also, please remember to tell us if you worked with your own
    OpenSSL build or if it is system provided.

Please remember to put ``` lines before and after any commands plus
output and code, like this:

    ```
    $ echo output output output
    output output output
    ```

    ```
    #include <stdio.h>
    
    int main() {
        int foo = 1;
        printf("%d\n", foo);
    }
    ```
-->
```

## What you have

- `/testbed/repo` is a git clone of `openssl/openssl` truncated just after the regression was
  reported.  `HEAD` is `73d6b4efe6835a6c97ce61df6bf339b0903e5b7a` and the full history behind it is present.
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
