# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Pre-push CLI compiler cache repeatedly hashes the entire dependency tree

## Problem

The pre-push `TypeScript (CLI)` check can take 8–10 minutes, even when the direct TypeScript check completes in approximately 1–2 minutes.

The delay primarily comes from `scripts/checks/cached-command.mts`, not TypeScript. Before running the compiler, the wrapper recursively reads and hashes repository inputs, generated outputs, and both dependency trees. After a successful compiler run, it repeats the complete fingerprint.

A typical checkout currently includes approximately:

- 35,500 files under the root and plugin dependency trees.
- 546 MB of installed dependencies.
- 5,000 TypeScript files in the CLI type-check program.

The fingerprint also includes `HEAD` and `origin/main`. Every commit, rebase, merge, or base refresh therefore invalidates the cached result, even when the compiler inputs have identical contents. This makes cache reuse unlikely during the pre-push workflow it is intended to accelerate.

## Current behavior

For `tsc-cli`, the wrapper performs this sequence:

1. Discover tracked and untracked repository files.
2. Read and hash source, tests, scripts, tools, agent files, and configuration.
3. Recursively read and hash both `node_modules` trees.
4. Hash Node.js, npm, resolved executables, and generated output directories.
5. Include `HEAD` and `origin/main` in the fingerprint.
6. Run `tsc -p tsconfig.cli.json --incremental`.
7. Repeat the complete filesystem fingerprint.
8. Write a successful validation receipt only when both fingerprints match.

The hook passes no changed filenames. The TypeScript configuration includes the complete CLI, test, script, tool, Hermes, and E2E TypeScript surface.

## Expected behavior

The validation cache should preserve its current source, dependency, executable, configuration, and environment integrity guarantees without repeatedly reading every unchanged dependency file.

An unchanged checkout should complete fingerprint validation in seconds. A Git commit or `origin/main` update should not invalidate the compiler result when all compiler inputs remain byte-for-byte identical.

## Proposed direction

Persist a file-digest index in the existing Git validation-cache directory.

Cache each content digest against the file's canonical path and stable filesystem identity:

- Device.
- Inode.
- File type and mode.
- Size.
- Modification time.
- Change time.

Reuse a cached digest only when the complete identity still matches. Read and hash the file again whenever any identity field changes.

Additional changes:

- Remove `HEAD` and `origin/main` from the compiler-result fingerprint. Relevant file contents are already fingerprinted.
- Reuse unchanged file digests during pre-check and post-check validation.
- Preserve no-follow file opens and before/during/after identity checks.
- Preserve symbolic-link destination hashing and external or cyclic directory rejection.
- Preserve command, environment, platform, architecture, Node.js, npm, resolved executable, configuration, dependency-content, and output identity.
- Prune stale digest-index entries with a bounded policy.
- Report separate timings for discovery, hashing, compiler execution, and post-check verification.

Do not replace dependency-content validation with lockfile-only, package-manifest-only, or timestamp-only trust.

## Acceptance criteria

- [ ] An unchanged dependency tree does not require rereading every dependency file.
- [ ] A new Git commit with identical compiler inputs can reuse the successful result.
- [ ] An `origin/main` update with identical compiler inputs does not invalidate the result.
- [ ] A changed source, test, configuration, dependency, or compiler executable invalidates the applicable cached digest.
- [ ] File type, mode, inode, size, modification-time, or change-time changes invalidate the cached digest.
- [ ] A file that changes during hashing prevents cache publication.
- [ ] A compiler input that changes during execution prevents cache publication.
- [ ] Malformed, missing, or unsafe digest-index state causes fresh validation.
- [ ] Symbolic-link and external-directory protections remain fail-closed.
- [ ] External Node loaders and execution overrides continue to disable result reuse.
- [ ] Tests cover cold-cache, warm-cache, invalidation, concurrent-change, and unsafe-cache cases.
- [ ] The PR records cold and warm timings on the same checkout.
- [ ] The warm `tsc-cli` fingerprint path completes in seconds rather than minutes on the measured checkout.
- [ ] The direct TypeScript diagnostics and exit status remain unchanged.

## Measurement notes

Measure these phases independently:

- Repository input discovery.
- Source and configuration hashing.
- Dependency hashing.
- Compiler execution.
- Post-check verification.
- Total wrapper duration.

Compare cold and warm runs against the same commit, dependency installation, environment, and generated outputs. Do not report compiler time as total cache-wrapper time.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a05d1f238f84e59e6d4fbdc30e547ec7281772c4`.  There
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
{"case_id": "NVIDIA_NemoClaw__11782__a05d1f2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
