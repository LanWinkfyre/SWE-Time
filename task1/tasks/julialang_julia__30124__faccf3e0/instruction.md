# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Performance regression with StaticArray broadcast

EDIT by @maleadt: see https://github.com/JuliaLang/julia/issues/30124#issuecomment-442821432 for a non-CUDAnative specific reproducer.

  If you replace the multiplication line by the next commented one, it works fine.

```julia
using CUDAnative, CuArrays, StaticArrays

Ks = [SMatrix{1, 1, Float64}(rand(1,1))] |> CuArrays.CuArray
fs = [SVector{1, Float64}(rand(1))] |> CuArrays.CuArray

function kernel(fs::AbstractVector{TV}, Ks) where {N, T, TV<:SVector{N,T}}
    i = (blockIdx().x-1) * blockDim().x + threadIdx().x
    m = 2.0
    if i == 1
	    fs[i] = m * (Ks[i] * fs[i])
	    #fs[i] = SVector{1,T}((m,)) .* (Ks[i] * fs[i])
    end
    return
end

@cuda blocks=1 threads=1 kernel(fs,  Ks)

#=
ERROR: InvalidIRError: compiling kernel(CuDeviceArray{SArray{Tuple{3},Float64,1,3},1,CUDAnative.AS.Global}, CuDeviceArray{SArray{Tuple{3,3},Float64,2,9},1,CUDAnative.AS.Global}) resulted in invalid LLVM IR
Reason: unsupported call to the Julia runtime (call to jl_invoke)
Stacktrace:
 [1] Type at broadcast.jl:141
 [2] result_style at broadcast.jl:397
 [3] combine_styles at broadcast.jl:390
 [4] broadcasted at broadcast.jl:1162
 [5] broadcast at broadcast.jl:702
 [6] * at /home/mohd/.julia/packages/StaticArrays/WmJnA/src/linalg.jl:25
 [7] kernel at REPL[18]:5
Stacktrace:
 [1] check_ir(::CUDAnative.CompilerContext, ::LLVM.Module) at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/compiler/validation.jl:123
 [2] #compile#80(::Bool, ::Function, ::CUDAnative.CompilerContext) at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/compiler/driver.jl:74
 [3] compile at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/compiler/driver.jl:49 [inlined]
 [4] #compile#79(::Base.Iterators.Pairs{Union{},Union{},Tuple{},NamedTuple{(),Tuple{}}}, ::Function, ::CUDAdrv.CuDevice, ::Any, ::Any) at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/compiler/driver.jl:28
 [5] compile at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/compiler/driver.jl:16 [inlined]
 [6] macro expansion at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/execution.jl:255 [inlined]
 [7] #cufunction#91(::Base.Iterators.Pairs{Union{},Union{},Tuple{},NamedTuple{(),Tuple{}}}, ::typeof(cufunction), ::typeof(kernel), ::Type{Tuple{CuDeviceArray{SArray{Tuple{3},Float64,1,3},1,CUDAnative.AS.Global},CuDeviceArray{SArray{Tuple{3,3},Float64,2,9},1,CUDAnative.AS.Global}}}) at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/execution.jl:230
 [8] cufunction(::Function, ::Type) at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/execution.jl:230
 [9] top-level scope at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/execution.jl:198
 [10] top-level scope at gcutils.jl:87
 [11] top-level scope at /home/mohd/.julia/packages/CUDAnative/5H3Dk/src/execution.jl:195
=#
```

My `versioninfo()` is:
 

Good luck!



```julia
using StaticArrays # 0.10.0

K = SMatrix{1,1}(rand(1,1))

using InteractiveUtils
versioninfo()
@code_warntype 2.0 * K

using BenchmarkTools
@btime 2.0 * $K
```

Before and after the offending commit:





So not limited to CUDAnative's Julia support, but a serious broadcast/StaticArrays regression instead.
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `038d8665afd2eeeaca81ba5ebd3da1ece40e69bc` and the full history behind it is present.
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
