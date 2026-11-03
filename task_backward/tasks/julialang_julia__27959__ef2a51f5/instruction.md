# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
at-testset messes with linenumbers

I am pretty sure this has happened during the last week or so but haven't bisected yet, maybe someone has a guess before I start doing that? Consider e.g.
```
shell> cat bug.jl
using Test

let
    [1, 2] + 2
end

@testset begin
    [1, 2] + 2
end

julia> include("bug.jl")
┌ Warning: `a::AbstractArray + b::Number` is deprecated, use `a .+ b` instead.
│   caller = top-level scope at bug.jl:4
└ @ Core /home/fredrik/bug.jl:4
┌ Warning: `a::AbstractArray + b::Number` is deprecated, use `a .+ b` instead.
│   caller = macro expansion at bug.jl:1090 [inlined]
└ @ Core /home/fredrik/bug.jl:1090
Test Summary: |
test set      | No tests
Test.DefaultTestSet("test set", Any[], 0, false)
```

Funny enough I got L1090 in a big package too, what does that constant mean? :thinking:
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `feaee9ebbc22b04d1fe9a4fbe74e36c317b71046` and the full history behind it is present.
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
