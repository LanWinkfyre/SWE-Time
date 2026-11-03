# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Strange code hang in combination with @generated functions

This is the weirdest problem I have ever encountered in several years of using Julia and has taken me several hours to track down to debug and distill a minimal working example:

This came up in the context of an unregistered package of mine for working with strided array views (WIP, https://github.com/Jutho/Strided.jl), and only started to be a problem when I pulled the latest master today (I guess before I was working on master from a few days ago, at most two weeks or so). 

```julia
module Strided
	struct StridedView{T,N,A<:DenseArray{T}} <: DenseArray{T,N}
		parent::A
		size::NTuple{N,Int}
		strides::NTuple{N,Int}
	end

	function Base.convert(T::Type{<:DenseArray}, a::StridedView)
	end

	@generated function test1(dims::NTuple{N,Int}) where {N}
		loopvars = [gensym() for k = 1:N]
		return :()
	end

	function test2()
	end
end
dims=(1,)
Strided.test1(dims) #-> code hangs
```

The hanging will stop under any of the following modifications:
* remove `function test2() end` such that the generated function is the last in the module. 
* add `@show "hi $N"` as first line of `test1`, however 
    *   the "hi" is important, `@show "$N"` is not sufficient
    *   the display output is important, `t=@elapsed "$N"` is not sufficient but `@time "hi $N"` is, in fact with `@time` the `hi` is not necessary
    *  the macro is important, `println("hi $N")` is not sufficient
* remove the definition of `Base.convert`
* simplify the type definition of `StridedView`
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `f8243b7d203a28c1ac4374f883fcb6d4d9667418` and the full history behind it is present.
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
