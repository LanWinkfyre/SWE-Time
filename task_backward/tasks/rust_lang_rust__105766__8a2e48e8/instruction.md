# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Some bootstrap tests fail with custom rustc

### Command

I tried this with Rust 1.66.0, simplified from my build for Fedora:

```shell
$ ./configure --local-rust-root=/usr
$ ./x test bootstrap
```

I expected to see this happen: passing tests

Instead, this happened: 20 `builder::tests::...` failures, all of this sort:

```
---- builder::tests::alias_and_path_for_library stdout ----
failed to execute command: "/builddir/build/BUILD/rustc-1.66.0-src/build/x86_64-unknown-linux-gnu/stage0/bin/rustc" "--target" "x86_64-unknown-linux-gnu" "--print" "target-libdir"
error: No such file or directory (os error 2)
thread 'main' panicked at 'status code: 1', lib.rs:1654:9
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

My stage0 should be using `/usr/bin/rustc`.

### Version it worked on

It most recently worked on: Rust 1.65.0

### Version with regression

`rustc-1.66.0-src/version`:




### Backtrace
<details><summary>Backtrace</summary>
<p>

```
thread 'main' panicked at 'status code: 1', lib.rs:1654:9
stack backtrace:
   0: rust_begin_unwind
   1: core::panicking::panic_fmt
   2: bootstrap::detail_exit
             at ./lib.rs:1654:9
   3: bootstrap::util::fail
             at ./util.rs:475:5
   4: bootstrap::util::output
             at ./util.rs:425:19
   5: bootstrap::Build::new
             at ./lib.rs:436:13
   6: bootstrap::builder::tests::configure_with_args
             at ./builder/tests.rs:18:27
   7: bootstrap::builder::tests::configure
             at ./builder/tests.rs:6:5
   8: bootstrap::builder::tests::alias_and_path_for_library
             at ./builder/tests.rs:142:55
   9: bootstrap::builder::tests::alias_and_path_for_library::{{closure}}
             at ./builder/tests.rs:140:1
  10: core::ops::function::FnOnce::call_once
             at /builddir/build/BUILD/rustc-1.65.0-src/library/core/src/ops/function.rs:248:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</p>
</details>

@rustbot modify labels: +regression-from-stable-to-stable -regression-untriaged +A-bootstrap

<!-- TRIAGEBOT_START -->

<!-- TRIAGEBOT_ASSIGN_START -->

<!-- TRIAGEBOT_ASSIGN_DATA_START$${"user":"KittyBorgX"}$$TRIAGEBOT_ASSIGN_DATA_END -->

<!-- TRIAGEBOT_ASSIGN_END -->
<!-- TRIAGEBOT_END -->
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `7a6af2711baa5a5db116c123116b2150ed63799d` and the full history behind it is present.
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
