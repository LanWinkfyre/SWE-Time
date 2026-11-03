# Locate the commit that introduced this regression

A regression was reported against `zed-industries/zed`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Project panel shows all files as "ignored" when an ancestor matches the global gitignore

If you have cloned this repository to a parent path that looks like `~/src/github.com/git-industries/zed`, all files will be visualized in Zed's project panel as "ignored" (dark grey).

### Reproduction steps

1. Add `*.com` to your global gitignore
2. `git init` a repo with a `*.com` parent, for example: 

    ```console
    $ mkdir -p ~/zed-example.com/src
    $ git -C ~/zed-example.com/src git init
    $ zed ~/zed-example.com/src 
     ```
3. All files in the project pane will be dark grey, indicating they are all ignored (which is false)


### Current vs. Expected behavior

<img width="1372" height="1035" alt="Image" src="https://github.com/user-attachments/assets/3c36e673-0ce9-46c4-b471-f2a5f257e56d" />

`.gitignore` and `commited` files should be light grey, not dark, like `ignored`.

### Root Cause

My global `core.excludesfile` (`~/.config/git/gitignore`) contains: `*.com`

With no trailing slash, this pattern matches files and directories named *.com including a parent ancestor of the repo path (`github.com`) matches it. 

Git itself is unaffected, since it only matches ignore patterns against paths inside the repo's working tree, never against ancestors above the repo root (confirmed via git status and git check-ignore -v, both correct). 

This is purely a Zed bug.

### Regression

 In `crates/worktree/src/ignore.rs`, `IgnoreStack::is_abs_path_ignored`, the Global arm now reads:

```rust
  // crates/worktree/src/ignore.rs:88-93
  if let Ok(relative_path) = abs_path.strip_prefix(repo_root) {
      combined_path = ignore.path().join(relative_path);
      &combined_path
  } else {
      abs_path
  }
```

 



### Zed version and system specs

Zed: 1.12.0
OS: macOS 26.5.2
Memory: 16 GiB
Arch: arm64

### Attach Zed log file

_No response_

### Relevant Zed settings

_No response_

### Relevant Keymap

_No response_

### (for AI issues) Model provider details

_No response_

### If you are using WSL on Windows, what flavor of Linux are you using?

None
```

## What you have

- `/testbed/repo` is a git clone of `zed-industries/zed` truncated just after the regression was
  reported.  `HEAD` is `c214057e086517920b214800725c5d16294ddf0d` and the full history behind it is present.
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
