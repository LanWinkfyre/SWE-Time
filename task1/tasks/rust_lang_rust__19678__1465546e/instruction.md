# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`make install` is failing

```
$ make install
…
rustdoc: doc/rustc_trans/index.html
/home/chris/rust/src/librustc_trans/lib.rs:25:40: 25:46 warning: feature has been added to Rust, directive not necessary
/home/chris/rust/src/librustc_trans/lib.rs:25 #![feature(default_type_params, globs, if_let, import_shadowing, macro_rules, phase, quote)]
                                                                                     ^~~~~~
<stdin>:5:2: 5:3 error: unknown start of token: \\
<stdin>:5  \   /
           ^
task '<main>' panicked at 'Box<Any>', /home/chris/rust/src/libsyntax/diagnostic.rs:99
/home/chris/rust/mk/docs.mk:287: recipe for target 'doc/rustc_trans/index.html' failed
make[1]: *** [doc/rustc_trans/index.html] Error 101
make[1]: Leaving directory '/home/chris/rust'
/home/chris/rust/mk/install.mk:22: recipe for target 'install' failed
make: *** [install] Error 2
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `8fbfa66b4591023d54d885fff9cdf889393af109` and the full history behind it is present.
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
