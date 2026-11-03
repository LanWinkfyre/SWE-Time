# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Unreachable reached in Atoms.jl yet again

 Will try bisect.

```julia
using Atoms
using SCF
using AtomicLevels
using AtomicPotentials
using FEDVRQuasi

rₘₐₓ, ρ = 10, 0.1
fedvr_order = 10
N = max(ceil(Int, rₘₐₓ/(ρ*fedvr_order)),2)
t = range(0.0, stop=rₘₐₓ, length=N)
R = FEDVR(t, fedvr_order)[:,2:end-1]

nucleus = pc"He"
atom = Atom(R, [spin_configurations(ground_state(nucleus))[1]],
            nucleus, eltype(R))

fock = Fock(atom)
```

Expected output:
```
Fock operator with
- quantum system: Atom{Float64}(R=FEDVR{Float64} basis with 9 elements on 0.0..10.0, restricted to basis functions 2..81 ⊂ 1..82; Z = 2 [helium]; 2 e⁻ ⇒ Q = 0) with 1 Configuration{SpinOrbital}: 1s²
- SCF equations:  
  - Hartree–Fock equation: E|1s₀α⟩ = OrbitalEquation(1s₀α): 
  [1, 1]  =  + 1ĥ₀|1s₀α⟩ + 1r⁻¹×Y⁰(1s₀β,1s₀β)|1s₀α⟩

⟨1s₀α| 𝓗 |1s₀α⟩ = -0.7500000012522258 Ha = -20.408250034074314 eV

  - Hartree–Fock equation: E|1s₀β⟩ = OrbitalEquation(1s₀β): 
  [1, 1]  =  + 1ĥ₀|1s₀β⟩ + 1r⁻¹×Y⁰(1s₀α,1s₀α)|1s₀β⟩

⟨1s₀β| 𝓗 |1s₀β⟩ = -0.7500000012522258 Ha = -20.408250034074314 eV
```
Actual [output.txt](https://github.com/JuliaLang/julia/files/3073313/output.txt)

Environment:
[Project.toml.txt](https://github.com/JuliaLang/julia/files/3073318/Project.toml.txt)
[Manifest.toml.txt](https://github.com/JuliaLang/julia/files/3073317/Manifest.toml.txt)

Thanks @JeffBezanson! I should in general try to simplify my types, hopefully I could lower my compile times as well.

I finally finished the bisect:
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `20834c3176bf1cfd29096f72f49bb63de0d7b02d` and the full history behind it is present.
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
