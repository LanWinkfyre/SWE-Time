# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`error: relocation refers to local symbol "" [12], which is defined in a discarded section` only when using ld.gold linker with --gc-sections

**tl;dr:** https://github.com/rust-lang/rust/issues/59652#issuecomment-482253086

Cannot compile firefox anymore due to:
 error: linking with ... cargo-linker
error: relocation refers to local symbol "" [12], which is defined in a discarded section



https://bugzilla.mozilla.org/show_bug.cgi?id=1541214

<details><summary>old info</summary>
This issue doesn't happen with
Last **good** nightly:
<s>nightly-2019-03-28-x86_64-unknown-linux-gnu (default)

binary: rustc

commit-date: 2019-03-27
host: x86_64-unknown-linux-gnu
release: 1.35.0-nightly
LLVM version: 8.0</s>
nightly-2019-03-29-x86_64-unknown-linux-gnu (default)

binary: rustc

commit-date: 2019-03-28
host: x86_64-unknown-linux-gnu
release: 1.35.0-nightly
LLVM version: 8.0


The issue happens with
First **bad** nightly:
<s>nightly-2019-03-29-x86_64-unknown-linux-gnu (default)

binary: rustc

commit-date: 2019-03-28
host: x86_64-unknown-linux-gnu
release: 1.35.0-nightly
LLVM version: 8.0</s>
nightly-2019-03-30-x86_64-unknown-linux-gnu (default)

binary: rustc

commit-date: 2019-03-29
host: x86_64-unknown-linux-gnu
release: 1.35.0-nightly
LLVM version: 8.0

For each test I was using the same cargo:
cargo 1.35.0-dev (025b01ed 2019-04-01)
release: 1.35.0
commit-hash: 025b01edd0bba49b7e49c1cacc65bb1f6462ee57
commit-date: 2019-04-01

</details>

Errors look like this:

 0:16.63 = note: /home/user/.rustup/toolchains/nightly-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/lib/libcompiler_builtins-9b00dedc0dda6ebf.rlib(compiler_builtins-9b00dedc0dda6ebf.compiler_builtins.cqcjgied-cgu.0.rcgu.o)(.stack_sizes+0x0): error: relocation refers to local symbol "" [12], which is defined in a discarded section

 0:16.84 section group signature: "(null)"
0:16.84 /home/user/.rustup/toolchains/nightly-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/lib/libstd-e4188d26f42911c5.rlib(std-e4188d26f42911c5.std.b8iklw2d-cgu.0.rcgu.o)(.stack_sizes+0x1b): error: relocation refers to local symbol "" [696], which is defined in a discarded section
0:16.84 section group signature: "(null)"




```
    
```

<details>





</details>
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `7641873f591dca86e2b31f60fc76b39553892631` and the full history behind it is present.
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
