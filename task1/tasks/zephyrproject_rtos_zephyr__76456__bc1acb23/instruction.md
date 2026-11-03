# Locate the commit that introduced this regression

A regression was reported against `zephyrproject-rtos/zephyr`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
tests: native_sim: modem_cmux build failure

**Describe the bug**


fails 

**To Reproduce**

`scripts/twister -p native_sim -T tests/subsys/modem/modem_cmux -s modem.modem_cmux --build-only
`


**Expected behavior**
build PASS

**Impact**

modem_mcux support

**Logs and console output**

'''
- Build files have been written to: /__w/zephyr/zephyr/twister-out/native_sim/tests/subsys/modem/modem_cmux/modem.modem_cmux
[1/110] Generating include/generated/zephyr/version.h
-- Zephyr version: 3.7.99 (/__w/zephyr/zephyr), build: v3.7.0-233-gc2070a090c70
[2/110] Preparing syscall dependency handling

[3/110] Generating misc/generated/syscalls_subdirs.trigger
[4/110] Generating misc/generated/syscalls.json, misc/generated/struct_tags.json
[5/110] Generating include/generated/zephyr/syscall_dispatch.c, include/generated/zephyr/syscall_list.h
[6/110] Generating include/generated/zephyr/driver-validation.h
[7/110] Generating include/generated/zephyr/kobj-types-enum.h, include/generated/zephyr/otype-to-str.h, include/generated/zephyr/otype-to-size.h
[8/110] Building C object zephyr/CMakeFiles/offsets.dir/arch/posix/core/offsets/offsets.c.obj
[9/110] Generating include/generated/zephyr/offsets.h
[10/110] Building C object CMakeFiles/app.dir/src/main.c.obj
FAILED: CMakeFiles/app.dir/src/main.c.obj 
ccache /usr/lib/llvm-16/bin/clang -DKERNEL -DK_HEAP_MEM_POOL_SIZE=0 -DTC_RUNID=6aa275a52394d71b47eca3af1273f500 -D__ZEPHYR__=1 -I/__w/zephyr/zephyr/tests/subsys/modem/modem_cmux/../mock -I/__w/zephyr/zephyr/twister-out/native_sim/tests/subsys/modem/modem_cmux/modem.modem_cmux/zephyr/include/generated/zephyr -I/__w/zephyr/zephyr/include -I/__w/zephyr/zephyr/twister-out/native_sim/tests/subsys/modem/modem_cmux/modem.modem_cmux/zephyr/include/generated -I/__w/zephyr/zephyr/soc/native/inf_clock -I/__w/zephyr/zephyr/boards/native/native_sim -I/__w/zephyr/zephyr/scripts/native_simulator/common/src/include -I/__w/zephyr/zephyr/scripts/native_simulator/native/src/include -I/__w/zephyr/zephyr/subsys/testsuite/include -I/__w/zephyr/zephyr/subsys/testsuite/coverage -I/__w/zephyr/zephyr/subsys/testsuite/ztest/include -fno-strict-aliasing -Werror -O0 -imacros /__w/zephyr/zephyr/twister-out/native_sim/tests/subsys/modem/modem_cmux/modem.modem_cmux/zephyr/include/generated/zephyr/autoconf.h -fno-common -g -gdwarf-4 -fcolor-diagnostics --config /__w/zephyr/zephyr/cmake/toolchain/llvm/clang_libgcc.cfg -Wall -Wformat -Wformat-security -Wno-format-zero-length -Wno-unused-but-set-variable -Wno-typedef-redefinition -Wno-deprecated-non-prototype -Wdouble-promotion -Wno-pointer-sign -Wpointer-arith -Wno-sometimes-uninitialized -Wno-shift-overflow -Wno-missing-braces -Wno-self-assign -Wno-address-of-packed-member -Wno-unused-function -Wno-initializer-overrides -Wno-section -Wno-unknown-warning-option -Wno-unused-variable -Wno-format-invalid-specifier -Wno-gnu -Wno-tautological-compare -Werror=implicit-int -fno-pic -fno-pie -fno-asynchronous-unwind-tables -Wno-vla -fmacro-prefix-map=/__w/zephyr/zephyr/tests/subsys/modem/modem_cmux=CMAKE_SOURCE_DIR -fmacro-prefix-map=/__w/zephyr/zephyr=ZEPHYR_BASE -fmacro-prefix-map=/__w/zephyr=WEST_TOPDIR -ffunction-sections -fdata-sections -m32 -msse2 -mfpmath=sse -fvisibility=hidden -std=c11 -MD -MT CMakeFiles/app.dir/src/main.c.obj -MF CMakeFiles/app.dir/src/main.c.obj.d -o CMakeFiles/app.dir/src/main.c.obj -c /__w/zephyr/zephyr/tests/subsys/modem/modem_cmux/src/main.c
/__w/zephyr/zephyr/tests/subsys/modem/modem_cmux/src/main.c:796:28: error: too few arguments to function call, expected 2, have 1
        modem_pipe_open(dlci1_pipe);
        ~~~~~~~~~~~~~~~           ^
/__w/zephyr/zephyr/include/zephyr/modem/pipe.h:99:5: note: 'modem_pipe_open' declared here
int modem_pipe_open(struct modem_pipe *pipe, k_timeout_t timeout);
    ^
/__w/zephyr/zephyr/tests/subsys/modem/modem_cmux/src/main.c:797:28: error: too few arguments to function call, expected 2, have 1
        modem_pipe_open(dlci2_pipe);
        ~~~~~~~~~~~~~~~           ^
/__w/zephyr/zephyr/include/zephyr/modem/pipe.h:99:5: note: 'modem_pipe_open' declared here
int modem_pipe_open(struct modem_pipe *pipe, k_timeout_t timeout);
    ^
/__w/zephyr/zephyr/tests/subsys/modem/modem_cmux/src/main.c:802:29: error: too few arguments to function call, expected 2, have 1
        modem_pipe_close(dlci1_pipe);
        ~~~~~~~~~~~~~~~~           ^
/__w/zephyr/zephyr/include/zephyr/modem/pipe.h:176:5: note: 'modem_pipe_close' declared here
int modem_pipe_close(struct modem_pipe *pipe, k_timeout_t timeout);
    ^
/__w/zephyr/zephyr/tests/subsys/modem/modem_cmux/src/main.c:803:29: error: too few arguments to function call, expected 2, have 1
        modem_pipe_close(dlci2_pipe);
        ~~~~~~~~~~~~~~~~           ^
/__w/zephyr/zephyr/include/zephyr/modem/pipe.h:176:5: note: 'modem_pipe_close' declared here
int modem_pipe_close(struct modem_pipe *pipe, k_timeout_t timeout);
    ^
/__w/zephyr/zephyr/tests/subsys/modem/modem_cmux/src/main.c:812:39: error: too few arguments to function call, expected 2, have 1
        zassert_ok(modem_pipe_open(dlci1_pipe));
                   ~~~~~~~~~~~~~~~           ^
/__w/zephyr/zephyr/subsys/testsuite/ztest/include/zephyr/ztest_assert.h:283:41: note: expanded from macro 'zassert_ok'
#define zassert_ok(cond, ...) zassert(!(cond), #cond " is non-zero", ##__VA_ARGS__)
                                        ^~~~
/__w/zephyr/zephyr/subsys/testsuite/ztest/include/zephyr/ztest_assert.h:189:14: note: expanded from macro 'zassert'
        _zassert_va(cond, default_msg, COND_CODE_1(__VA_OPT__(1), (__VA_ARGS__), (NULL)))
                    ^~~~
/__w/zephyr/zephyr/subsys/testsuite/ztest/include/zephyr/ztest_assert.h:186:16: note: expanded from macro '_zassert_va'
        _zassert_base(cond, default_msg, msg, ##__VA_ARGS__)
                      ^~~~
/__w/zephyr/zephyr/subsys/testsuite/ztest/include/zephyr/ztest_assert.h:175:25: note: expanded from macro '_zassert_base'
                bool _ret = z_zassert(cond, _msg ? ("(" default_msg ")") : (default_msg), __FILE__,\
                                      ^~~~
/__w/zephyr/zephyr/include/zephyr/modem/pipe.h:99:5: note: 'modem_pipe_open' declared here
int modem_pipe_open(struct modem_pipe *pipe, k_timeout_t timeout);
    ^
/__w/zephyr/zephyr/tests/subsys/modem/modem_cmux/src/main.c:814:39: error: too few arguments to function call, expected 2, have 1
        zassert_ok(modem_pipe_open(dlci2_pipe));
                   ~~~~~~~~~~~~~~~           ^
/__w/zephyr/zephyr/subsys/testsuite/ztest/include/zephyr/ztest_assert.h:283:41: note: expanded from macro 'zassert_ok'
#define zassert_ok(cond, ...) zassert(!(cond), #cond " is non-zero", ##__VA_ARGS__)
                                        ^~~~
/__w/zephyr/zephyr/subsys/testsuite/ztest/include/zephyr/ztest_assert.h:189:14: note: expanded from macro 'zassert'
        _zassert_va(cond, default_msg, COND_CODE_1(__VA_OPT__(1), (__VA_ARGS__), (NULL)))
                    ^~~~
/__w/zephyr/zephyr/subsys/testsuite/ztest/include/zephyr/ztest_assert.h:186:16: note: expanded from macro '_zassert_va'
        _zassert_base(cond, default_msg, msg, ##__VA_ARGS__)
                      ^~~~
/__w/zephyr/zephyr/subsys/testsuite/ztest/include/zephyr/ztest_assert.h:175:25: note: expanded from macro '_zassert_base'
                bool _ret = z_zassert(cond, _msg ? ("(" default_msg ")") : (default_msg), __FILE__,\
                                      ^~~~
/__w/zephyr/zephyr/include/zephyr/modem/pipe.h:99:5: note: 'modem_pipe_open' declared here
int modem_pipe_open(struct modem_pipe *pipe, k_timeout_t timeout);
    ^
6 errors generated.
ninja: build stopped: subcommand failed.
'''



**Environment (please complete the following information):**

 - OS: (e.g. Linux,, )
 - Toolchain (e.g Zephyr SDK, ...)


**Additional context**
```

## What you have

- `/testbed/repo` is a git clone of `zephyrproject-rtos/zephyr` truncated just after the regression was
  reported.  `HEAD` is `3bcaa6f8d63136ffc2ae37b6e77ee4e1cda6964f` and the full history behind it is present.
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
