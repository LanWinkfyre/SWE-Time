# Locate the commit that introduced this regression

A regression was reported against `JuliaLang/julia`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression when using AMDGPU and CUDA in same session

When loading AMDGPU.jl and CUDA.jl (in that order) on Julia master breaks usage of AMDGPU. It appears that when AMDGPU calls into GPUCompiler's `cached_compilation` function, and various GPUCompiler interface functions are called (which have overloads defined in AMDGPU), those interface function calls fall back to their non-specialized base-case method defined in GPUCompiler. Specifically, the call:

`GPUCompiler.runtime_module(job)`

where `job` is a:

`GPUCompiler.CompilerJob{GPUCompiler.GCNCompilerTarget, AMDGPU.Compiler.ROCCompilerParams}`

does not call the method https://github.com/JuliaGPU/AMDGPU.jl/blob/bf66efcc5541319ae44d3ff45669abebb133d421/src/compiler.jl#L59, but instead calls https://github.com/JuliaGPU/GPUCompiler.jl/blob/18163a561a169934844d493e4fcd3238439c3965/src/interface.jl#L188.

I can use reflection within GPUCompiler to see that AMDGPU's method does in fact exist and matches the signature for `runtime_module` called with `job`.

If CUDA is not loaded, or before CUDA is loaded, the GPUCompiler overloads in AMDGPU are called correctly. Loading CUDA before AMDGPU also avoids the problem.

`git bisect` points to:



The commit immediately prior does not exhibit the problematic behavior.

Currently the failing AMDGPU code paths can't be exercised without access to a supported AMD GPU; I am going to implement a way to call the desired methods without hardware access, as well as an MWE, to make it easier to reproduce.

@vtjnash
```

## What you have

- `/testbed/repo` is a git clone of `JuliaLang/julia` truncated just after the regression was
  reported.  `HEAD` is `48abb7206d243decca0c4e93eb71db613cd5032b` and the full history behind it is present.
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
