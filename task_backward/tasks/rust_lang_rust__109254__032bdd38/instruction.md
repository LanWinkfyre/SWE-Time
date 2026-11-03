# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Failed to bootstrap rustc due to size assertions

Rut language (lates git sources) build on Solaris x86 fails with:
```
error[E0308]: mismatched types
    --> /builds/psumbera/rust-lang-build/compiler/rustc_index/src/lib.rs:29:32
     |
27   | macro_rules! static_assert_size {
     | ------------------------------- in this expansion of `static_assert_size!`
28   |     ($ty:ty, $size:expr) => {
29   |         const _: [(); $size] = [(); ::std::mem::size_of::<$ty>()];
     |                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected an array with a fixed size of 136 elements, found one with 144 elements
     |
    ::: compiler/rustc_ast/src/ast.rs:3130:5
     |
3130 |     static_assert_size!(Item, 136);
     |     ------------------------------ in this macro invocation

error[E0308]: mismatched types
    --> /builds/psumbera/rust-lang-build/compiler/rustc_index/src/lib.rs:29:32
     |
27   | macro_rules! static_assert_size {
     | ------------------------------- in this expansion of `static_assert_size!`
28   |     ($ty:ty, $size:expr) => {
29   |         const _: [(); $size] = [(); ::std::mem::size_of::<$ty>()];
     |                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ expected an array with a fixed size of 64 elements, found one with 72 elements
     |
    ::: compiler/rustc_ast/src/ast.rs:3131:5
     |
3131 |     static_assert_size!(ItemKind, 64);
     |     --------------------------------- in this macro invocation
```
Strange is that build on Solaris SPARC is ok.

I tried to use git bisect and it says:
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `511364e7874dba9649a264100407e4bffe7b5425` and the full history behind it is present.
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
