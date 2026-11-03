# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
GC error on 1.10



This is the minimized version of the issue that prompted #52256 (as well as #52184 and #51774, it took me two months to minimize) but one crucial difference is that the crash occurs on a normal (debug) build of julia with no particular flag set in the build process. It also crashes on julia master but not in v1.9.

The other crucial difference is that it crashes on a single thread (i.e. launched with `-t1`). All along the minimization process it only crashed when using multiple threads so this is a surprise.

<details>

<summary> reproducer.jl </summary>

```julia
using StaticArrays: SVector, SMatrix
using Printf

mutable struct System
    somelist::Vector{SVector{3,Float64}}
    mat::SMatrix{3,3,Float64,9}
end

function System(n)
    somelist = [zero(SVector{3,Float64}) for _ in 1:n]
    System(somelist, SMatrix{3,3,Float64,9}(25, 0, 0, 0, 25, 0, 0, 0, 25))
end

function output(o::System)
    mktemp() do _, io
        for s in ("", "")
            for (i, x) in enumerate(('a', 'b', 'c'))
                @printf io "%19.12f%19.12f%19.12f" o.mat[1,i] o.mat[2,i] o.mat[3,i]
            end
        end
        poss = zero(SVector{3,Float64})
        for opos in poss
            pos = o.mat*opos
            @printf io "%19.12f%19.12f%19.12f" pos[1] pos[2] pos[3]
        end
    end
    nothing
end

const CHANNEL = Channel{System}(Inf)
for _ in 1:5
    Base.Threads.@spawn while true
        x = take!($CHANNEL)
        output(x)
    end
end

function run_main(syst::System)
    for _ in 1:10
        put!(CHANNEL, deepcopy(syst))
        yield()
    end
    nothing
end


for irange in 1:10000
    step = System(80)
    run_main(step)
end

```

</details>

I then simply launch it with
```
/LionelSSDext4/liozou/julia-test-1.10/usr/bin/julia-debug -t1 --startup-file=no --bug-report=rr,chaos /tmp/reproducer.jl
```

Here is the rr trace: https://julialang-dumps.s3.amazonaws.com/reports/2023-12-01T10-48-13-Liozou.tar.zst
And the full output (including the dump):

<details>

<summary>output</summary>

```
GC error (probable corruption)
Allocations: 1520729 (Pool: 1519177; Big: 1552); GC: 1
Array{StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}, (80,)}[StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0)), StaticArraysCore.SArray{Tuple{3}, Float64, 1, 3}(data=(0, 0, 0))]

thread 0 ptr queue:
~~~~~~~~~~ ptr queue top ~~~~~~~~~~
Task(next=nothing, queue=Base.IntrusiveLinkedList{Task}(head=Task(next=Task(next=Task(next=Task(next=<circular reference @-6>, queue=<circular reference @-5>, storage=nothing, donenotify=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), result=nothing, logstate=nothing, code=Main.var"#5#6"{Base.Channel{Main.System}}(##225=Base.Channel{Main.System}(cond_take=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), cond_wait=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), cond_put=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), state=:open, excp=nothing, data=Array{Main.System, (0,)}[], n_avail_items=0, sz_max=9223372036854775807)), rngState0=0xe3398f4220ac9d3c, rngState1=0x899f35f795947f90, rngState2=0x5698c3cbf37a0156, rngState3=0xf106cddea4b9b659, rngState4=0xe358e4a012eb8710, _state=0x00, sticky=false, _isexception=false, priority=0x0000), queue=<circular reference @-4>, storage=nothing, donenotify=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), result=nothing, logstate=nothing, code=Main.var"#5#6"{Base.Channel{Main.System}}(##225=Base.Channel{Main.System}(cond_take=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), cond_wait=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), cond_put=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), state=:open, excp=nothing, data=Array{Main.System, (0,)}[], n_avail_items=0, sz_max=9223372036854775807)), rngState0=0x1aac3ff1d8f43034, rngState1=0x14802f94b541ef20, rngState2=0x7942d7c173e44ced, rngState3=0x8152d63da3f75d6a, rngState4=0x4f888f2347910313, _state=0x00, sticky=false, _isexception=false, priority=0x0000), queue=<circular reference @-3>, storage=nothing, donenotify=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), result=nothing, logstate=nothing, code=Main.var"#5#6"{Base.Channel{Main.System}}(##225=Base.Channel{Main.System}(cond_take=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), cond_wait=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), cond_put=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), state=:open, excp=nothing, data=Array{Main.System, (0,)}[], n_avail_items=0, sz_max=9223372036854775807)), rngState0=0xa11288352b970af6, rngState1=0xe67f45959c2ec6aa, rngState2=0x5193977f5f8481df, rngState3=0xbae5a560fccd6eaa, rngState4=0x0b6cedcb01b03a4a, _state=0x00, sticky=false, _isexception=false, priority=0x0000), queue=<circular reference @-2>, storage=nothing, donenotify=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), result=nothing, logstate=nothing, code=Main.var"#5#6"{Base.Channel{Main.System}}(##225=Base.Channel{Main.System}(cond_take=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), cond_wait=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), cond_put=Base.GenericCondition{Base.ReentrantLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.ReentrantLock(locked_by=nothing, reentrancy_cnt=0x00000000, havelock=0x00, cond_wait=Base.GenericCondition{Base.Threads.SpinLock}(waitq=Base.IntrusiveLinkedList{Task}(head=nothing, tail=nothing), lock=Base.Threads.SpinLock(owned=0)), _=(0, 0, 0))), state=:open, excp=nothing, data=Array{Main.System, (0,)}[], n_avail_items=0, sz_max=9223372036854775807)), rngState0=0x61b03f67d6f89086, rngState1=0x1ee87ddebe294103, rngState2=0xb93d13df070e25f6, rngState3=0x3eacce10f111b1c0, rngState4=0xa05f80d86cbdc2e5, _state=0x00, sticky=false, _isexception=false, priority=0x0000), tail=<circular reference @-2>), storage=Base.IdDict{Any, Any}(ht=Array{Any, (32,)}[
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  :SOURCE_PATH,
  "/tmp/reproducer.jl",
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>,
  #<null>], count=1, ndel=6), donenotify=nothing, result=nothing, logstate=nothing, code=#<null>, rngState0=0x3bdd6b7492f99322, rngState1=0xc820e13302084685, rngState2=0x3393658f2559db6d, rngState3=0xc524859e7b717044, rngState4=0xe358e4a012eb8710, _state=0x00, sticky=true, _isexception=false, priority=0x0000)
==========
"�= z�0H�9MLP�PP"
==========
(0, 0, 0)
==========
0
==========
0
==========
0
==========
~~~~~~~~~~ ptr queue bottom ~~~~~~~~~~

[33573] signal (6.-6): Aborted
in expression starting at /tmp/reproducer.jl:47
pthread_kill at /lib/x86_64-linux-gnu/libc.so.6 (unknown line)
raise at /lib/x86_64-linux-gnu/libc.so.6 (unknown line)
abort at /lib/x86_64-linux-gnu/libc.so.6 (unknown line)
gc_dump_queue_and_abort at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:1813
gc_mark_outrefs at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:2508 [inlined]
gc_mark_loop_serial_ at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:2677
gc_mark_loop_serial at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:2700
gc_mark_loop at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:2813
_jl_gc_collect at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:3137
ijl_gc_collect at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:3434
maybe_collect at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:935
jl_gc_pool_alloc_inner at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:1291
jl_gc_pool_alloc_noinline at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:1348
jl_gc_alloc_ at /LionelSSDext4/liozou/julia-test-1.10/src/julia_internal.h:477
jl_gc_alloc at /LionelSSDext4/liozou/julia-test-1.10/src/gc.c:3486
ijl_string_to_array at /LionelSSDext4/liozou/julia-test-1.10/src/array.c:289
unsafe_wrap at ./strings/string.jl:100 [inlined]
StringVector at ./iobuffer.jl:32 [inlined]
format at /LionelSSDext4/liozou/julia-test-1.10/usr/share/julia/stdlib/v1.10/Printf/src/Printf.jl:932
#3 at /tmp/reproducer.jl:24
mktemp at ./file.jl:738
mktemp at ./file.jl:736 [inlined]
output at /tmp/reproducer.jl:15 [inlined]
#5 at /tmp/reproducer.jl:34
unknown function (ip: 0x1f5f4ef5fa52)
_jl_invoke at /LionelSSDext4/liozou/julia-test-1.10/src/gf.c:2894
ijl_apply_generic at /LionelSSDext4/liozou/julia-test-1.10/src/gf.c:3076
jl_apply at /LionelSSDext4/liozou/julia-test-1.10/src/julia.h:1982
start_task at /LionelSSDext4/liozou/julia-test-1.10/src/task.c:1238
Allocations: 1520729 (Pool: 1519177; Big: 1552); GC: 1
```

</details>

Across the minimization I have seen other kinds of crashes such as segmentation faults with backtraces pointing to `gc_mark_outrefs`, and segfaults without backtraces.

Might or might not be related to other reported crashes occuring on 1.10 i.e. #50705, #52032, #51792, #51800, #52200.



CC: @pchintalapudi, @gbaraldi.
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `aef528d32a6291ce82452c3a1ff1fa56ccf17641` and the full history behind it is present.
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
