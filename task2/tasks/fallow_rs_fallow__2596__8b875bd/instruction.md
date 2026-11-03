# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
mcp: add a cloud-backed runtime coverage tool

The MCP server exposes five runtime-coverage tools (`check_runtime_coverage`, `get_cleanup_candidates`, `get_hot_paths`, `get_importance`, `get_blast_radius`) and every one of them requires a local V8 directory or Istanbul file in the `coverage` field. Nothing in `crates/mcp` reads fallow cloud. An agent that wants the production signal has to shell out to `fallow coverage analyze --cloud`; through MCP the cloud runtime-context, review packet and cross-deployment history are unreachable.

### What to do

1. Add a `coverage_source` style option (or a sibling tool such as `get_cloud_runtime_context`) that reuses the CLI's cloud path: `crates/cli/src/coverage/cloud_client.rs` fetches `/v1/coverage/{repo}/runtime-context` with `FALLOW_API_KEY`, and `analyze.rs` already turns that payload into `runtime_coverage`. Inputs: `repo`, optional `project_id`, `period_days`, `environment`, `commit_sha`, plus the existing `production`, `top`, `min_invocations_hot`.
2. Return the same `runtime_coverage` block the CLI prints in `--format json`, so agents get one shape for local and cloud data.
3. Refuse cleanly when `FALLOW_API_KEY` is absent, with the same hint text the CLI uses.
4. Document the tool in the MCP tool guides and cover it with a test that stubs the HTTP call.

### Acceptance

- `tools/list` shows the cloud-capable tool with its input schema.
- A `tools/call` with a valid key returns `runtime_coverage.findings` and `hot_paths` for a repo that has cloud data, and a typed error without a key.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8b875bdf06105317ab1b94c4493cf639c9e4839b`.  There
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
{"case_id": "fallow_rs_fallow__2596__8b875bd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
