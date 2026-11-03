# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
build on windows failed "zephyr/scripts/Makefile.build:280: *** multiple target patterns."

**_Reported by Sharron LIU:_**
Build "zephyr/samples/hello_world" failed at windows/MSYS. 
```
$ pwd
/home/xianrong/zephyr/samples/hello_world
$ make BOARD=quark_d2000_crb

C:/msys64/home/xianrong/zephyr/scripts/Makefile.build:280: *** multiple target patterns.  Stop.
make[2]: *** [/home/xianrong/zephyr/arch/x86/Makefile.idt:32: C:/msys64/home/xianrong/zephyr/scripts/gen_idt/gen_idt] Error 2
make[2]: Leaving directory '/home/xianrong/zephyr/samples/hello_world/outdir/quark_d2000_crb'
make[1]: *** [Makefile:177: sub-make] Error 2
make[1]: Leaving directory '/home/xianrong/zephyr'
make: *** [C:/msys64/home/xianrong/zephyr/Makefile.inc:82: all] Error 2
```

how-to-reproduce
# setup windows build env at win10 https://www.zephyrproject.org/doc/getting_started/installation_win.html#using-msys2-recommended
# source zephyr-env.sh
# cd samples/hello_world
# make pristine
# make BOARD=quark_d2000_crb
# verify the build log

User impact:
blocking windows build validation for v1.8
(Imported from Jira ZEP-2140)

**_by Sharron LIU:_**
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `6c2eff60668b0538808af79a2a4bbb52d012ac79` and the full history behind it is present.
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
