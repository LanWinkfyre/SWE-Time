# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[clangd] Segfault when module imported through a header

I'm encountering a crash on Windows when running `clangd` on a source file that imports a named module through a header:


### Steps to reproduce
1. Create a static library target with a single implementation file containing `export module X;`
2. Create a header containing `import X;` (important, directly using `import` in the source file does not cause a crash)
3. Create an executable target linking against the static library - single source file including the header
4. Run CMake configure to get `compile_commands.json`
5. Run `clangd` on the source file of the executable target with `--experimental-modules-support`

I've also made a repository at https://github.com/itzexpoexpo/clangd-crash-repro.git that has the exact CMake setup I've used to reproduce this.

### Notes
Happens at least since 22.1.0, also tested 21.1.8 which doesn't crash on these specific steps, but still crashes on my actual codebase in a very similar fashion, unsure if relevant.



I hit this issue too separately (would occasionally see `Assertion failed: (ModuleFileIndex <= MF.TransitiveImports.size()),
  function get, file ASTReader.cpp, line 1103`).

 cc @jansvoboda11
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `cc613052fd6afe2e3522c18234e382588069441d` and the full history behind it is present.
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
