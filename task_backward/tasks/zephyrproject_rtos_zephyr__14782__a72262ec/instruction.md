# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Build process produces hex files which will not install on BBC micro:bit

**Describe the bug**
Building for BBC micro:bit against v1.14.0-rc2 I found that often (but not always) the resultant hex file would not copy onto the device over USB. micro:bit is an mbed device and flashing involves copying the binary hex file to a target USB drive. Copying would fail like this:

C:\workspaces\zephyr_projects\peripheral_hr\build>copy zephyr\zephyr.hex d:
The system cannot find the file specified.
        0 file(s) copied.

and the mbed USB drive would disconnect. Physically unplugging the USB cable and plugging it in again would bring back the mbed drive.

The hello_world sample project builds and installs OK.

The bluetooth/peripheral_hr project exhibits the problem.

**To Reproduce**
Steps to reproduce the behavior:

1. Check out tag 
2. Set up the bluetooth/peripheral_hr project for BBC micro:bit with

cmake -GNinja -DBOARD=bbc_microbit ..

3. Build with

ninja

4. Attempt to install to a USB connected micro:bit (assuming assigned drive letter is D: on Windows)

copy zephyr\zephyr.hex d:

**Expected behavior**

The hex file should successfuly copy to the mbed drive and the mbed drive should stay connected to the host computer:

C:\workspaces\zephyr_projects\peripheral_hr\build>copy zephyr\zephyr.hex d:
        1 file(s) copied.

Instead, this happens:

C:\workspaces\zephyr_projects\peripheral_hr\build>copy zephyr\zephyr.hex d:
The system cannot find the file specified.
        0 file(s) copied.

**Impact**
Have to work with 1.14.0-rc1. Showstopper for 1.14.0 if this is not fixed though.

**Screenshots or console output**

**Environment (please complete the following information):**
 - OS: Windows
 - Toolchain: Zephyr 1.14.0-rc2 with ninja
 - Commit SHA or Version used

I used git bisect and determined that the following commit is probably where the problem was introduced:





**Additional context**

It's been pointed out to me that this commit has relevance:
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `3ebd9b4a09dcf26ec689c3a2ae9eb241201cd1ef` and the full history behind it is present.
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
