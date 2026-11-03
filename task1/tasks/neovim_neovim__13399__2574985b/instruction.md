# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
SIGKILL when run nvim executable during `make` with Apple Clang

- `nvim --version`: Not available
- `vim -u DEFAULTS` (version: ) behaves differently?: Not available
- Operating system/version: macOS v11.0.1 root:xnu-7195.50.7~2/RELEASE_ARM64_T8101 arm64
- Terminal name/version: macOS Terminal.app v2.11 (440) 
- `$TERM`: shell v3.1.2, xterm-256color

-On Mac Mini M1 (Apple Silicon)- Does not relate to the issue.

### Steps to reproduce using `nvim -u NORC`

1. Checkout the repository on the master branch
2. Install dependencies
3. Run `make`

### Actual behaviour

Compilation failed due to `SIGKILL` on `nvim` executable launch:

```
[2/4] Generating pack/dist/opt/vimball/doc/tags
FAILED: runtime/pack/dist/opt/vimball/doc/tags 
cd /Users/dive/Projects/github/neovim/build/runtime/pack/dist/opt/vimball && /opt/local/bin/cmake -E copy_directory /Users/dive/Projects/github/neovim/runtime/pack/dist/opt/vimball /Users/dive/Projects/github/neovim/build/runtime/pack/dist/opt/vimball && /Users/dive/Projects/github/neovim/build/bin/nvim -u NONE -i NONE -e --headless -c helptags\ doc -c quit
/bin/sh: line 1: 48650 Killed: 9               /Users/dive/Projects/github/neovim/build/bin/nvim -u NONE -i NONE -e --headless -c helptags\ doc -c quit
[3/4] Generating pack/dist/opt/matchit/doc/tags
FAILED: runtime/pack/dist/opt/matchit/doc/tags 
cd /Users/dive/Projects/github/neovim/build/runtime/pack/dist/opt/matchit && /opt/local/bin/cmake -E copy_directory /Users/dive/Projects/github/neovim/runtime/pack/dist/opt/matchit /Users/dive/Projects/github/neovim/build/runtime/pack/dist/opt/matchit && /Users/dive/Projects/github/neovim/build/bin/nvim -u NONE -i NONE -e --headless -c helptags\ doc -c quit
/bin/sh: line 1: 48651 Killed: 9               /Users/dive/Projects/github/neovim/build/bin/nvim -u NONE -i NONE -e --headless -c helptags\ doc -c quit
[4/4] Generating doc/tags
FAILED: runtime/doc/tags 
cd /Users/dive/Projects/github/neovim/build/runtime && /opt/local/bin/cmake -E remove doc/* && /opt/local/bin/cmake -E copy_directory /Users/dive/Projects/github/neovim/runtime/doc doc && /Users/dive/Projects/github/neovim/build/bin/nvim -u NONE -i NONE -e --headless -c helptags\ ++t\ doc -c quit
/bin/sh: line 1: 48656 Killed: 9               /Users/dive/Projects/github/neovim/build/bin/nvim -u NONE -i NONE -e --headless -c helptags\ ++t\ doc -c quit
ninja: build stopped: subcommand failed.
make: *** [nvim] Error 1
```

The `nvim` executable is there, but it fails with `SIGKILL` when you try to run it:

```
~/P/g/neovim $ file ./build/bin/nvim
./build/bin/nvim: Mach-O 64-bit executable arm64

~/P/g/neovim $ ./build/bin/nvim
fish: “./build/bin/nvim” terminated by signal SIGKILL (Forced quit)
```

### Expected behaviour

The executable works as expected.

@dive Thanks for confirming (I cannot test Apple silicon myself).

 Would you mind editing the issue title to replace "Apple Silicon (arm64)" with "Apple clang" to make that clear?

I'll have to leave the question how to best fix it to @bfredl...
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `6af64d384f96a69462a2a50dd7054566af98de37` and the full history behind it is present.
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
