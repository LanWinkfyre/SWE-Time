# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Assertion in codegen with recursive subtyping

This works on Julia 1.0-1.3 but fails on 1.4-current master.
```
julia> struct A{T}
           x::T
       end

julia> struct B <: AbstractVector{A{B}}
       end

julia> A(B())
julia: /home/alex/Projects/julia/src/cgutils.cpp:611: llvm::Type* _julia_struct_to_llvm(jl_codegen_params_t*, jl_value_t*, jl_unionall_t*, bool*, bool): Assertion `isptr == jl_field_isptr(jst, i)' failed.

signal (6): Aborted
in expression starting at none:0
gsignal at /lib/x86_64-linux-gnu/libc.so.6 (unknown line)
abort at /lib/x86_64-linux-gnu/libc.so.6 (unknown line)
unknown function (ip: 0x7f1fe56bc489)
__assert_fail at /lib/x86_64-linux-gnu/libc.so.6 (unknown line)
_julia_struct_to_llvm at /home/alex/Projects/julia/src/cgutils.cpp:611
_julia_type_to_llvm at /home/alex/Projects/julia/src/cgutils.cpp:489
julia_type_to_llvm at /home/alex/Projects/julia/src/cgutils.cpp:499 [inlined]
mark_julia_type at /home/alex/Projects/julia/src/codegen.cpp:1325
emit_function at /home/alex/Projects/julia/src/codegen.cpp:6034
jl_emit_code at /home/alex/Projects/julia/src/codegen.cpp:7426
jl_emit_codeinst at /home/alex/Projects/julia/src/codegen.cpp:7471
_jl_compile_codeinst at /home/alex/Projects/julia/src/jitlayers.cpp:124
jl_generate_fptr at /home/alex/Projects/julia/src/jitlayers.cpp:352
jl_compile_method_internal at /home/alex/Projects/julia/src/gf.c:1978
jl_compile_method_internal at /home/alex/Projects/julia/src/gf.c:2244 [inlined]
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2237 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
#38 at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:220
jfptr_YY.38_54597 at /home/alex/Projects/julia/usr/lib/julia/sys.so (unknown line)
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
with_repl_linfo at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:462
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
display at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:213
display at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:225
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
display at ./multimedia.jl:328
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
jl_apply at /home/alex/Projects/julia/src/julia.h:1739 [inlined]
jl_f__call_latest at /home/alex/Projects/julia/src/builtins.c:732
#invokelatest#2 at ./essentials.jl:721 [inlined]
invokelatest at ./essentials.jl:719 [inlined]
print_response at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:247
#40 at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:231
jfptr_YY.40_55737 at /home/alex/Projects/julia/usr/lib/julia/sys.so (unknown line)
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
with_repl_linfo at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:462
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
print_response at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:229
do_respond at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:798
jfptr_do_respond_54708 at /home/alex/Projects/julia/usr/lib/julia/sys.so (unknown line)
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
jl_apply at /home/alex/Projects/julia/src/julia.h:1739 [inlined]
jl_f__call_latest at /home/alex/Projects/julia/src/builtins.c:732
#invokelatest#2 at ./essentials.jl:721 [inlined]
invokelatest at ./essentials.jl:719 [inlined]
run_interface at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/LineEdit.jl:2486
jfptr_run_interface_55466 at /home/alex/Projects/julia/usr/lib/julia/sys.so (unknown line)
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
run_frontend at /home/alex/Projects/julia/usr/share/julia/stdlib/v1.7/REPL/src/REPL.jl:1126
#44 at ./task.jl:406
jfptr_YY.44_53911 at /home/alex/Projects/julia/usr/lib/julia/sys.so (unknown line)
_jl_invoke at /home/alex/Projects/julia/src/gf.c:2245 [inlined]
jl_apply_generic at /home/alex/Projects/julia/src/gf.c:2427
jl_apply at /home/alex/Projects/julia/src/julia.h:1739 [inlined]
start_task at /home/alex/Projects/julia/src/task.c:859
Allocations: 2674 (Pool: 2665; Big: 9); GC: 0
[1]    9473 abort      /home/alex/Projects/julia/julia
```

Bisect:
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `8fc52931fca94f4247f2b0e8f69447f8417d70ab` and the full history behind it is present.
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
