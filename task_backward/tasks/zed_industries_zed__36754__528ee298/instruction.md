# Locate the commit that introduced this regression

A regression was reported against `zed-industries/zed`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
LSPs no longer working (macOS 26 Tahoe)

### Summary

<!-- Begin your issue with a one sentence summary -->
Not a single LSP is working since I updated Zed.

### Description
<!--  Describe with sufficient detail to reproduce from a clean Zed install.
  - Any code must be sufficient to reproduce (include context!)
  - Code must as text, not just as a screenshot.
  - Issues with insufficient detail may be summarily closed.
-->

I primarily write in Rust and Typescript, since I updated Zed not a single LSP is working, I don't see any particular error, there is just nothing happening, no code intelligence, no linter, rust analyzer doesn't event try to run.
I also noticed that saving is taking a long time.

Steps to reproduce: None, literally

The only logs I could find that may or may not be useful are

<details><summary>Zed log</summary>

```
2025-08-22T07:17:22-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:17:22-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:17:35-07:00 INFO  [gpui::arena] increased element arena capacity to 4096kb
2025-08-22T07:17:36-07:00 INFO  [workspace] open paths ["/Users/remikalbe/.config/zed/settings.json"]
2025-08-22T07:18:08-07:00 WARN  [editor] timed out waiting for formatting
2025-08-22T07:18:09-07:00 INFO  [project::lsp_store] attempting to start language server "biome", path: "/Users/remikalbe/Git/github.com/remi-boo", id: 7
2025-08-22T07:18:09-07:00 INFO  [project::lsp_store] attempting to start language server "vtsls", path: "/Users/remikalbe/Git/github.com/remi-boo", id: 8
2025-08-22T07:18:09-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:18:09-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:18:09-07:00 INFO  [project::prettier_store] Initializing default prettier with plugins {}
2025-08-22T07:18:09-07:00 INFO  [project::prettier_store] Installing default prettier and plugins: [("prettier", "3.6.2")]
2025-08-22T07:18:10-07:00 INFO  [project::prettier_store] Initialized default prettier with plugins: {}
2025-08-22T07:18:20-07:00 INFO  [editor] Failed to determine selections from before format. Falling back to selections when format was initiated
2025-08-22T07:18:23-07:00 INFO  [editor] Failed to determine selections from before format. Falling back to selections when format was initiated
2025-08-22T07:18:23-07:00 WARN  [editor] timed out waiting for formatting
2025-08-22T07:18:26-07:00 WARN  [editor] timed out waiting for formatting
2025-08-22T07:18:28-07:00 WARN  [editor] timed out waiting for formatting
2025-08-22T07:18:29-07:00 INFO  [project::lsp_store] attempting to start language server "biome", path: "/Users/remikalbe/Git/github.com/remi-boo", id: 9
2025-08-22T07:18:29-07:00 INFO  [project::lsp_store] attempting to start language server "vtsls", path: "/Users/remikalbe/Git/github.com/remi-boo", id: 10
2025-08-22T07:18:29-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:18:29-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:18:58-07:00 INFO  [db] Opening database /Users/remikalbe/Library/Application Support/Zed/db/0-stable/db.sqlite

```

```
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] attempting to start language server "json-language-server", path: "/Users/remikalbe/Git/github.com/remi-boo", id: 1
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] attempting to start language server "package-version-server", path: "/Users/remikalbe/Git/github.com/remi-boo", id: 2
2025-08-22T07:14:50-07:00 INFO  [project::debugger::breakpoint_store] Finish deserializing breakpoints & initializing breakpoint store
2025-08-22T07:14:50-07:00 INFO  [project::debugger::breakpoint_store] Finish deserializing breakpoints & initializing breakpoint store
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] attempting to start language server "rust-analyzer", path: "/Users/remikalbe/Git/github.com/experiments/rust-heterogeneous-collections", id: 3
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
2025-08-22T07:14:50-07:00 INFO  [project::lsp_store] Refreshing workspace configurations for servers {}
```

</details>

### Zed Version and System Specs

Zed: v0.200.4 (Zed) 
OS: macOS 26.0.0   <----------- Tahoe Beta
Memory: 64 GiB
Architecture: aarch64

Here is the final result of the bisect
```

## What you have

- `/testbed/repo` is a git clone of `zed-industries/zed` truncated just after the regression was
  reported.  `HEAD` is `3d2fa72d1fcf177e2beee1433c97e3bfa7adc09a` and the full history behind it is present.
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
