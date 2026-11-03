# Locate the commit that introduced this regression

A regression was reported against `openssl/openssl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Configure: version number is missing from ENGINESDIR in Makefile

After configuring, the version number is missing from `ENGINESDIR` variable in the Makefile

```Makefile
ENGINESDIR=$(libdir)/engines-
```

As a consequence, OpenSSL is unable to find it's installed engines:

```
msp@msppc:~/src/openssl$ strace -f openssl rand -engine foo |& grep engine
execve("/opt/openssl-dev/bin/openssl", ["openssl", "rand", "-engine", "foo"], 0x7fff36c86fc0 /* 52 vars */) = 0
openat(AT_FDCWD, "/opt/openssl-dev/lib/engines-/foo.so", O_RDONLY|O_CLOEXEC) = -1 ENOENT (No such file or directory)
write(2, "invalid engine \"foo\"\n", 21invalid engine "foo"
...
```


### Analysis


The version number is missing because the `$sover_dirname` is not determined correctly by the configure script. 


For the fun of it and as an exercise, I wrote a little bisection script (my first one :-) ) which configures OpenSSL and checks the `ENGINESDIR` variable.

**engine-checker.sh**

```sh
#!/bin/bash

(make clean && rm Makefile && perl Configure debug-linux-x86_64) >/dev/null || (echo CONFIGURE FAILED ; exit 125)

if grep '^ENGINESDIR=.*/engines-[0-9.]\+' Makefile; then
	echo GOOD; exit 0
else
	echo BAD; exit 1
fi
```

If you want to try it out yourself, save it to your openssl source directory and make it executable:

```
~/src/openssl$  chmod +x engine-checker.sh
```

Now you can run a fully automated bisection:
```

## What you have

- `/testbed/repo` is a git clone of `openssl/openssl` truncated just after the regression was
  reported.  `HEAD` is `5cae2d349b561a84dbfc93d6b6abc5fb7263fb7c` and the full history behind it is present.
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
