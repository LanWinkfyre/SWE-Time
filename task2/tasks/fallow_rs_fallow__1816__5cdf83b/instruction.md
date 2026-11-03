# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Migrate the GitHub Action to the native github-annotations and github-summary formats

The CLI now ships native GitHub-format output: `--format github-annotations`, `--format github-summary`, and `fallow report --from` for analyze-once rendering (landed on main after v3.3.0, including the workflow-command escaping core and golden snapshots). The composite action still renders annotations and step summaries through its jq layer (`action/jq/` plus the scripts in `action/scripts/`).

Migrating the action to the native formats gives one source of truth for the escaping contract, severity ordering, the annotation budget notice, and repo-root path rebasing, and removes a stack of bash/jq that has to track CLI output changes by hand.

Blocked on: the first release that includes these formats. The action installs released binaries, so migrating before then would invoke flags the installed CLI rejects.

Scope sketch:
- Replace the annotation and summary generation in the action with the native formats.
- Raise the action's default/minimum fallow version to the first release carrying the formats, and decide the compatibility story for users who pin an older CLI version: hard minimum with a clear error, or keep the jq path as a fallback during a deprecation window.
- Remove the superseded jq scripts and their tests in `action/tests/` once output parity is confirmed against the golden snapshots.
- PR review-comment assembly stays as is unless the native formats already cover it.

Out of scope: the GitLab CI template (`ci/`), which has its own formatting layer and deserves a separate decision.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5cdf83b10de669b72f559142ecdd36f54c7bc4a5`.  There
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
{"case_id": "fallow_rs_fallow__1816__5cdf83b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
