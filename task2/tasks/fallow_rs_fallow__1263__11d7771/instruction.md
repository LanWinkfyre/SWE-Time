# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
fallow coverage analyze --cloud: tolerate null caller_count/cyclomatic/owner_count in runtime-context

The cloud runtime-context response is moving from placeholder numbers to an explicit "not measured" for the blast-radius caller fields and the importance complexity/ownership fields. When the caller-graph (blast-radius) or the complexity/CODEOWNERS inputs (importance) are unavailable, the cloud will emit `null` instead of a misleading `0`/`1`:

- `blast_radius[].caller_count`
- `blast_radius[].caller_count_weighted_by_traffic`
- `importance[].cyclomatic`
- `importance[].owner_count`

The current deserializer in `crates/cli/src/coverage/cloud_client.rs` declares these as non-`Option` integers with no `#[serde(default)]`:

```rust
pub struct CloudRuntimeBlastRadiusEntry {
    // ...
    pub caller_count: u32,
    pub caller_count_weighted_by_traffic: u64,
    // ...
}
pub struct CloudRuntimeImportanceEntry {
    // ...
    pub cyclomatic: u32,
    pub owner_count: u32,
    // ...
}
```

`serde` cannot deserialize `null` (or an absent field) into `u32`/`u64`, so `fallow coverage analyze --cloud` will fail to parse the response once the cloud ships the change.

### Fix
Make the four fields tolerant and render "not measured":

```rust
#[serde(default)]
pub caller_count: Option<u32>,
#[serde(default)]
pub caller_count_weighted_by_traffic: Option<u64>,
// ...
#[serde(default)]
pub cyclomatic: Option<u32>,
#[serde(default)]
pub owner_count: Option<u32>,
```

Render `None` as `n/a`/unknown in the analyze + health output. Mirror the same fields in `crates/cli/src/health_types/runtime_coverage.rs` if they are populated from the cloud path.

`risk_band` already has an `Unknown` default variant (`CloudRuntimeRiskBand`), so the new `"unknown"` value deserializes fine; no change needed there.

### Coordination
This is a backward-compatible CLI change (tolerates both the old numbers and the new `null`). Release it before the cloud ships the `null`-emitting response so no `--cloud` user on the current CLI hits a parse error.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `11d777118a0b23ddf36329c9415319a05398fef1`.  There
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
{"case_id": "fallow_rs_fallow__1263__11d7771",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
