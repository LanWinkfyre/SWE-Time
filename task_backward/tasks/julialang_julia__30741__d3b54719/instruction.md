# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Infinite recursion in type intersection

 Apologies for not having a MWE, when trying to run `@code_typed` or `@code_warntype` on the last line that triggers the error, I get a `StackOverflowError`.

When I run the following code
```julia
using Pkg
Pkg.activate(".")

pkg"add https://github.com/JuliaAtoms/AtomicLevels.jl.git#revamp"
pkg"add https://github.com/MasonProtter/Symbolics.jl.git"
pkg"add https://github.com/jagot/AngularMomentumAlgebra.jl.git"
pkg"add https://github.com/JuliaApproximation/ContinuumArrays.jl.git"
pkg"add https://github.com/jagot/FiniteDifferencesQuasi.jl.git"
pkg"add https://github.com/jagot/SolverTraces.jl.git"
pkg"add https://github.com/jagot/SCF.jl.git"
pkg"add https://github.com/JuliaAtoms/Atoms.jl.git"

using AtomicLevels
using FiniteDifferencesQuasi

using Atoms
using SCF

rₘₐₓ = 300

nucleus = pc"He"
Z = Atoms.charge(nucleus)
ρ = 0.25
N = ceil(Int, rₘₐₓ/ρ + 1/2)
R=RadialDifferences(N, ρ, Z)

csf = CSF(c"1s2", [IntermediateTerm(T"1S", 0)], [T"1S"])
Atom(R, [csf], nucleus)
```
the last line triggers an infinite recursion in `subtype.c`, which breaks at some point, and then the code continues as nothing happened. On second run in the same Julia instance, the infinite recursion does _not_ occur.



Similar symptoms, not sure if related: #21696, #24254, #24942.

I will try to do a bisect.

I've done the bisect and ended up with the following result:
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `ec807bc01ccd53c4dac07dcce4bfb25a20d38f20` and the full history behind it is present.
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
