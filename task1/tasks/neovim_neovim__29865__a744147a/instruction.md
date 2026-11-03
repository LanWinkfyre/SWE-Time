# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
lsp filewatcher not work with some glob pattern

### Problem

https://github.com/Decodetalkers/neocmakelsp/blob/master/src/languageserver.rs#L280-L293

I have registered such kind of filewatcher. every time files under the project, like `buiild/CMakeCache.txt` is changed, lsp will read the file and publish some diagnose. it used to work on 0.9, but now it will only react to `CMakeCache.txt` such kind of file, which is on the top of the file. I have tried vscode, vscode works well, so I think it maybe a bug.. 

my config is 

```lua
local configs = require("lspconfig.configs")
local opts = {
    capabilities = {
        workspace = {
            didChangeWatchedFiles = {
                dynamicRegistration = true,
                relative_pattern_support = true,
            },
        },
        textDocument = {
            completion = {
                completionItem = {
                    snippetSupport = true
                }
            }
        }
    },
    on_attach = on_attach,
}
if persettings and persettings.lsp and persettings.lsp.neocmake then
    opts = persettings.lsp.neocmake
end

nvim_lsp.neocmake.setup(opts)
```

### Steps to reproduce

config neocmake like the above way. create a new cmake project, use git init, init the git repo. 

Then write the min thing

```cmake
cmake_minimum_required(VERSION 3.27)
project(AA)

find_package(ddggf REQUIRED)
```

here the `ddggf` package is not exist, run

```bash
cmake -B build
```

cmake will report error, and generate  `build/CMakeCache.txt`, and neocmakelsp will report warning on `ddggf`, but neocmakelsp does not receive any file changes. 


### Expected behavior

"**/CMakeCache.txt",such kind of glob can be support with filewatcher

### Neovim version (nvim -v)

v0.10.1

### Vim (not Nvim) behaves the same?

no

### Operating system/version

archlinux

### Terminal name/version

konsole/24.05.2

### $TERM environment variable

xterm-256color

### Installation

from the repo of archlinux
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `bb185d63ab86e305e35603297a88c0ec8fba27ae` and the full history behind it is present.
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
