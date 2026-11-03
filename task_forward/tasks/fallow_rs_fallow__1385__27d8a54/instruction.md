# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
ignorePatterns: leading "./" silently fails to match (entry patterns already normalize it)

## Summary

A `fallow.json` `ignorePatterns` entry written with a leading `./` (e.g. `./src/data/cards`) silently does not match, so those files are still analyzed. Dropping the `./` (`src/data/cards`) works. There is no error or warning, so it reads as "the ignore did nothing."

Surfaced in a real walkthrough (Web Dev Simplified, "This Tool Forces AI To Write Good Code"): the reviewer added `./source/data/productinfo` to `ignore`, saw it not take effect on camera, and only got it working after removing the `./`.

## Root cause

`ignorePatterns` are compiled straight into globset without normalizing a leading `./`:

`crates/config/src/config/resolution.rs:263`
```rust
fn compile_ignore_patterns(ignore_patterns: &[String]) -> GlobSet {
    let mut ignore_builder = GlobSetBuilder::new();
    for pattern in ignore_patterns {
        ignore_builder.add(
            Glob::new(pattern).expect("ignorePatterns entry was validated at config load time"),
        );
    }
    ...
}
```

Candidate paths are matched as project-root-relative (`src/...`, via `strip_prefix(root)` in `crates/core/src/discover/walk.rs`), and globset compiles with `literal_separator(true)`, so a pattern containing `./` never matches.

This is exactly the bug already fixed for entry patterns, which DO normalize:

`crates/core/src/plugins/mod.rs:183`
```rust
fn normalize_entry_pattern(pattern: String) -> String {
    pattern
        .strip_prefix("./")
        .map(str::to_owned)
        .unwrap_or(pattern)
}
```

Ignore patterns just never got the same treatment.

## Proposed fix (S)

- Mirror `normalize_entry_pattern` in `compile_ignore_patterns`: strip a leading `./` before `Glob::new`.
- Check the sibling `compile_ignore_unresolved_imports` just below it for the same gap.
- Add a regression test next to the existing ignore-pattern tests in `crates/core/src/discover/walk.rs` covering a `./`-prefixed entry.
- Optional: note in the config docs that `ignorePatterns` are root-relative (no `./` needed).

## Acceptance

- `ignorePatterns: ["./foo/**"]` excludes the same files as `["foo/**"]`.
- Regression test covers the `./` case.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `27d8a5402aededded27235521e4ad04400b59585`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fallow_rs_fallow__1385__27d8a54",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
