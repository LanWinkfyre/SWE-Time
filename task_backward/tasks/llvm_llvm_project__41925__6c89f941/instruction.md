# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
missed optimization leading to compiletime assert with address sanitizer

|  |  |
| --- | --- |
| Bugzilla Link | [42580](https://llvm.org/bz42580) |
| Version | trunk |
| OS | Linux |
| Blocks | llvm/llvm-project#4440  |
| CC | @arndb,@efriedma-quic,@nathanchance,@nickdesaulniers,@zygoloid |

## Extended Description 
The current clang-9 prerelease causes one file in the linux kernel to get fail compilation with an assertion triggering when building with -sanitize=kernel-address:

```c
void __iwl_err(char *, ...);
int a;
void iwl_fw_dbg_apply_point() {
  const char b[] = "WRT ext=%d. Invalid apply point %d for %s\n";
  if (a) {
    void __compiletime_assert_2790(void);
    if (b[sizeof(b) - 2] != '\n')
      __compiletime_assert_2790();
  }
  __iwl_err(0, b);
}
```

$ clang-9 -O2 -fsanitize=kernel-address  -S dbg.i -o-    | grep compiletime
	callq	__compiletime_assert_2790

both clang-8 and gcc-8 pass the assertion here.

See also https://godbolt.org/z/cPrkv4

I bisected using Arnd's reproducer:





























 NFC
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `8b222ecf2769ee133691f208f6166ce118c4a164` and the full history behind it is present.
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
