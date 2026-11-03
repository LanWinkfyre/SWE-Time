# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`InspectTree` stack overflow

### Problem

On current neovim nightly, doing `nvim --clean src/nvim/statusline.c` into `:InspectTree` leads to stack overflow


 

### Steps to reproduce

- `nvim --clean src/nvim/statusline.c`
- `:InspectTree`

### Expected behavior

To not show the error message:
```
Error executing Lua callback: stack overflow
stack traceback:
        [C]: in function 'id'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:46: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        ...
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:48: in function 'traverse'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:115: in function 'new'
        /usr/local/share/nvim/runtime/lua/vim/treesitter/dev.lua:269: in function 'inspect_tree'
        /usr/local/share/nvim/runtime/lua/vim/treesitter.lua:494: in function 'inspect_tree'
        /usr/local/share/nvim/runtime/plugin/nvim.lua:18: in function </usr/local/share/nvim/runtime/plugin/nvim.lua:9>
```

### Neovim version (nvim -v)



### Vim (not Nvim) behaves the same?

No

### Operating system/version

Linux 6.5.2-arch1-1

### Terminal name/version

Kitty 0.29.2

### $TERM environment variable

xterm-kitty

### Installation

Build from source
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `bc67cf3ccdf935a0e2974fbbe5557a3d24931c54` and the full history behind it is present.
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
