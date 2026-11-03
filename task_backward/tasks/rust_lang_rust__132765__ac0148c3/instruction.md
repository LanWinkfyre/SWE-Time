# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[ICE]: index out of bounds

### Code

```rust
trait LendingIterator {
    type Item<'q>: 'a;
    fn for_each(mut self, mut f: Box<dyn FnMut(Self::Item<'_>) + 'static>) {}
}
struct Query<'q> {}
impl<'static> Query<'q> {
    pub fn new() -> Self {}
}
fn data() {
    LendingIterator::for_each(Box::new(&data), Box::new);
}
pub fn main() {}

```

### Affected release channels

- [ ] Previous Stable
- [ ] Current Stable
- [ ] Current Beta
- [x] Current Nightly

### Rust Version


binary: rustc

commit-date: 2024-11-07
host: x86_64-unknown-linux-gnu
release: 1.84.0-nightly
LLVM version: 19.1.3

### Current error output



### Backtrace

```
thread 'rustc' panicked at /rust/deps/ena-0.14.3/src/snapshot_vec.rs:199:10:
index out of bounds: the len is 7 but the index is 7
stack backtrace:
   0:     0x7f719d25517a - <std::sys::backtrace::BacktraceLock::print::DisplayBacktrace as core::fmt::Display>::fmt::hfadad24fb33e3d1a
   1:     0x7f719da040a6 - core::fmt::write::h42d25fbda60cd99f
   2:     0x7f719edc3351 - std::io::Write::write_fmt::hc2819193e80b365e
   3:     0x7f719d254fd2 - std::sys::backtrace::BacktraceLock::print::h9450230402d77664
   4:     0x7f719d2574d6 - std::panicking::default_hook::{{closure}}::h739047d4d787c596
   5:     0x7f719d257320 - std::panicking::default_hook::h203d1229480f37a5
   6:     0x7f719c2d2269 - std[56fe22ad9ea837fd]::panicking::update_hook::<alloc[b5641001d343df5f]::boxed::Box<rustc_driver_impl[945e9afaf49c7d35]::install_ice_hook::{closure#0}>>::{clos
   7:     0x7f719d257be8 - std::panicking::rust_panic_with_hook::h657fdcc17f7e2546
   8:     0x7f719d2579ba - std::panicking::begin_panic_handler::{{closure}}::h6c1a7592f2611ed5
   9:     0x7f719d255629 - std::sys::backtrace::__rust_end_short_backtrace::h3e1efd1ff0b15465
  10:     0x7f719d25767c - rust_begin_unwind
  11:     0x7f7199ccd320 - core::panicking::panic_fmt::h41647251c9f15c53
  12:     0x7f719b9f0b1b - core::panicking::panic_bounds_check::h66515744fb563c4b
  13:     0x7f719dacc1f6 - <rustc_middle[f0eb6ba890d0a9bb]::ty::Ty as rustc_type_ir[8408d34320f8a6fb]::fold::TypeSuperFoldable<rustc_middle[f0eb6ba890d0a9bb]::ty::context::TyCtxt>>::try_
  14:     0x7f719dac6323 - <&rustc_middle[f0eb6ba890d0a9bb]::ty::list::RawList<(), rustc_middle[f0eb6ba890d0a9bb]::ty::generic_args::GenericArg> as rustc_type_ir[8408d34320f8a6fb]::fold:
  15:     0x7f719dac9e17 - <rustc_middle[f0eb6ba890d0a9bb]::ty::Ty as rustc_type_ir[8408d34320f8a6fb]::fold::TypeSuperFoldable<rustc_middle[f0eb6ba890d0a9bb]::ty::context::TyCtxt>>::try_
  16:     0x7f719dac8554 - <rustc_middle[f0eb6ba890d0a9bb]::ty::Ty as rustc_type_ir[8408d34320f8a6fb]::fold::TypeSuperFoldable<rustc_middle[f0eb6ba890d0a9bb]::ty::context::TyCtxt>>::try_
  17:     0x7f719d01a962 - <rustc_infer[21ddc8b2a5f19898]::infer::resolve::OpportunisticVarResolver as rustc_type_ir[8408d34320f8a6fb]::fold::FallibleTypeFolder<rustc_middle[f0eb6ba890d0
  18:     0x7f719d087548 - <rustc_trait_selection[c0f45c4e16f8dab6]::error_reporting::TypeErrCtxt>::same_type_modulo_infer::<rustc_middle[f0eb6ba890d0a9bb]::ty::Ty>
  19:     0x7f719d0fcaba - <rustc_trait_selection[c0f45c4e16f8dab6]::error_reporting::TypeErrCtxt>::note_type_err
  20:     0x7f719d084350 - <rustc_trait_selection[c0f45c4e16f8dab6]::error_reporting::TypeErrCtxt>::report_and_explain_type_error
  21:     0x7f719c62446e - <rustc_hir_typeck[9dbf9add14d719fd]::fn_ctxt::FnCtxt>::report_arg_errors
  22:     0x7f719a103be3 - <rustc_hir_typeck[9dbf9add14d719fd]::fn_ctxt::FnCtxt>::confirm_builtin_call
  23:     0x7f719e6fa2bf - <rustc_hir_typeck[9dbf9add14d719fd]::fn_ctxt::FnCtxt>::check_expr_with_expectation_and_args
  24:     0x7f719e6f4736 - <rustc_hir_typeck[9dbf9add14d719fd]::fn_ctxt::FnCtxt>::check_block_with_expected
  25:     0x7f719e6fabb4 - <rustc_hir_typeck[9dbf9add14d719fd]::fn_ctxt::FnCtxt>::check_expr_with_expectation_and_args
  26:     0x7f719dc4df5b - rustc_hir_typeck[9dbf9add14d719fd]::check::check_fn
  27:     0x7f719dc43bac - rustc_hir_typeck[9dbf9add14d719fd]::typeck
  28:     0x7f719dc43553 - rustc_query_impl[1357963d8dd30e8b]::plumbing::__rust_begin_short_backtrace::<rustc_query_impl[1357963d8dd30e8b]::query_impl::typeck::dynamic_query::{closure#2}::{closure#0}, rustc_middle[f0eb6ba890d0a9bb]::query::erase::Erased<[u8; 8usize]>>
  29:     0x7f719e123681 - rustc_query_system[887bb79932b1d8c1]::query::plumbing::try_execute_query::<rustc_query_impl[1357963d8dd30e8b]::DynamicConfig<rustc_query_system[887bb79932b1d8c1]::query::caches::VecCache<rustc_span[db86d96c2ae2e3a4]::def_id::LocalDefId, rustc_middle[f0eb6ba890d0a9bb]::query::erase::Erased<[u8; 8usize]>>, false, false, false>, rustc_query_impl[1357963d8dd30e8b]::plumbing::QueryCtxt, false>
  30:     0x7f719e121b4d - rustc_query_impl[1357963d8dd30e8b]::query_impl::typeck::get_query_non_incr::__rust_end_short_backtrace
  31:     0x7f719e1217c7 - <rustc_middle[f0eb6ba890d0a9bb]::hir::map::Map>::par_body_owners::<rustc_hir_analysis[af6e6fecb0b5810e]::check_crate::{closure#4}>::{closure#0}
  32:     0x7f719e11f799 - rustc_hir_analysis[af6e6fecb0b5810e]::check_crate
  33:     0x7f719e268aca - rustc_interface[5fea8bf9cd0b71b5]::passes::run_required_analyses
  34:     0x7f719e80861e - rustc_interface[5fea8bf9cd0b71b5]::passes::analysis
  35:     0x7f719e8085ef - rustc_query_impl[1357963d8dd30e8b]::plumbing::__rust_begin_short_backtrace::<rustc_query_impl[1357963d8dd30e8b]::query_impl::analysis::dynamic_query::{closure#2}::{closure#0}, rustc_middle[f0eb6ba890d0a9bb]::query::erase::Erased<[u8; 1usize]>>
  36:     0x7f719e992cee - rustc_query_system[887bb79932b1d8c1]::query::plumbing::try_execute_query::<rustc_query_impl[1357963d8dd30e8b]::DynamicConfig<rustc_query_system[887bb79932b1d8c1]::query::caches::SingleCache<rustc_middle[f0eb6ba890d0a9bb]::query::erase::Erased<[u8; 1usize]>>, false, false, false>, rustc_query_impl[1357963d8dd30e8b]::plumbing::QueryCtxt, false>
  37:     0x7f719e9929ce - rustc_query_impl[1357963d8dd30e8b]::query_impl::analysis::get_query_non_incr::__rust_end_short_backtrace
  38:     0x7f719e88707a - rustc_interface[5fea8bf9cd0b71b5]::interface::run_compiler::<core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>, rustc_driver_impl[945e9afaf49c7d35]::run_compiler::{closure#0}>::{closure#1}
  39:     0x7f719e8cd5d0 - std[56fe22ad9ea837fd]::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface[5fea8bf9cd0b71b5]::util::run_in_thread_with_globals<rustc_interface[5fea8bf9cd0b71b5]::util::run_in_thread_pool_with_globals<rustc_interface[5fea8bf9cd0b71b5]::interface::run_compiler<core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>, rustc_driver_impl[945e9afaf49c7d35]::run_compiler::{closure#0}>::{closure#1}, core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>>::{closure#0}, core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>>::{closure#0}::{closure#0}, core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>>
  40:     0x7f719e8cd9eb - <<std[56fe22ad9ea837fd]::thread::Builder>::spawn_unchecked_<rustc_interface[5fea8bf9cd0b71b5]::util::run_in_thread_with_globals<rustc_interface[5fea8bf9cd0b71b5]::util::run_in_thread_pool_with_globals<rustc_interface[5fea8bf9cd0b71b5]::interface::run_compiler<core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>, rustc_driver_impl[945e9afaf49c7d35]::run_compiler::{closure#0}>::{closure#1}, core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>>::{closure#0}, core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>>::{closure#0}::{closure#0}, core[5ba82ee3405aa490]::result::Result<(), rustc_span[db86d96c2ae2e3a4]::ErrorGuaranteed>>::{closure#1} as core[5ba82ee3405aa490]::ops::function::FnOnce<()>>::call_once::{shim:vtable#0}
  41:     0x7f719e8ce4b9 - std::sys::pal::unix::thread::Thread::new::thread_start::hb3d6392adeea417c
  42:     0x7f7198a6bac3 - start_thread
                               at ./nptl/pthread_create.c:442:8
  43:     0x7f7198afd850 - __GI___clone3
                               at ./misc/../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
  44:                0x0 - <unknown>
```

### Anything else?

This issue is similar to https://github.com/rust-lang/rust/issues/122098; however, https://github.com/rust-lang/rust/issues/122098 does not report an ICE on the current nightly version. The difference is the addition of a `main` function.
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `6295686a37ed731f1059b07157170c9ac56bf8c3` and the full history behind it is present.
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
