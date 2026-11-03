# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[LLVM 11] link failure when using ASAN and cdylib together with LLD

System: Arch Linux

Linker: LLD 11.0.1 (compatible with GNU linkers)

## Reproduction
Create a new library

lib.rs:
```
#[derive(Debug)]
enum A {
    B,
}
```

Cargo.toml:
```
[lib]
crate-type = ["lib", "cdylib"]
```

Compile using:
```
RUSTFLAGS="-Zsanitizer=address -Clink-arg=-fuse-ld=lld" cargo +nightly build --target=x86_64-unknown-linux-gnu
```

## Result

```
  = note: ld.lld: error: undefined hidden symbol: __start_asan_globals
          >>> referenced by 2icvwuxjky13p126
          >>>               /xxx/bug/target/x86_64-unknown-linux-gnu/debug/deps/bug.2icvwuxjky13p126.rcgu.o:(asan.module_ctor)
          >>> referenced by 2icvwuxjky13p126
          >>>               /xxx/bug/target/x86_64-unknown-linux-gnu/debug/deps/bug.2icvwuxjky13p126.rcgu.o:(asan.module_dtor)

          ld.lld: error: undefined hidden symbol: __stop_asan_globals
          >>> referenced by 2icvwuxjky13p126
          >>>               /xxx/bug/target/x86_64-unknown-linux-gnu/debug/deps/bug.2icvwuxjky13p126.rcgu.o:(asan.module_ctor)
          >>> referenced by 2icvwuxjky13p126
          >>>               /xxx/bug/target/x86_64-unknown-linux-gnu/debug/deps/bug.2icvwuxjky13p126.rcgu.o:(asan.module_dtor)
          collect2: error: ld returned 1 exit status
```




LLVM issue? I am not sure how to get further
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `ca98712ff92c56506442cd5a500547f2f0cba0c3` and the full history behind it is present.
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
