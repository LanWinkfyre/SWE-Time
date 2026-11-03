# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
#![no_std] results in linker errors for debug builds that use Drop due to _rust_eh_personality

The following simple program fails to compile with Rust because the `Drop` trait introduces an incompatibility that causes a linker error. If you comment out the `impl` block, then it will work just fine. Additionally, if you compile with optimizations turned on, it will work just fine. But if you compile the following without optimizations, it will fail.

**t.rs:**
```rust
#![feature(lang_items, start)]
#![no_std]

#[lang = "eh_personality"] extern fn eh_personality() {}
#[lang = "panic_fmt"] fn panic_fmt() -> ! { loop {} }

struct Foo {}

impl core::ops::Drop for Foo {
    fn drop(&mut self) {
    }
}

#[start]
fn main(_argc: isize, _argv: *const *const u8) -> isize {
    let _foo = Foo {};
    return 0;
}
```

**The error:** (part of the paths have been redacted; `<RUSTUP>` is the installation directory for `rustup`)
```
$ rustc t.rs -l c
error: linking with `cc` failed: exit code: 1
  |
  = note: "cc" "-m64" "-L" "<RUSTUP>/toolchains/nightly-x86_64-apple-darwin/lib/rustlib/x86_64-apple-darwin/lib" "t.t0.rcgu.o" "t.t1.rcgu.o" "-o" "t" "-Wl,-dead_strip" "-nodefaultlibs" "-L" "<RUSTUP>/toolchains/nightly-x86_64-apple-darwin/lib/rustlib/x86_64-apple-darwin/lib" "-l" "c" "<RUSTUP>/toolchains/nightly-x86_64-apple-darwin/lib/rustlib/x86_64-apple-darwin/lib/libcore-6ee4b7a50e610a70.rlib"
  = note: Undefined symbols for architecture x86_64:
            "_rust_eh_personality", referenced from:
                Dwarf Exception Unwind Info (__eh_frame) in t.t0.rcgu.o
          ld: symbol(s) not found for architecture x86_64
          clang: error: linker command failed with exit code 1 (use -v to see invocation)


error: aborting due to previous error
```

**Rust version:**


**Note:** Building with optimizations on works, presumably because the optimizer is able to optimize away the call to `core::ptr::drop_in_place` (which is tagged with `.cfi_personality 155, _rust_eh_personality` in the generated debug assembly, which I presume is the source of the problem):
```
$ rustc t.rs -O -l c
$ ./t
```

**My system:** macOS 10.13.2. `rustc` is installed from `rustup`.




cc @arielb1

Unfortunately I don't know how to fix this. I'm not familiar enough with the compiler internals to be of much help other than this initial triage.
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `bb345a0be3ba3fa1970fe02789791c5c72788d8f` and the full history behind it is present.
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
