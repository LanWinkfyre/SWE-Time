# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
rustdoc crashing on linux-sparc64 due to unaligned access

Since version 1.31.0, ```rustdoc``` crashes when running the test ```src/test/run-make-fulldeps/rustdoc-error-lines```:

```
(sid_sparc64-dchroot)glaubitz@kyoto:~/rust$ cd src/test/run-make-fulldeps/rustdoc-error-lines
(sid_sparc64-dchroot)glaubitz@kyoto:~/rust/src/test/run-make-fulldeps/rustdoc-error-lines$ LD_LIBRARY_PATH="/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/test/run-make-fulldeps/rustdoc-error-lines/rustdoc-error-lines:/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib:/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage0-bootstrap-tools/sparc64-unknown-linux-gnu/release/deps:/usr/lib:" '/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/bin/rustdoc' -L /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib/rustlib/sparc64-unknown-linux-gnu/lib --test input.rs
Bus error
(sid_sparc64-dchroot)glaubitz@kyoto:~/rust/src/test/run-make-fulldeps/rustdoc-error-lines$
(sid_sparc64-dchroot)glaubitz@kyoto:~/rust/src/test/run-make-fulldeps/rustdoc-error-lines$ LD_LIBRARY_PATH="/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/test/run-make-fulldeps/rustdoc-error-lines/rustdoc-error-lines:/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib:/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage0-bootstrap-tools/sparc64-unknown-linux-gnu/release/deps:/usr/lib:" '/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/bin/rustdoc' -L /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib/rustlib/sparc64-unknown-linux-gnu/lib --test input.rs
Bus error
(sid_sparc64-dchroot)glaubitz@kyoto:~/rust/src/test/run-make-fulldeps/rustdoc-error-lines$ gdb /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/bin/rustdoc       GNU gdb (Debian 8.2-1) 8.2                                                                                                                                                  Copyright (C) 2018 Free Software Foundation, Inc.                                                                                                                           License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "sparc64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/bin/rustdoc...(no debugging symbols found)...done.
(gdb) set environment LD_LIBRARY_PATH "/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/test/run-make-fulldeps/rustdoc-error-lines/rustdoc-error-lines:/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib:/home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage0-bootstrap-tools/sparc64-unknown-linux-gnu/release/deps:/usr/lib:"
(gdb) r -L /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib/rustlib/sparc64-unknown-linux-gnu/lib --test input.rs
Starting program: /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/bin/rustdoc -L /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib/rustlib/sparc64-unknown-linux-gnu/lib --test input.rs
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/sparc64-linux-gnu/libthread_db.so.1".
[New Thread 0xffff80010793e100 (LWP 16987)]

Thread 2 "rustdoc" received signal SIGBUS, Bus error.
[Switching to Thread 0xffff80010793e100 (LWP 16987)]
0x000001000038a48c in pulldown_cmark::parse::RawParser::new_with_links_and_callback ()
(gdb) bt
#0  0x000001000038a48c in pulldown_cmark::parse::RawParser::new_with_links_and_callback ()
#1  0x00000100003855c0 in pulldown_cmark::passes::Parser::new_with_broken_link_callback ()
#2  0x000001000038546c in pulldown_cmark::passes::Parser::new ()
#3  0x000001000014a8a4 in rustdoc::html::markdown::find_testable_code ()
#4  0x00000100003357a4 in <rustdoc::test::HirCollector<'a, 'hir> as rustc::hir::intravisit::Visitor<'hir>>::visit_item ()
#5  0x00000100002e2178 in <scoped_tls::ScopedKey<T>>::set ()
#6  0x00000100003304d4 in rustdoc::test::run ()
#7  0x000001000009b3fc in rustdoc::main_args ()
#8  0x00000100002e0b68 in <scoped_tls::ScopedKey<T>>::set ()
#9  0x0000010000082ae4 in syntax::with_globals ()
#10 0x000001000015b600 in std::sys_common::backtrace::__rust_begin_short_backtrace ()
#11 0x000001000015bf40 in std::panicking::try::do_call ()
#12 0xffff8001044fdf58 in __rust_maybe_catch_panic () from /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib/libstd-3b39188da0a8cce7.so
#13 0x0000010000108be4 in <F as alloc::boxed::FnBox<A>>::call_box ()
#14 0xffff8001044eddc8 in std::sys_common::thread::start_thread () from /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib/libstd-3b39188da0a8cce7.so
#15 0xffff8001044b6300 in std::sys::unix::thread::Thread::new::thread_start ()
   from /home/glaubitz/rust/build/sparc64-unknown-linux-gnu/stage2/lib/libstd-3b39188da0a8cce7.so
#16 0xffff80010478fe68 in start_thread () from /lib/sparc64-linux-gnu/libpthread.so.0
#17 0xffff800104aa8274 in ?? () from /lib/sparc64-linux-gnu/libc.so.6
Backtrace stopped: previous frame identical to this frame (corrupt stack?)
(gdb)
```

I have not worked out yet whether this is a regression in the Rust compiler itself such that it generates code with unaligned access (we had this before) or whether ```rustdoc``` itself contains broken code.

CC @jrtc27 @psumbera @karcherm

Found the commit which introduced the bug:
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `adbfec229ce07ff4b2a7bf2d6dec2d13cb224980` and the full history behind it is present.
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
