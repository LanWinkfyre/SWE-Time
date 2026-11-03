# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
3DS `CONSOLE_LOG` is broken

## Description

I'm doing some tinkering with RetroArch on 3DS and I wanted to see the logs in the bottom screen. 

But the functionality can be restored:

> If you want to debug, you could build the project with the console enabled. For this, build with `CONSOLE_LOG` enabled in the makefile.

https://github.com/libretro/RetroArch/issues/12951#issuecomment-916045252

Unfortunately, this doesn't work as expected.

### Expected behavior

The bottom screen should show the RetroArch logs.

### Actual behavior

The log does briefly show in the bottom screen, and then the screen goes black again before I'm able to read it. Tapping on the bottom screen does nothing.

Going to _Settings_ > _User Interface_  and then toggling _3DS Bottom Screen_ off and then back on again makes the log show again, but once again it only shows briefly and then the screen goes blank.

### Steps to reproduce the bug

1. Set `CONSOLE_LOG             = 1` in Makefile.ctr (I did it in Makefile.ctr.salamander too just to be sure)
2. Compile RetroArch
3. Install the CIA file on a 3DS and observe the above behaviour

### Bisect Results





### Version/Commit
You can find this information under Information/System Information



### Environment information

- OS: 3DS
- Compiler: I'm compiling using the Docker devkitpro/devkitarm image + libretro-super

Thanks!
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `16c0f5e223b4022698481f1ea55391f8c3f7ace2` and the full history behind it is present.
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
