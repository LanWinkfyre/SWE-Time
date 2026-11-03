# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ICE: sty: `None`

<!--
[31mICE[0m: Rustc ./a.rs '' 'thread 'rustc' panicked at compiler/rustc_middle/src/ty/sty.rs:2078:27: 'called `Option::unwrap()` on a `None` value'', 'thread 'rustc' panicked at compiler/rustc_middle/src/ty/sty.rs:2078:27: 'called `Option::unwrap()` on a `None` value''
File: /tmp/im/a.rs
-->

snippet:
````rust
const fn x() {
    let array = [(); { loop {} }];
    let nan1: f64 = unsafe { std::mem::transmute([4]) };
}

fn main() {}

````

Version information
`

Possibly related line of code:


Command:
`/home/matthias/.rustup/toolchains/master/bin/rustc `

<details><summary><strong>Program output</strong></summary>
<p>



</p>
</details>

<!--
query stack:
#0 [lint_mod] linting top-level module
#1 [analysis] running analysis passes on this crate

-->





cc @nnethercote
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `f2d69d5a7c04617d122facd0a7a5bdde0af928ae` and the full history behind it is present.
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
