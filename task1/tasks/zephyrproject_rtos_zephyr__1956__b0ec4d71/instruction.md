# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
"CONFIG_QMSI_LIBRARY=y" takes no effect

**_Reported by Sharron LIU:_**
Verify Zephyr kernel linkage to 3rd party lib "libqmsi" failed. 

NOTE: "CONFIG_QMSI_BUILTIN" works fine with this commit. 

how-to-reproduce
==============
The issue was detected with "sample/hello_world/nanokernel", with attached patch. To reproduce:
```
$ cd zephyr
$ source zephyr-env.sh
$ git apply test_qmsi_library.patch
$ cd samples/hello_world/nanokernel
$ make pristine
$ make BOARD=quark_se_devboard
$ vim outdir/.config
```

Verify "CONFIG_QMSI=y", "CONFIG_QMSI_LIBRARY=y", "CONFIG_QMSI_INSTALL_PATH" take no effect.

user impact
=========
user will not be able to use self-built libqmsi.
If Zephyr intent to do so, please remove "CONFIG_QMSI_LIBRARY" from "ext/hal/qmsi/Kconfig" to avoid confusion. thanks.

(Imported from Jira ZEP-402)
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `d6f950c918715fe8b4de499b2ffc772b2d524f54` and the full history behind it is present.
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
