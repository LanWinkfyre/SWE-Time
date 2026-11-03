# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
napi-rs: auto-ignore prebuilt platform-binary optionalDependencies in unused-dep analysis

## Summary

napi-rs projects declare one prebuilt binary per platform as `optionalDependencies` (the `@napi-rs/cli` naming: `<pkg>-<platform>[-<libc>]`, e.g. `-darwin-arm64`, `-linux-x64-gnu`, `-win32-x64-msvc`). The napi loader picks the right one at runtime via `require`, so none are imported from source. fallow's unused-dependency analysis therefore flags every platform package as an unused optional dependency.

There is no built-in handling for this today (no napi plugin in the builtin registry; optional deps go through the same path as the rest). Verified in source:

- No napi entry in `crates/core/src/plugins/registry/builtin.rs`
- Optional deps collected identically to other categories in `crates/core/src/analyze/unused_deps.rs:392`
- `ignoreDependencies` is exact-match only (`unused_deps.rs:534`, `d == &dep`), whereas `ignoreUnresolvedImports` compiles globs via globset (`crates/config/src/config/resolution.rs:292`). So the only workaround is enumerating every triple by hand.

## Real-world impact

srcmap (a napi project) currently has to hardcode 14 platform packages in `ignoreDependencies` just to get a clean report:

```json
"@srcmap/codec-darwin-arm64", "@srcmap/codec-darwin-x64",
"@srcmap/codec-linux-arm64-gnu", "@srcmap/codec-linux-arm64-musl",
"@srcmap/codec-linux-x64-gnu", "@srcmap/codec-linux-x64-musl",
"@srcmap/codec-win32-x64-msvc",
"@srcmap/sourcemap-darwin-arm64", ... (7 more)
```

This list has to be maintained by hand every time a target is added or dropped.

## Detection signal

These projects carry the answer in `package.json` already. The `napi` field lists the binary name and the Rust target triples, from which the expected optional-dependency names are fully derivable:

```json
"napi": {
  "binaryName": "srcmap-codec",
  "targets": [
    "x86_64-apple-darwin", "aarch64-apple-darwin",
    "x86_64-unknown-linux-gnu", "x86_64-unknown-linux-musl",
    "aarch64-unknown-linux-gnu", "aarch64-unknown-linux-musl",
    "x86_64-pc-windows-msvc"
  ]
}
```

`aarch64-apple-darwin` maps to `<scope>/<binaryName-base>-darwin-arm64`, etc., the same triple to-platform mapping `@napi-rs/cli` uses when it generates the optionalDependencies.

## Possible approaches (whatever fits best)

1. **napi-rs plugin** (`area:plugins`): when a package has a `napi` field, derive the platform package names from `napi.targets` and treat them as tooling/always-used so they are never flagged.
2. **Built-in heuristic**: treat an optionalDependency as a napi prebuild when its name is `<own-package>-<known-platform-triple>` and its own package.json is os/cpu-constrained with no source imports.
3. **Lighter alternative**: support glob patterns in `ignoreDependencies` (align it with `ignoreUnresolvedImports`) so a single `@scope/pkg-*` entry covers all triples. Useful regardless of 1/2.

Happy to dogfood any of these against srcmap and oxc-coverage-instrument (both napi projects).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e6d7e8316474e27dcd4ba3f616c5ca494b8df92a`.  There
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
{"case_id": "fallow_rs_fallow__1164__e6d7e83",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
