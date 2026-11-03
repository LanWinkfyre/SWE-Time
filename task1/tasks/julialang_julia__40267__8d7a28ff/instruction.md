# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Multiarg `eachindex` slower on 1.6

```julia
function f!(ue, u, idxs)
    @inbounds for i in eachindex(ue)
        ue[i] = u[idxs[i]]
    end
    return ue
end
function g!(ue, u, idxs)
    @inbounds for i in eachindex(ue, idxs)
        ue[i] = u[idxs[i]]
    end
    return ue
end

using BenchmarkTools
u = rand(1000);
ue = rand(30);
idxs = collect(1:30);

@btime f!($ue, $u, $idxs);
@btime g!($ue, $u, $idxs);
```

1.6.0:
```julia
julia> @btime f!($ue, $u, $idxs);
  13.534 ns (0 allocations: 0 bytes)

julia> @btime g!($ue, $u, $idxs);
  19.248 ns (0 allocations: 0 bytes)
```
1.5.4:
```julia
julia> @btime f!($ue, $u, $idxs);
  13.878 ns (0 allocations: 0 bytes)

julia> @btime g!($ue, $u, $idxs);
  14.042 ns (0 allocations: 0 bytes)
```

Not very unexpected:
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `06e7ee6ce8277035cc4ae6d0a365698f2f5bb347` and the full history behind it is present.
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
