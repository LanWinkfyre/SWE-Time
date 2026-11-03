# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Performance regression in nightly-2017-01-15

I've recently run into a performance regression in the Rust compiler in a project I'm working on.  Specifically, the 2017-01-14 nightly is good, and 2017-01-15 is bad. The regression is independent of `CARGO_INCREMENTAL=1`.

If you have a machine with a few cores, you can test it on a clone of https://github.com/mit-pdos/distributary/. Run with
```console
$ cargo run -v --release --bin vote -- --avg --articles=100000 --runtime=10 --migrate=3 soup:// | grep 'PUT+'
```

On `-14`, the "migration" mentioned in the middle finishes quite quickly. On `-15`, it takes a long time, and so `PUT` never transitions to `PUT+`.

I wanted to try a `git bisect` to narrow the problem down further, but compiling it takes *forever*. A cursory glance over the commit range doesn't reveal anything particularly suspect, and `#rust-internals` told me to post here to get some more eyes on the problem.
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `956e2bcbaa00c05e051718b1375375915064f1c3` and the full history behind it is present.
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
