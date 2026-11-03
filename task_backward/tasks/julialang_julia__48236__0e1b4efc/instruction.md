# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Don't unroll nested loops too aggressively

In this function:

```julia
using Base.Threads
using Base.Cartesian

swap4(nt::NTuple{8,T}) where T = @inbounds (nt[5], nt[6], nt[7], nt[8], nt[1], nt[2], nt[3], nt[4])
swap2(nt::NTuple{8,T}) where T = @inbounds (nt[3], nt[4], nt[1], nt[2], nt[7], nt[8], nt[5], nt[6])
swap1(nt::NTuple{8,T}) where T = @inbounds (nt[2], nt[1], nt[4], nt[3], nt[6], nt[5], nt[8], nt[7])

function v5!(res, data_, n)
    @boundscheck checkbounds(res, 1:n)
    @boundscheck checkbounds(data_, 1:n)
    blocksize = 8
    nblocks = div(n + blocksize - 1, blocksize)
    colsize = nblocks*blocksize

    data = Matrix{Float32}(undef, colsize, n)
    tran = Matrix{Float32}(undef, colsize, n)
    for row in 1:n
        @inbounds for col in 1:colsize
            data[col,row] = col <= n ? data_[col,row] : Inf32
            tran[col,row] = col <= n ? data_[row,col] : Inf32
        end
    end

    for row in 1:blocksize:n
        @inbounds for col in 1:blocksize:n
            # v_1, v_2, ..., v_8
            @nexprs 8 l -> v_{l-1} = ntuple(_ -> Inf32, 8)

            for block in 1:n
                a_0 = @ntuple 8 blockidx -> data[row+blockidx-1, block]
                b_0 = @ntuple 8 blockidx -> tran[col+blockidx-1, block]
                a_4 = swap4(a_0)
                a_2 = swap2(a_0)
                a_6 = swap2(a_4)
                b_1 = swap1(b_0)
                @nexprs 4 l -> begin
                    @nexprs 2 k -> begin
                    v_{2*(l-1)+k-1} = @fastmath min.(v_{2*(l-1)+k-1}, a_{2*(l-1)} .+ b_{k-1})
                end
                end
            end

            vv = @ntuple 8 idx -> iseven(idx) ? swap1(v_{idx-1}) : v_{idx-1}

            @nexprs 8 ib -> begin
            @nexprs 8 jb -> begin
                i = ib + col - 1
                j = jb + row - 1
                if i <= n && j <= n
                    idx = xor(ib-1,jb-1)+1
                    el = vv[idx][ib]
                    res[j, i] = el
                end
            end
            end
        end
    end
end
```

I'd expect (at most!) the `for block in 1:n` to unroll a bit (by a factor of 4), but taking a look at `@code_typed`, we can see that all the nice tuple operations (that could just map to SIMD instructions directly!) got taken apart into individual element calls. This is problematic, because LLVM then ends up unrolling this unrolled inner loop again and storing pretty much everything on the stack, working on blocks of 256*8 = 2048 `float` at a time, instead of keeping the assembly small & tight, working on "only" 64 elements/8 SIMD vectors at a time (but with consequently much fewer loads & stores from/to memory - instead of writing to temporaries on the stack, the result can just be written directly to the target memory, never to be touched again).

I don't dare post the output of `@code_typed` here (it's already 1400 slots long) and even less so for the `@code_llvm` and `@code_native` (I had to set my terminal scrollback to 4000 lines to finally see it all), but here's a small script to take a look.

```julia
n = 20
d = rand(Float32, n, n)
r = zeros(Float32, n, n)
@code_typed v5!(r, d, n)
#@code_llvm v5!(r, d, n)
#@code_native v5!(r, d, n)
```

The generated native code is full of 

```asm
	vmovaps	ymmword ptr [rsp + 5376], ymm9  # 32-byte Spill
	vmovaps	ymm2, ymmword ptr [rsp + 64]    # 32-byte Reload
	vaddps	ymm8, ymm2, ymmword ptr [rsp + 512] # 32-byte Folded Reload
	vmovaps	ymm9, ymmword ptr [rsp + 5344]  # 32-byte Reload
	vminps	ymm9, ymm9, ymm8
```

where this ideally should not spill anything. Apologies for the large MWE :) 

As for why I didn't write this with SIMD.jl - I think it'd be a shame to use platform intrinsics here and this ought to be achievable without them. I would have used `VecElement` since that is in `Base`, but that seems to have alignment problems, judging from other issues.
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `a526a4a4b3e9afc648320291c6242d99b364667f` and the full history behind it is present.
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
