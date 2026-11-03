# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
perf: bound peak parse memory so large repos do not OOM

## Problem

`fallow` reads and parses every discovered source file up front, holding the result for all of them in memory at the same time. In `crates/extract/src/lib.rs`, `parse_all_files` does:

```rust
let modules: Vec<ModuleInfo> = files
    .par_iter()
    .filter_map(|file| parse_single_file_cached(...))
    .collect();
```

Every file's `ModuleInfo` (744 bytes of header plus heap collections for member accesses, line offsets, imports, exports, complexity, and more) stays resident for the whole pipeline (resolution, graph build, dead-code, dupes, health). Peak memory is therefore `O(total source bytes)` held all at once. On a very large repository this is enough to exhaust available RAM and stall before producing output.

This is the root cause behind #1086. The default per-file size skip that shipped for #1086 mitigates the single-pathological-file case, but it does not address the case where many ordinary files sum to more memory than the machine has.

## Proposed direction

Make peak parse memory `O(in-flight)` rather than `O(total)`:

- Drop or compact the per-file data that downstream passes do not need after extraction, so retained memory per file shrinks.
- Or chunk/stream the parse with back-pressure so only a bounded working set is resident at once.

Either approach needs to preserve identical analysis results on the benchmark fixtures (the resolution and graph layers must see the same per-file data they see today).

## Acceptance

- Peak RSS on a large fixture is materially lower and grows sub-linearly with total source size.
- Issue counts are byte-identical on all benchmark fixtures.
- No regression on small/medium-repo wall time.

Size: L. Tracks the durable fix for #1086 (which stays open against this).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `70d5167074917d27e02531e8a669463bb52784c5`.  There
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
{"case_id": "fallow_rs_fallow__1104__70d5167",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
