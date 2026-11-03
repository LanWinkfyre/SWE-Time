# Locate the commit that introduced this regression

A regression was reported against `darktable-org/darktable`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
**Describe the bug**
An icm profile with a long name cannot be found. Darktable reports on the command line:
[colorin] could not find requested profile `/home/foo/config/darktable/color/in/Nkx_D300_4139837_01_1_03_9_00_10_00_00_00_05_00_0400_0_0_32_47'!

You can observe that the filename is truncated and does not end with .icm. The complete filename is "Nkx_D300_4139837_01_1_03_9_00_10_00_00_00_05_00_0400_0_0_32_476_SD1.icm"

**To Reproduce**
Steps to reproduce the behavior:
1. place an icm profile in the color/in directory with the filename "Nkx_D300_4139837_01_1_03_9_00_10_00_00_00_05_00_0400_0_0_32_476_SD1.icm"
2. Try to apply the input color profile
3. Darktable reports on the commandline that the icm profile cannot be found. Note: The filename is truncated in the message.

**Expected behavior**
The icm profile is applied.

**Platform (please complete the following information):**
I have tried the master branch, darktable-2.6x and darktable-2.4x.

**Workaround**
If you shorten the filename darktable is able to apply the color profile without any issues.

**Additional**
I could attach the icm profile which was sent to me but I am not sure about the legal consequences (hence it is a profile extracted from a Nikon program for a Nikon D300). I can attach/send the file directly if this is necessary. I guess you can reproduce the issue on your system by copying one of your own icm profiles and make a long name.

**Commit that introduced the error**
I have bisect the code and found:
```

## What you have

- `/testbed/repo` is a git clone of `darktable-org/darktable` truncated just after the regression was
  reported.  `HEAD` is `e2188ea4b3a960ac98e72d485732a6255f62f984` and the full history behind it is present.
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
