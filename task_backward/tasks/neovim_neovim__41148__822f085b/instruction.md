# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`vim.fn.bufload()` + `vim.cmd("e")` spuriously marks buffer as `modified` on nightly

### Problem

Calling `vim.fn.bufload()` followed by `vim.cmd("e <file>")` marks the buffer as `modified = true` on nightly. The same sequence produces `modified = false` on stable.

I am not sure whether this is an intentional behavior change in nightly or an unintended side effect of an internal refactor. If it is intentional, I would like to understand the correct way to programmatically load a buffer in the
background without it becoming spuriously modified, since `bufload()` is the documented API for this use case and there does not seem to be a clean alternative that avoids the issue.


### Steps to reproduce

Save the following as `/tmp/test_bufload.lua` and run with:

```bash
# stable — expected: no modified
nvim --clean -u /tmp/test_bufload.lua

# nightly — actual: modified = true
nvim --clean -u /tmp/test_bufload.lua
```

```lua
local tmpfile = vim.fn.tempname() .. ".lua"
vim.fn.writefile({ "dihina2 saya diam, kali ini saya akan lawan!" }, tmpfile)

local bufnr = vim.fn.bufadd(tmpfile)
local before_load = vim.bo[bufnr].modified

vim.fn.bufload(bufnr)
vim.cmd("e " .. tmpfile)

local after_load = vim.bo[bufnr].modified
local loaded = vim.api.nvim_buf_is_loaded(bufnr)

print(string.format("file      : %s", tmpfile))
print(string.format("bufnr     : %d", bufnr))
print(string.format("is_loaded : %s", tostring(loaded)))
print(string.format("modified before bufload : %s", tostring(before_load)))
print(string.format("modified after  bufload : %s", tostring(after_load)))

if after_load and not before_load then
	print("")
	print("[BUG] buffer marked as modified after bufload + e")
	print("      expected: modified should remain false")
else
	print("")
	print("[OK] no spurious modified flag")
end
```

## Additional context
- `bufload()` alone without `vim.cmd("e")` does **not** trigger the issue
- `noautocmd call bufload(bufnr)` does **not** reliably prevent it
- The only workaround found so far is to avoid `bufload()` entirely and use `bufadd()` instead, but this means the buffer is never loaded until the user opens it manually, which is not always acceptable

### Expected behavior

```
modified before bufload : false
modified after  bufload : false

[OK] no spurious modified flag
```

### Nvim version (nvim -v)



### Vim (not Nvim) behaves the same?

no

### Operating system/version

Linux

### Terminal name/version

N/A. reproducible with `--clean`

### $TERM environment variable

N/A

### Installation

Built from source / nightly appimage
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `21a0227d2f654ddc568c3733e72150021cd84a6b` and the full history behind it is present.
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
