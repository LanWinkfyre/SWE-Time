# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Apparent mutation within kwarg function

Minimal example
```julia
mutable struct A
  a::Int
end

g(a, b; kw = true) = iszero(a.a) && !b

function repro()
  a = A(0)
  b = iszero(a.a)
  println((; b))
  if g(a, b) else end
  println((; b))
end

repro()
```
output is
```julia
(b = true,)
(b = false,)
```
while on Julia 1.10 we get the expected
```julia
(b = true,)
(b = true,)
```

The buggy behaviour seems to have quite a few prerequisites (any change makes the bug disappear):
1. `A` needs to be mutable (even though it is not mutated explicitly anywhere)
2. `g` needs to take a kwarg (even though it is unused)
3. `g` needs to take both parameters with non-trivial conditions on it
4. the `&&` conditional needs to be in that order (even though it should not matter since the first will be true)
5. the call to `g(a, b)` needs to be within the `if` conditional (even though trivial)

version info:

Additionally I've checked that version 1.12.4 seems to be affected as well.

I suspect it to be due to wrong lowering since `@code_typed` already shows `(b = false,)`:
```julia-repl
julia> @code_typed repro()
CodeInfo(
1 ─ %1 =   builtin (0 === 0)::Bool
│   %2 = %new(@NamedTuple{b::Bool}, %1)::@NamedTuple{b::Bool}
│           invoke Main.println(%2::@NamedTuple{b::Bool})::Any
│   %4 =   builtin (0 === 0)::Bool
└──      goto #3 if not %4
2 ─ %6 = intrinsic Base.not_int(%1)::Bool
└──      goto #4
3 ─      goto #4
4 ┄ %9 = φ (#2 => %6, #3 => false)::Bool
└──      goto #5
5 ─      goto #7 if not %9
6 ─      nothing::Nothing
7 ┄         invoke Main.println((b = false,)::@NamedTuple{b::Bool})::Nothing
└──      return nothing
) => Nothing
```
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `7eb1edb73e09445e89edc96d09e827fa1f2464fd` and the full history behind it is present.
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
