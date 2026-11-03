# Locate the commit that introduced this regression

A regression was reported against `openssl/openssl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Invalid relocation with libcrypto.a on armeabi-v7a

Scenario: building a shared library linking statically to `libcrypto.a`
Target platform: Android on 32-bit ARM (ARMv7-A). This issue is not observed on 64-bit ARM (AArch64).

Build Step Failing with Relocation Error
When building the shared object, the following linker error occurs (paths redacted):
```
$ANDROID_NDK/toolchains/llvm/prebuilt/darwin-x86_64/bin/clang++ --target=armv7-none-linux-androideabi27 --sysroot=$ANDROID_NDK/toolchains/llvm/prebuilt/darwin-x86_64/sysroot -fPIC -g -DANDROID -fdata-sections -ffunction-sections -funwind-tables -fstack-protector-strong -no-canonical-prefixes -D_FORTIFY_SOURCE=2 -march=armv7-a -mthumb -Wformat -Werror=format-security   -fno-limit-debug-info  -static-libstdc++ -Wl,--build-id=sha1 -Wl,--no-rosegment -Wl,--no-undefined-version -Wl,--fatal-warnings -Wl,--no-undefined -Qunused-arguments -shared -Wl,-soname,$TARGET_LIB_NAME.so -o $TARGET_LIB_PATH $TARGET_SOURCES  -landroid  -llog  _deps/openssl-src/libcrypto.a  -ldl  -pthread  -latomic -lm && :
  ld.lld: error: relocation R_ARM_REL32 cannot be used against symbol 'OPENSSL_armcap_P'; recompile with -fPIC
  >>> defined in _deps/openssl-src/libcrypto.a(libcrypto-lib-armcap.o)
  >>> referenced by libcrypto-lib-sha512-armv4.o:(.text+0x280) in archive _deps/openssl-src/libcrypto.a
  
...
```

This error repeats for multiple assembly objects, such as libcrypto-lib-sha512-armv4.o, libcrypto-lib-sha256-armv4.o, and libcrypto-lib-sha1-armv4-large.o.

The assembly files are being compiled with -fPIC. Here is an example for libcrypto-lib-sha512-armv4.o:
```
  armv7a-linux-androideabi34-clang  -Icrypto -I. -Iinclude -Iproviders/common/include -Iproviders/implementations/include  -DAES_ASM -DBSAES_ASM -DECP_NISTZ256_ASM -DGHASH_ASM -DKECCAK1600_ASM -DOPENSSL_BN_ASM_GF2m -DOPENSSL_BN_ASM_MONT -DOPENSSL_CPUID_OBJ -DPOLY1305_ASM -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DSTATIC_LEGACY -fPIC -pthread -Wa,--noexecstack -Qunused-arguments -Wall -O3 -march=armv7-a -DOPENSSL_USE_NODELETE -DOPENSSL_PIC -DOPENSSLDIR="\"$CMAKE_BUILD_DIR/_deps/openssl-build/ssl\"" -DENGINESDIR="\"$CMAKE_BUILD_DIR/_deps/openssl-build/lib/engines-3\"" -DMODULESDIR="\"$CMAKE_BUILD_DIR/_deps/openssl-build/lib/ossl-modules\"" -DOPENSSL_BUILDING_OPENSSL -DNDEBUG  -c -o crypto/sha/libcrypto-lib-sha512-armv4.o crypto/sha/sha512-armv4.S
```

This issue does not seem to appear when building OpenSSL directly as a shared object, likely because the problematic relocations are deferred to runtime in that case. However, it’s possible that this could result in subtle bugs on 32-bit ARM Android platforms when using libcrypto.so.

The following changes appear to fix the issue:
```diff
 #if __ARM_MAX_ARCH__>=7 && !defined(__KERNEL__)
 .LOPENSSL_armcap:
+# if !defined(OPENSSL_PIC)
 #  ifdef	_WIN32
 .word	OPENSSL_armcap_P
 #  else
 .word	OPENSSL_armcap_P-.Lsha512_block_data_order
 #  endif
+# else
+.word   OPENSSL_armcap_P(GOT)
+# endif
 .skip	32-4
 #else
 .skip	32
 #endif
```

```diff
 #if __ARM_MAX_ARCH__>=7 && !defined(__KERNEL__)
 	ldr	r12,.LOPENSSL_armcap
-# if !defined(_WIN32)
+# if !defined(_WIN32) && !defined(OPENSSL_PIC)
 	ldr	r12,[r3,r12]		@ OPENSSL_armcap_P
 # endif
-# if defined(__APPLE__) || defined(_WIN32)
+# if defined(__APPLE__) || defined(_WIN32) || defined(OPENSSL_PIC)
 	ldr	r12,[r12]
 # endif
```

Similar changes would have to be applied to all assemblies that use OpenSSL_armcap symbol.

I currently can't test if this fully fixes the issue, so please take a look into it.
```

## What you have

- `/testbed/repo` is a git clone of `openssl/openssl` truncated just after the regression was
  reported.  `HEAD` is `93d1bb6dff0f0126ef1a5cac7b8693308763eb8a` and the full history behind it is present.
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
