# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
CI run: plain multi-line scalars lose continuation lines

`crates/core/src/scripts/ci.rs` lifts `run:` values out of workflow files. Two of the three original shapes are fixed; one remains.

Folded block scalars are fixed: `is_multiline_run_marker` accepts `|` and `>` with any combination of chomping and explicit indentation indicator.

Package-manager indirection is fixed in #2063: `npm run <script> -- --flag` and `yarn <script> --flag` now resolve through the script catalogue and are rescanned, bounded by a depth limit and a global expansion budget. Ambiguity is sticky, so a script name declared with different bodies across packages is never followed regardless of workspace order; names and bodies filter separately under `--production`; and entry files from workspace bodies no longer seed root-relative patterns. This unblocks #2019.

**What remains: plain multi-line scalars.** `run: npx eslint .` followed by indented continuation lines drops every continuation, which is the shape of GitHub's own `code-scanning/eslint.yml` starter workflow. This one needs care: `MultilineRunState::start` measures indent from the start of the whole line, so a naive fold would swallow sibling step keys (`env:`, `with:`) and let their path-looking values flow into `entry_files`, which can hide genuinely unused files. It needs key-column anchoring and continuations appended to the already-pushed command rather than pushed as separate commands.

A smaller test gap belongs with that work: there is still no end-to-end `analyze_content` test for a folded block, only the predicate test `folded_run_scalar_is_a_block_marker`.

Backslash line continuations inside `run: |` are a separate, already-documented limitation and are deliberately out of scope here.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9a40a7f9d74bb52fe16d5b5fa727cc2cedc6ffeb`.  There
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
{"case_id": "fallow_rs_fallow__2016__9a40a7f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
