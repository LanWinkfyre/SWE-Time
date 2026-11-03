# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wrong glibc linked in building crates using proc_macro with linuxbrew

If the versions of system glibc and linuxbrew glibc are different, building crates using proc_macro (ex. serde_derive, structopt_derive) is failed at Rust 1.32.0.
In Rust 1.31.1, this issue don't occur.

## Environment
CentOS Linux release 7.6.1810 (Core)
Rust 1.32.0, 1.31.1
System glibc: 2.17
linuxbrew glibc: 2.23

## Step

### Source code

Cargo.toml

```toml
[package]
name = "temp"
version = "0.1.0"

[dependencies]
structopt    = "0.2.14"
```

src/main.rs

```
#[macro_use]
extern crate structopt;
use structopt::StructOpt;

#[derive(Debug, StructOpt)]
pub struct Opt {}

fn main() {
    let _ = Opt::from_args();
    println!("Hello, world!");
}
```

### Build result

```
$ rustup override set 1.32.0
$ cargo clean; cargo run

   Compiling structopt v0.2.14
error: /lib64/libc.so.6: version `GLIBC_2.18' not found (required by /home/dalance/work/repos/temp/target/debug/deps/libstructopt_derive-cdf0ae629ff7e333.so)
   --> /home/dalance/.cargo/registry/src/github.com-1ecc6299db9ec823/structopt-0.2.14/src/lib.rs:490:1
    |
490 | extern crate structopt_derive;
    | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

error: aborting due to previous error

error: Could not compile `structopt`.
```

The `ldd` result of `libstructopt_derive....so` is below.
In this result, linker should search to linuxbrew's glibc, but actually search to system glibc.

```
$ ldd /home/dalance/work/repos/temp/target/debug/deps/libstructopt_derive-cdf0ae629ff7e333.so
        linux-vdso.so.1 (0x00007fffac483000)
        libdl.so.2 => /home/dalance/.linuxbrew/lib/libdl.so.2 (0x00007f2c95292000)
        librt.so.1 => /home/dalance/.linuxbrew/lib/librt.so.1 (0x00007f2c95288000)
        libpthread.so.0 => /home/dalance/.linuxbrew/lib/libpthread.so.0 (0x00007f2c95268000)
        libgcc_s.so.1 => /home/dalance/.linuxbrew/lib/libgcc_s.so.1 (0x00007f2c95051000)
        libc.so.6 => /home/dalance/.linuxbrew/lib/libc.so.6 (0x00007f2c94eb3000)
        /home/dalance/.linuxbrew/Cellar/glibc/2.23/lib64/ld-linux-x86-64.so.2 (0x00007f2c9566a000)
```

### Workaround

If `.cargo/config` set to below, build is passed at Rust 1.32.0.

```
[target.x86_64-unknown-linux-gnu]
linker = "/usr/bin/cc"
```

## Broken revision

I run `git bisect` from 1.31.1 to 1.32.0. The result is below.







## Related issue

This issue seems to be the same.
https://github.com/rust-lang/cargo/issues/6582
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `75f9159009cd0814bd6b5c3bf6a5406de7c4fe8d` and the full history behind it is present.
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
