# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Compiler (effectively) hangs, regression from overflow error

```rs
pub enum Either<L, R> {
    Left(L),
    Right(R),
}

pub trait HasItem<'a, _Constraint = &'a Self> {
    type Item;
}

pub type Item<'a, Self_> = <Self_ as HasItem<'a>>::Item;

pub trait LendingIterator: for<'a> HasItem<'a> {
    fn next(&mut self) -> Option<Item<'_, Self>>;
}

impl<'a, A: 'a, B: 'a> HasItem<'a> for Either<A, B>
where A: LendingIterator, B: LendingIterator,
 for<'b> B: HasItem<'b, Item = Item<'b, Self>>
{
    type Item = Item<'a, Self>;
}

impl<A, B> LendingIterator for Either<A, B>
where A: LendingIterator, B: LendingIterator,
 for<'b> B: HasItem<'b, Item = Item<'b, Self>>
{
    fn next(&mut self) -> Option<Item<'_, Self>> {
        match self {
            Either::Left(iter) => iter.next(),
            Either::Right(iter) => iter.next(),
        }
    }
}
```
hangs since `1.56`
error [on `1.55`](https://godbolt.org/z/Er3v1xrPd)
```
error[E0275]: overflow evaluating the requirement `for<'b> <B as HasItem<'b>>::Item == <Either<A, B> as HasItem<'b>>::Item`
  --> <source>:16:24
   |
6  | pub trait HasItem<'a, _Constraint = &'a Self> {
   | --------------------------------------------- required by this bound in `HasItem`
...
16 | impl<'a, A: 'a, B: 'a> HasItem<'a> for Either<A, B>
   |                        ^^^^^^^^^^^
   |
note: required because of the requirements on the impl of `HasItem<'a>` for `Either<A, B>`
  --> <source>:16:24
   |
16 | impl<'a, A: 'a, B: 'a> HasItem<'a> for Either<A, B>
   |                        ^^^^^^^^^^^     ^^^^^^^^^^^^

error[E0275]: overflow evaluating the requirement `for<'b> <B as HasItem<'b>>::Item == <Either<A, B> as HasItem<'b>>::Item`
  --> <source>:23:12
   |
12 | pub trait LendingIterator: for<'a> HasItem<'a> {
   |                            ------------------- required by this bound in `LendingIterator`
...
23 | impl<A, B> LendingIterator for Either<A, B>
   |            ^^^^^^^^^^^^^^^
   |
note: required because of the requirements on the impl of `for<'a> HasItem<'a>` for `Either<A, B>`
  --> <source>:16:24
   |
16 | impl<'a, A: 'a, B: 'a> HasItem<'a> for Either<A, B>
   |                        ^^^^^^^^^^^     ^^^^^^^^^^^^

error[E0275]: overflow evaluating the requirement `for<'b> <B as HasItem<'b>>::Item == <Either<A, B> as HasItem<'b>>::Item`
  --> <source>:20:5
   |
20 |     type Item = Item<'a, Self>;
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
   |
note: required because of the requirements on the impl of `HasItem<'a>` for `Either<A, B>`
  --> <source>:16:24
   |
16 | impl<'a, A: 'a, B: 'a> HasItem<'a> for Either<A, B>
   |                        ^^^^^^^^^^^     ^^^^^^^^^^^^

error[E0275]: overflow evaluating the requirement `for<'b> <B as HasItem<'b>>::Item == <Either<A, B> as HasItem<'b>>::Item`
  --> <source>:27:8
   |
27 |     fn next(&mut self) -> Option<Item<'_, Self>> {
   |        ^^^^
   |
note: required because of the requirements on the impl of `HasItem<'_>` for `Either<A, B>`
  --> <source>:16:24
   |
16 | impl<'a, A: 'a, B: 'a> HasItem<'a> for Either<A, B>
   |                        ^^^^^^^^^^^     ^^^^^^^^^^^^

error: aborting due to 4 previous errors
```

@rustbot label I-hang, regression-from-stable-to-stable, A-traits, A-lifetimes, E-needs-bisection, T-compiler

<hr>

_Edit:_

“Hangs” means “runs for a wile on 100% CPU until I cancel it”. Who knows if it would ever terminate… actually, maybe I should test smaller recursion limits.

Note that this code example is _not expected_ to compile successfully. [Here’s a version that works / with the mistakes fixed](https://godbolt.org/z/cehTbs9cz). (The fixed version also works on some older Rust versions, including `1.55` and older.)


<hr>

_Edit2:_ Using smaller limits (like… around `#![recursion_limit = "14"]` it starts getting unbearably slow) reveals that this is apparently more like exponential-time slowdown rather than “actual” hanging.

@rustbot label -I-hang, +I-compiletime, +perf-regression
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `775e480722c7aba6ff4ff3ccec8c1f4639ae7889` and the full history behind it is present.
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
