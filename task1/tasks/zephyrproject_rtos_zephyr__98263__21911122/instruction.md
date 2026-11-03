# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
tests: drivers: counter: frdm_imx91/mimx9131 counter test build failure

### Describe the bug

- frdm_imx91/mimx9131





### Regression

- [x] This is a regression.

### Steps to reproduce

```
west build -b frdm_imx91/mimx9131 tests/drivers/counter
``

### Relevant log output

```shell
[82/169] Building C object zephyr/subsys/testsuite/ztest/CMakeFiles/subsys__testsuite__ztest.dir/src/ztest_rules.c.obj[83/169] Building C object zephyr/subsys/testsuite/ztest/CMakeFiles/subsys__testsuite__ztest.dir/src/ztest_defaults.c.obj
[84/169] Linking C static library zephyr/subsys/testsuite/ztest/libsubsys__testsuite__ztest.a
[85/169] Building C object zephyr/drivers/interrupt_controller/CMakeFiles/drivers__interrupt_controller.dir/intc_gicv3.c.obj[86/169] Linking C static library zephyr/drivers/interrupt_controller/libdrivers__interrupt_controller.a
[87/169] Building C object zephyr/drivers/cache/CMakeFiles/drivers__cache.dir/cache_handlers.c.obj
[88/169] Linking C static library zephyr/drivers/cache/libdrivers__cache.a
[89/169] Building C object zephyr/drivers/clock_control/CMakeFiles/drivers__clock_control.dir/clock_control_mcux_ccm_rev2.c.obj[90/169] Linking C static library zephyr/drivers/clock_control/libdrivers__clock_control.a
[91/169] Building C object zephyr/drivers/console/CMakeFiles/drivers__console.dir/uart_console.c.obj
[92/169] Linking C static library zephyr/drivers/console/libdrivers__console.a
[93/169] Building C object zephyr/drivers/counter/CMakeFiles/drivers__counter.dir/counter_mcux_tpm.c.objFAILED: zephyr/drivers/counter/CMakeFiles/drivers__counter.dir/counter_mcux_tpm.c.obj -Wexpansion-to-defined -Wno-unused-but-set-variable -Werror=implicit-int -fno-pic -fno-pie -fno-asynchronous-unwind-tables -ftls-model=local-exec -fno-reorder-functions --param=min-pagesize=0 -fno-defer-pop -fmacro-prefix-map=/home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/tests/drivers/counter/counter_basic_api=CMAKE_SOURCE_DIR -fmacro-prefix-map=/home/jenkins/agent/workspace/bitbucket_build_platform/zephyr=ZEPHYR_BASE -fmacro-prefix-map=/home/jenkins/agent/workspace/bitbucket_build_platform=WEST_TOPDIR -ffunction-sections -fdata-sections -mno-outline-atomics -moverride=tune=no_ldp_stp_qregs -specs=picolibc.specs -Wno-misleading-indentation -std=c99 -MD -MT zephyr/drivers/counter/CMakeFiles/drivers__counter.dir/counter_mcux_tpm.c.obj -MF zephyr/drivers/counter/CMakeFiles/drivers__counter.dir/counter_mcux_tpm.c.obj.d -o zephyr/drivers/counter/CMakeFiles/drivers__counter.dir/counter_mcux_tpm.c.obj -c /home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/drivers/counter/counter_mcux_tpm.c/home/jenkins/agent/workspace/bitbucket_build_platform/zephyr/drivers/counter/counter_mcux_tpm.c:44:47: 
error: 'TPM_CONTROLS_COUNT' undeclared here (not in a function); did you mean 'TPM_CNT_COUNT'? 
44 | struct mcux_tpm_channel_data channels[TPM_CONTROLS_COUNT]; 
   | ^~~~~~~~~~~~~~~~~~ | TPM_CNT_COUNTninja: build stopped: subcommand failed.
```

### Impact

Annoyance – Minor irritation; no significant impact on usability or functionality.

### Environment

- os: ubuntu
- toolchain: zephyr


### Additional Context

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `433893e54b9ca7e70d6f158690839b56913d5dce` and the full history behind it is present.
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
