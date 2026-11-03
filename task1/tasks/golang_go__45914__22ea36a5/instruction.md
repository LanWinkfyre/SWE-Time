# Locate the commit that introduced this regression

A regression was reported against `golang/go`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
os: ERROR_NO_SYSTEM_RESOURCES when making child process use os.Stdout on Windows 7

### What version of Go are you using (`go version`)?



### Does this issue reproduce with the latest release?
~~Yes.~~ (Actually, no, this is a new regression, see below.)


### What operating system and processor architecture are you using (`go env`)?

The windows program is cross compiled from linux/amd64 to windows/amd64.
The windows version is Windows 7 (version 6.1.7601), vanilla installation.

### What did you do?
The following command tries to execute `cmd /c echo abc` and let the child process use `os.Stdout`.
If there is no command line argument, it will simply set `cmd.Stdout = os.Stdout`;
otherwise, it will create a goroutine to copy `cmd.StdoutPipe()` to `os.Stdout`.
https://play.golang.org/p/rzblvBHqLb2
```
package main

import (
	"io"
	"log"
	"os"
	"os/exec"
)

func main() {
	cmd := exec.Command("cmd", "/c", "echo", "abc")
	if len(os.Args) == 1 {
		println("bug")
		cmd.Stdout = os.Stdout
	} else {
		println("io.Copy")
		outpipe, err := cmd.StdoutPipe()
		if err != nil {
			log.Fatal(err)
		}
		defer outpipe.Close()
		go io.Copy(os.Stdout, outpipe)
	}
	err := cmd.Run()
	if err != nil {
		log.Fatal(err)
	}
}
``` 

### What did you expect to see?

```
C:\> test.exe
bug
abc

C:\> test.exe test
io.Copy
abc
```

### What did you see instead?

```
C:\> test.exe
bug
2021/05/02 00:01:02 fork/exec c:\windows\system32\cmd.exe: Insufficient system resources exist to complete the requested service.

C:\> test.exe test
io.Copy
abc
```

This problem reproduces every time, even when the system is freshly rebooted, so error message is likely bogus.
Also, this bug also applies to other command line programs, and it's not specific to `cmd.exe`.

Debugging revealed that the error is returned by `CreateProcessW`, and some (e.g. https://github.com/rprichard/win32-console-docs/issues/6) mentions that "CreateProcessW fails with ERROR_NO_SYSTEM_RESOURCES when used with EXTENDED_STARTUPINFO_PRESENT and an attempt is made to restrict the inherited handles. The problem appears only on Win7 OS as in your tests."


Actually, this is a new regression, sorry I didn't check the latest release before filing the issue.



/cc @zx2c4 @alexbrainman
```

## What you have

- `/testbed/repo` is a git clone of `golang/go` truncated just after the regression was
  reported.  `HEAD` is `abb110bf3de82f85aefe0fb284cc9359488b5f09` and the full history behind it is present.
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
