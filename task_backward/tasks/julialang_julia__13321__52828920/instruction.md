# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
SegFault in inference0.ji compilation on master for ARM

I get a segfault very early in the bootstrap when compiling the current master for 32bit ARM with stock LLVM 3.6.2. Happens with both qemu and native compilation.

Backtrace is

``` c
#0  0xb62d45b8 in jl_f_new_expr (F=<optimized out>, args=0xbefff254, nargs=3)
    at /home/yuyichao/julia/src/alloc.c:879
#1  0xb6ff60e8 in julia.new_0 ()
#2  0xb62787b4 in jl_apply (nargs=2, args=0xbefff2cc, f=<optimized out>)
    at /home/yuyichao/julia/src/julia.h:1328
#3  jl_apply_generic (F=0x95339680, args=0xbefff2cc, nargs=2)
    at /home/yuyichao/julia/src/gf.c:1708
#4  0xb62d1260 in jl_apply (nargs=2, args=0xbefff2cc, f=0x95339680)
    at /home/yuyichao/julia/src/julia.h:1328
#5  do_call (f=0x95339680, args=args@entry=0x9533c974, nargs=nargs@entry=2, 
    eval0=eval0@entry=0x0, locals=locals@entry=0x0, nl=nl@entry=0, 
    ngensym=ngensym@entry=0) at /home/yuyichao/julia/src/interpreter.c:65
#6  0xb62d03c0 in eval (e=<optimized out>, locals=locals@entry=0x0, 
    nl=nl@entry=0, ngensym=ngensym@entry=0)
    at /home/yuyichao/julia/src/interpreter.c:213
#7  0xb62d1170 in jl_interpret_toplevel_expr (e=<optimized out>)
    at /home/yuyichao/julia/src/interpreter.c:27
#8  0xb62e6934 in jl_toplevel_eval_flex (e=<optimized out>, fast=fast@entry=1)
    at /home/yuyichao/julia/src/toplevel.c:527
#9  0xb62e7734 in jl_toplevel_eval_flex (fast=1, e=<optimized out>)
    at /home/yuyichao/julia/src/toplevel.c:573
#10 jl_parse_eval_all (fname=fname@entry=0xb6d63a50 "boot.jl", len=len@entry=8)
    at /home/yuyichao/julia/src/toplevel.c:577
#11 0xb62e7970 in jl_load (fname=0xb6d63a50 "boot.jl", len=len@entry=8)
    at /home/yuyichao/julia/src/toplevel.c:617
#12 0xb62d73c8 in _julia_init (rel=<optimized out>)
    at /home/yuyichao/julia/src/init.c:549
#13 0xb62d8284 in julia_init (rel=<optimized out>)
    at /home/yuyichao/julia/src/task.c:260
#14 0x00011188 in main (argc=1, argv=0xbefffc1c)
    at /home/yuyichao/julia/ui/repl.c:594
```

The direct cause of the SegFault is that the first parameter (`args[0]`) to `jl_f_new_expr` is `NULL`.
This happens in the call `_new(:LabelNode, :Int)` in `boot.jl` (which is the `#3` in the backtrace)

The `jl_f_new_expr` is called from `julia.new_0` and the llvm ir can be find [here](https://gist.github.com/yuyichao/c3f9fc9dfdf1010a5b55#file-_new-ll), the dump of `jl_Module` right after codegen in `to_function()` is also [available](https://gist.github.com/yuyichao/c3f9fc9dfdf1010a5b55#file-_new-module-ll)

~~AFAICT, the first argument should be `*'jl_sym#curly5'` and I've verified in GDB that this is indeed `0`. A list of global symbols recognized by gdb is here and AFAIK none of them looks right.~~ The dereference is wrong here but it seems that this is [exactly the mistake we are making in codegen](https://github.com/JuliaLang/julia/issues/13321#issuecomment-143385886).

```
(gdb) p jl_(*'jl_sym#::4')
:fastmath                                                                         
$4 = void                                                                         
(gdb) p jl_(*'jl_sym#=1')
:Base
$5 = void
(gdb) p jl_(*'jl_sym#Type6')
:parameters
$6 = void
(gdb) p jl_(*'jl_sym#block8')
:flags
$7 = void
(gdb) p jl_(*'jl_sym#call2')
:meta
$8 = void
(gdb) p jl_(*'jl_sym#curly5')
#<null>
$9 = void
(gdb) p jl_(*'jl_sym#n7')
#<null>
$10 = void
(gdb) p jl_(*'jl_sym#new12')
:item
$11 = void
```

This only happens on master and not release-0.4 so @vtjnash 

Also @ViralBShah if you can reproduce this too.


Hmmm.
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `262d6babf634181c456868182f972a90240a5863` and the full history behind it is present.
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
