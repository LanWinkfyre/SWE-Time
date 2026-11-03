# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
tests:  lpcxpresso55s69/lpc55s69/cpu0/ns: drivers.flash.common.tfm_ns: Build failure

**Describe the bug**
tests/drivers/flash/common build failure

Please also mention any information which could help others to understand
the problem you're facing:
 - What target platform are you using?
lpcxpresso55s69/lpc55s69/cpu0/ns
lpcxpresso55s69/lpc55s69/cpu1
 - What have you tried to diagnose or workaround this issue?
 git bisect
 - Is this a regression? If yes, have you been able to "git bisect" it to a
   specific commit?
 



<html>
<body>

CASE_NAME | ZEPHYR_VERSION | RESULT | PLATFORM | TEST_PATH
-- | -- | -- | -- | --
drivers.flash.common.default | v3.7.0-rc1 | Build failure | lpcxpresso55s69/lpc55s69/cpu1 | tests/drivers/flash/common
sample.drivers.flash.shell | v3.7.0-rc1 | Build failure | lpcxpresso55s69/lpc55s69/cpu1 | samples/drivers/flash_shell

</body>
</html>

**To Reproduce**
Steps to reproduce the behavior:

scripts/twister -p lpcxpresso55s69/lpc55s69/cpu0/ns -T tests/drivers/flash/common -s drivers.flash.common.tfm_ns

**Expected behavior**
Build PASS

**Impact**

flash support for this platform

**Logs and console output**

```
CMakeFiles/app.dir/src/main.c.obj -c /home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/tests/drivers/flash/common/src/main.c
/home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/tests/drivers/flash/common/src/main.c:49:2: error: #error There is no flash device enabled or it is missing Kconfig options
   49 | #error There is no flash device enabled or it is missing Kconfig options
      |  ^~~~~
In file included from /home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/include/zephyr/toolchain/gcc.h:98,
                 from /home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/include/zephyr/toolchain.h:50,
                 from /home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/include/zephyr/kernel_includes.h:23,
                 from /home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/include/zephyr/kernel.h:17,
                 from /home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/tests/drivers/flash/common/src/main.c:7:
/home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/include/zephyr/device.h:92:41: error: '__device_dts_ord_65' undeclared here (not in a function); did you mean '__device_dts_ord_15'?
   92 | #define DEVICE_NAME_GET(dev_id) _CONCAT(__device_, dev_id)
      |                                         ^~~~~~~~~
```

**Environment (please complete the following information):**
 - OS: (e.g. Linux)
 - Toolchain (e.g Zephyr SDK, ...)
 - Commit SHA or Version used:  v3.7.0-rc1
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `4d0a8c1e8b8316ec5071a3fcc98cd292d3bc4e6d` and the full history behind it is present.
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
