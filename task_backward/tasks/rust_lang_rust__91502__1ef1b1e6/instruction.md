# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
struct update syntax causes ICE

<!--
Thank you for finding an Internal Compiler Error! 🧊  If possible, try to provide
a minimal verifiable example. You can read "Rust Bug Minimization Patterns" for
how to create smaller examples.

http://blog.pnkfx.org/blog/2019/11/18/rust-bug-minimization-patterns/

-->

### Code

```Rust
use once_cell::sync::OnceCell;
struct Foo {
    a: u64,
    b: u64,
    c: u64,
}
struct Bar {
    b: u64,
    c: u64,

}

static BAR: OnceCell<Bar> = OnceCell::new();

impl Foo {
    fn with_a(a: u64) -> Foo {
        Foo {
            a,
            ..BAR.get().unwrap() // Realized later that this shouldn't compile, but I'd expect an error, not an ICE
        }
    }
}
```
[Playground link](https://play.rust-lang.org/?version=nightly&mode=debug&edition=2021&gist=730f6b96dc286b2cb6dcad243fe6af7e)

### Meta
<!--
If you're using the stable version of the compiler, you should also check if the
bug also exists in the beta or nightly versions.
-->

`rustc --version --verbose`:


### Error output



<!--
Include a backtrace in the code block by setting `RUST_BACKTRACE=1` in your
environment. E.g. `RUST_BACKTRACE=1 cargo build`.
-->
<details><summary><strong>Backtrace</strong></summary>
<p>

```
thread 'rustc' panicked at 'Box<dyn Any>', compiler/rustc_errors/src/lib.rs:1170:9
stack backtrace:
   0: std::panicking::begin_panic::<rustc_errors::ExplicitBug>
   1: std::panic::panic_any::<rustc_errors::ExplicitBug>
   2: <rustc_errors::HandlerInner>::bug
   3: <rustc_errors::Handler>::bug
   4: rustc_middle::ty::context::tls::with_opt::<rustc_middle::util::bug::opt_span_bug_fmt<rustc_span::span_encoding::Span>::{closure#0}, ()>
   5: rustc_middle::util::bug::opt_span_bug_fmt::<rustc_span::span_encoding::Span>
   6: rustc_middle::util::bug::bug_fmt
   7: <rustc_typeck::check::fn_ctxt::FnCtxt>::apply_adjustments
   8: <rustc_typeck::check::method::confirm::ConfirmContext>::confirm
   9: <rustc_typeck::check::fn_ctxt::FnCtxt>::lookup_method
  10: <rustc_typeck::check::fn_ctxt::FnCtxt>::check_expr_kind
  11: <rustc_typeck::check::fn_ctxt::FnCtxt>::check_expr_with_expectation_and_args
  12: <rustc_typeck::check::fn_ctxt::FnCtxt>::check_expr_kind
  13: <rustc_typeck::check::fn_ctxt::FnCtxt>::check_expr_with_expectation_and_args
  14: <rustc_typeck::check::fn_ctxt::FnCtxt>::check_expr_kind
  15: <rustc_typeck::check::fn_ctxt::FnCtxt>::check_expr_with_expectation_and_args
  16: <rustc_typeck::check::fn_ctxt::FnCtxt>::check_block_with_expected
  17: <rustc_typeck::check::fn_ctxt::FnCtxt>::check_expr_with_expectation_and_args
  18: rustc_typeck::check::check::check_fn
  19: <rustc_infer::infer::InferCtxtBuilder>::enter::<&rustc_middle::ty::context::TypeckResults, <rustc_typeck::check::inherited::InheritedBuilder>::enter<rustc_typeck::check::typeck_with_fallback<rustc_typeck::check::typeck::{closure#0}>::{closure#1}, &rustc_middle::ty::context::TypeckResults>::{closure#0}>
  20: rustc_typeck::check::typeck
  21: rustc_query_system::query::plumbing::try_execute_query::<rustc_query_impl::plumbing::QueryCtxt, rustc_query_system::query::caches::DefaultCache<rustc_span::def_id::LocalDefId, &rustc_middle::ty::context::TypeckResults>>
  22: <rustc_query_impl::Queries as rustc_middle::ty::query::QueryEngine>::typeck
  23: <rustc_middle::hir::map::Map>::par_body_owners::<rustc_typeck::check::typeck_item_bodies::{closure#0}>
  24: rustc_typeck::check::typeck_item_bodies
  25: rustc_query_system::query::plumbing::try_execute_query::<rustc_query_impl::plumbing::QueryCtxt, rustc_query_system::query::caches::DefaultCache<(), ()>>
  26: rustc_query_system::query::plumbing::get_query::<rustc_query_impl::queries::typeck_item_bodies, rustc_query_impl::plumbing::QueryCtxt>
  27: <rustc_session::session::Session>::time::<(), rustc_typeck::check_crate::{closure#7}>
  28: rustc_typeck::check_crate
  29: rustc_interface::passes::analysis
  30: rustc_query_system::query::plumbing::try_execute_query::<rustc_query_impl::plumbing::QueryCtxt, rustc_query_system::query::caches::DefaultCache<(), core::result::Result<(), rustc_errors::ErrorReported>>>
  31: rustc_query_system::query::plumbing::get_query::<rustc_query_impl::queries::analysis, rustc_query_impl::plumbing::QueryCtxt>
  32: <rustc_interface::passes::QueryContext>::enter::<rustc_driver::run_compiler::{closure#1}::{closure#2}::{closure#3}, core::result::Result<(), rustc_errors::ErrorReported>>
  33: <rustc_interface::interface::Compiler>::enter::<rustc_driver::run_compiler::{closure#1}::{closure#2}, core::result::Result<core::option::Option<rustc_interface::queries::Linker>, rustc_errors::ErrorReported>>
  34: rustc_span::with_source_map::<core::result::Result<(), rustc_errors::ErrorReported>, rustc_interface::interface::create_compiler_and_run<core::result::Result<(), rustc_errors::ErrorReported>, rustc_driver::run_compiler::{closure#1}>::{closure#1}>
  35: <scoped_tls::ScopedKey<rustc_span::SessionGlobals>>::set::<rustc_interface::util::setup_callbacks_and_run_in_thread_pool_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_errors::ErrorReported>, rustc_driver::run_compiler::{closure#1}>::{closure#0}, core::result::Result<(), rustc_errors::ErrorReported>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_errors::ErrorReported>>
```

</p>
</details>



<!-- TRIAGEBOT_START -->

<!-- TRIAGEBOT_ASSIGN_START -->

<!-- TRIAGEBOT_ASSIGN_DATA_START$${"user":"compiler-errors"}$$TRIAGEBOT_ASSIGN_DATA_END -->

<!-- TRIAGEBOT_ASSIGN_END -->
<!-- TRIAGEBOT_END -->

 We have a "type changing struct-update" here because we're doing `..struct` from a `&Bar` down into a `Bar` and there's some deref adjustment stuff going on here (or something like that).

I can demote this `bug!()` into a `delay_span_bug` to suppress the ICE, but I'm gonna take a better look at this first and see if I can fix it a bit more cleanly.
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `532d2b14c05f9bc20b2d27cbb5f4550d28343a36` and the full history behind it is present.
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
