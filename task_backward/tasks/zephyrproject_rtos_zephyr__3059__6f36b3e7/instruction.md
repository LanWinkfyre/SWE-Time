# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
"samples/philosophers" build failed unexpectedly @quark_d2000  "section `noinit' will not fit in region `RAM'"

**_Reported by Sharron LIU:_**
"samples/philosophers" build failed @quark_d2000. 




build failure:
```
/opt/zephyr-sdk/sysroots/i686-pokysdk-linux/usr/bin/iamcu-poky-elfiamcu/../../libexec/iamcu-poky-elfiamcu/gcc/i586-poky-elfiamcu/5.2.1/real-ld: zephyr_prebuilt.elf section `noinit' will not fit in region `RAM'
/opt/zephyr-sdk/sysroots/i686-pokysdk-linux/usr/bin/iamcu-poky-elfiamcu/../../libexec/iamcu-poky-elfiamcu/gcc/i586-poky-elfiamcu/5.2.1/real-ld: region `RAM' overflowed by 936 bytes
collect2: error: ld returned 1 exit status
make[2]: *** [zephyr_prebuilt.elf] Error 1
make[2]: Leaving directory `/home/sharron/workspace/views/iot/zephyr/samples/philosophers/outdir/quark_d2000_crb'
```
(Imported from Jira ZEP-1598)
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `916837c22ca8050417a6dd4503b991a8a74aafdd` and the full history behind it is present.
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
