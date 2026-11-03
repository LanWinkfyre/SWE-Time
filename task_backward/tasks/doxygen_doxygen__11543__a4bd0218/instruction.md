# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Doxygen V.1.14 is very slow

Due to issue #11310 Doxygen Version 1.13.x is not suitable for me and thus I'm further using V.1.12.

But since the issue is "fixed but not released" I've tried to use the actual master/Version 1.14 from build [5429](https://github.com/doxygen/doxygen/actions/runs/14342216437) and there is a strange behavior:

 runnig again without any changes (i.e. without deleting the html directory) takes about **1 minute**.
I think the difference is from graphviz building all the images only at the first run, and so its ok.



Some observations:
After starting Doxygen nothing seems to happen for about 40 minutes though Doxygen utilizes my 4core/8thread machine with about 15%-20% (at a total CPU usage of about 35% due to other processes). At the end then normal Doxygen messages are output (taking about 4 minutes) and Doxygen ends normally.
It seems that Doxoygen first does lots of preparing work without any output and after that normally creates the documentation.



OS: Windows 10
Doxygen: Release-Builds of the above versions 

Regards from Meerbusch
Thomas


Hi @thom-sch. Thanks for reporting. There is definitely something wrong if there are 40 minutes of additional run time. Unfortunately, there is not too much info in your report that actually helps us to reproduce the issue.

Assuming you cannot share the source code, there are some things that may help us.

- which step (when running with QUIET=NO) is Doxygen executing when it halts for 40 minutes?
- could you try a debug build and attach a debugger to the running process (or launch Doxygen from the debugger) and dump the stack at various points during this 40 minute of "silence". Then we know where in the code Doxygen gets "stuck".
- Can you reduce the size of the project while keeping the same behavior? Maybe that can pinpoint to what triggers the behavior.
- You mentioned that build 5223 has similar behavior. I assume you mean it has the "40 minutes" problem. And the only version you can try that doesn't have the problem is 1.12? Is there any way you get 1.13 to work (even if not perfect) so we at least know if it has the problem or not?



@thom-sch Thanks for the example, very useful.

A bisection gave:
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `1ca6d10fd6930d8cd062dce36985433cd90b3e74` and the full history behind it is present.
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
