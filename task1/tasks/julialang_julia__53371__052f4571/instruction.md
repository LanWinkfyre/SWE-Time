# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
slow subtyping of complex Union

I just ran into an example where precompilation of my package suddenly took forever (usually ~5s, now I terminate it after a minute). I managed to boil it down to the following:

```julia
module precompilationhang

const XorM{X} = Union{<:X,Missing}

struct Type1{P,V<:AbstractVector{P},Vr<:XorM{V},Vc<:XorM{V}}
end

struct Type2{P,
    E1<:(AbstractVector{M} where M<:Type1{P}),
    E2<:(AbstractVector{M} where M<:Type1{P}),
    E3<:(AbstractVector{M} where M<:Type1{P}),
    E4<:(AbstractVector{M} where M<:Type1{P})}
    f1::Vector{E1}
    f2::Vector{E2}
    f3::Vector{Vector{E3}}
    f4::Vector{Vector{E4}}
end

end
```

Precompilation of this tiny package takes about 4:40 minutes.
Trying to simplify it further first looked as if it still has the same issue, but this was merely impatience. For example (all of the examples have just the one thing changed that I mention, the changes don't accumulate):
- `XorM = Union{X,Missing}` takes 13 seconds
- removing just the field `f1` takes 10 seconds
- removing `E1` and `f1` takes 5 seconds
- removing just the `Vc` type parameter from `Type1` takes 2 seconds



> Compared to what? 1.9, 1.10.0?

The example above runs instantaneously on 1.9.4 and takes several minutes on 1.10.0 (tested on Windows and Linux). The slowdown also occurs on master.
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `93876c92ed725272d8853d73dc0c3256095f1617` and the full history behind it is present.
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
