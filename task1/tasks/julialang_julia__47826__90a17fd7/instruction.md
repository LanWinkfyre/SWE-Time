# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Segmentation fault with threads

For a simple multithreading code, it seems with version 1.9.0-alpha1, when running with more than 1 threads, julia crash randomly (more than 50%, but there are few chances the code finished fine). However, it is working fine with 1.8.3.

1. The output of `versioninfo()`
    

2. How you installed Julia
    ```bash
    juliaup add 1.9  # 1.9.0-alpha1+0.x64.linux.gnu
    juliaup add 1.8  # 1.8.3+0.x64.linux.gnu
    ```

3. A minimal working example (MWE), also known as a minimum reproducible example
    ```julia
    nw = 8
    nk = 1000
    A = zeros(ComplexF64, nw, nw, nk)
    B = rand(ComplexF64, nw, nw, nk)
    
    @time Threads.@threads for ik in 1:nk
        for j in 1:nk
            A[:, :, ik] += B[:, :, j]
        end
    end
    ```

The crash output is somewhat not unique, following are the output I collected:
```
[3544842] signal (11.1): Segmentation fault
in expression starting at /tmp/test_perf.jl:11
to_indices at ./indices.jl:354 [inlined]
to_indices at ./indices.jl:344 [inlined]
getindex at ./abstractarray.jl:1294
unknown function (ip: 0x7f97b610ef65)
_jl_invoke at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2450 [inlined]
ijl_apply_generic at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2632
macro expansion at /home/jqiao/git/wannier90_dev/examples/example16-noqe/test_perf.jl:14 [inlined]
#9#threadsfor_fun#3 at ./threadingconstructs.jl:139
#9#threadsfor_fun at ./threadingconstructs.jl:106 [inlined]
#1 at ./threadingconstructs.jl:84
unknown function (ip: 0x7f97b610db6f)
_jl_invoke at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2450 [inlined]
ijl_apply_generic at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2632
jl_apply at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/julia.h:1868 [inlined]
start_task at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/task.c:1089
Allocations: 11282400 (Pool: 11281162; Big: 1238); GC: 36
```

```
[3545031] signal (11.1): Segmentation fault
in expression starting at /tmp/test_perf.jl:11
ijl_get_nth_field at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/datatype.c:1500
ijl_get_nth_field_checked at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/datatype.c:1546
getindex at ./tuple.jl:29 [inlined]
to_indices at ./indices.jl:354 [inlined]
to_indices at ./indices.jl:344 [inlined]
getindex at ./abstractarray.jl:1294
unknown function (ip: 0x7f4e8d2bef65)
_jl_invoke at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2450 [inlined]
ijl_apply_generic at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2632
macro expansion at /tmp/test_perf.jl:14 [inlined]
#9#threadsfor_fun#3 at ./threadingconstructs.jl:139
#9#threadsfor_fun at ./threadingconstructs.jl:106 [inlined]
#1 at ./threadingconstructs.jl:84
unknown function (ip: 0x7f4e8d2bdb6f)
_jl_invoke at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2450 [inlined]
ijl_apply_generic at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2632
jl_apply at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/julia.h:1868 [inlined]
start_task at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/task.c:1089
Allocations: 5218944 (Pool: 5217706; Big: 1238); GC: 16
```

```
[3547161] signal (11.1): Segmentation fault
in expression starting at /tmp/test_perf.jl:11
jl_field_isatomic at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/julia.h:1183 [inlined]
ijl_get_nth_field at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/datatype.c:1507
ijl_get_nth_field_checked at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/datatype.c:1546
getindex at ./tuple.jl:29 [inlined]
to_indices at ./indices.jl:354 [inlined]
to_indices at ./indices.jl:344 [inlined]
setindex! at ./abstractarray.jl:1397
unknown function (ip: 0x7f4994111259)
_jl_invoke at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2450 [inlined]
ijl_apply_generic at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2632
macro expansion at /tmp/test_perf.jl:14 [inlined]
#9#threadsfor_fun#3 at ./threadingconstructs.jl:139
#9#threadsfor_fun at ./threadingconstructs.jl:106 [inlined]
#1 at ./threadingconstructs.jl:84
unknown function (ip: 0x7f499410db6f)
_jl_invoke at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2450 [inlined]
ijl_apply_generic at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/gf.c:2632
jl_apply at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/julia.h:1868 [inlined]
start_task at /cache/build/default-amdci5-1/julialang/julia-release-1-dot-9/src/task.c:1089
Allocations: 6392485 (Pool: 6391247; Big: 1238); GC: 20
```
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `495a004bda33e284b0acc612f5ced9ba1eb9a777` and the full history behind it is present.
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
