# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Error 2 for Type-aware in VSCode on Windows again in 3.21

### What happened?

A bug that was fixed earlier, re-appeared. Not sure if the cause is the same. When type-aware is enabled, scanning takes a long time on the repo on VSCode in Windows 11. Eventually it errors out with error code 2. The only thing it does manage to show rather quickly are the Health scorings/results, the other parts never show.

### Reproduction

1. On this opensource repo https://github.com/openfrontio/OpenFrontIO, on Windows 11 in VSCode with Fallow extenstion version 3.21
2. Switch between type-aware enabled and disabled and re-scan
3. Notice without type-aware works. But with type-aware on, the Health scorings are shown relatively quickly in Fallow's sidebar, the other two keep Fallow running for quite a while before it stops on error 2.

### Expected behavior

Type-aware to not result in error 2.

### Fallow version

3.21

### Operating system

Windows

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `45bddc6859377636bc1e0ea0374cd318bd7f9e70`.  There
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
{"case_id": "fallow_rs_fallow__2499__45bddc6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
