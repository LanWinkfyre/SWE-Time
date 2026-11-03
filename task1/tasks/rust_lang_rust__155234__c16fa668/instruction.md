# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
regression: worker-thread stack overflow while building stage1 rustc on sparcv9-sun-solaris

I am seeing a regression when building Rust on `sparcv9-sun-solaris`.

  Environment
  - host: `sparcv9-sun-solaris`
  - OS: Solaris 11.4 on `sun4v`
  - build type: normal `dist`/nightly build

  Bisection


  

  Failure
  The build fails while compiling `rustc_attr_parsing`:

  ```text
  thread 'lto cgu.04' (26) has overflowed its stack
  fatal runtime error: stack overflow, aborting
  rustc exited with signal: 6 (SIGABRT) (core dumped)
  error: could not compile `rustc_attr_parsing` (lib)
```
  Notes

  - Changing ulimit -s did not help.
  - The overflow is in a Rust-created worker thread, not the shell/main thread.
  - From source inspection, rustc worker threads use the internal default stack size unless overridden via RUST_MIN_STACK.

  Workaround
  Setting:

  `RUST_MIN_STACK=16777216`

  makes the same build pass on this machine.

  So the current picture is:

  - default worker-thread stack (8 MiB) fails on this target/build
  - 16 MiB is sufficient in my testing
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `14196dbfa3eb7c30195251eac092b1b86c8a2d84` and the full history behind it is present.
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
