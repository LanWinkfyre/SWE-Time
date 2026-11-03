# Locate the commit that introduced this regression

A regression was reported against `nodejs/node`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test-net-connect-options-ipv6 takes way to long on OS X



```
=== release test-net-connect-options-ipv6 ===                                  
Path: parallel/test-net-connect-options-ipv6
Command: out/Release/node /Users/Jeremiah/Documents/node/test/parallel/test-net-connect-options-ipv6.js
--- TIMEOUT ---
[01:24|% 100|+ 998|-   1]: Done                            
make: *** [test] Error 1
```



cc @trott / @mscdex?
```

## What you have

- `/testbed/repo` is a git clone of `nodejs/node` truncated just after the regression was
  reported.  `HEAD` is `cc82e5e3d9aefb5e31dbe688b0038327bb7d9b80` and the full history behind it is present.
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
