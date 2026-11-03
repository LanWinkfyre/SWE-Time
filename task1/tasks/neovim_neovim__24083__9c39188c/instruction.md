# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
### Problem

When placing the cursor over `{` with matchparen enabled, the fold line is highlighted with `MatchParen`



![image](https://github.com/neovim/neovim/assets/7904185/7f9578ff-8596-48e9-a648-1c8ba4757b14)


### Steps to reproduce

1. Create `luarc.json`:
```json
{
    "workspace.library": [
        "/Users/lewrus01/.data/nvim/site/pack/packer/opt/neodev.nvim/types/nightly",
        "/usr/local/share/nvim/runtime/lua",
        "/Users/lewrus01/projects/packer.nvim/lua",
    ],
    "workspace.checkThirdParty": false
}
```
2. `nvim -u NONE --clean .luarc.json --cmd ':set fdm=syntax'`

3. Should see:
![image](https://github.com/neovim/neovim/assets/7904185/c6167e20-32f0-47d2-9ffe-44efdbae3d6d)




### Expected behavior

![image](https://github.com/neovim/neovim/assets/7904185/e64febb1-4f8d-457f-b099-ef2d7cf55ba6)


### Neovim version (nvim -v)



### Vim (not Nvim) behaves the same?

no

### Operating system/version

macOS 13.4

### Terminal name/version

kitty

### $TERM environment variable

xterm-kitty

### Installation

Source
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `8d4a53fe6e20652946948170f2436ec520f9bdfe` and the full history behind it is present.
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
