# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
test(mcp): Windows process-tree lifecycle tests are flaky (timeouts) on CI runners

The Windows subprocess/job-tree lifecycle tests in crates/mcp (code_mode_subprocess::windows_tests::completed_success_cleans_descendant_process_tree, server::tests::run::run_fallow_completed_success_cleans_descendant_process_tree_windows_job, run_fallow_timeout_terminates_and_reaps_windows_job_tree) intermittently time out on GitHub Windows runners. Observed on three unrelated runs in one week: the v3.11.0 Deno PR (#2080, twice, different jobs), a lightningcss dependabot PR, and the v3.13.0 release-validation run, each passing on plain rerun with no code change in crates/mcp.

Likely cause: fixed timeouts racing slow runner process spawning under load. Proposal: raise or make adaptive the subprocess-completion timeouts in these tests, or serialize them (they may contend on process-tree enumeration), and add a retry-once annotation only if the timeout fix is insufficient. A flaky release gate costs a full ~20 minute validation rerun per hit.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d00354b85399a5908d45f38bb890877c78e5375b`.  There
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
{"case_id": "fallow_rs_fallow__2112__d00354b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
