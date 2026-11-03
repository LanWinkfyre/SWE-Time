# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
cli and mcp tests mutate process-global env, which is unsound under the parallel harness

`crates/cli` tests call `std::env::set_var` and `std::env::remove_var` from inside `#[test]` functions. Confirmed sites include `crates/cli/src/ci.rs` (around 2542, 3441, 3498) and `crates/cli/src/api.rs` (around 619, 629, 838, 849). `crates/mcp/src/server/tests/run.rs` does the same.

Both mutate process-global state while the test harness runs tests as parallel threads in one process. Rust 2024 marks these functions unsafe for exactly this reason: another thread reading the environment concurrently is a data race, and a test that sets a variable can change the behaviour of an unrelated test that happens to read it.

This is filed as a soundness issue on its own merits, not as a flake fix. It was found while investigating #2460, and it is explicitly **not** an explanation for anything in that issue: all three causes there were identified and fixed elsewhere (#2483, #2490, d5a422c62). No failure has been attributed to these call sites. Filing it so the finding is not lost, with no claim it is currently breaking anything.

The fix worth having is to remove the dependency on shared globals rather than to serialize the tests. Injecting the value, or reading it through a seam a test can set locally, removes the unsoundness; serializing only hides it and leaves the next parallel-test change free to reintroduce the race. A guard test that fails when a new `env::set_var` appears in these crates would keep it from coming back.

Not urgent. Worth doing before the 2024 edition migration makes these call sites hard errors rather than a latent hazard.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `79085fb4e009ff6768ee02eeb1139857231998b8`.  There
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
{"case_id": "fallow_rs_fallow__2494__79085fb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
