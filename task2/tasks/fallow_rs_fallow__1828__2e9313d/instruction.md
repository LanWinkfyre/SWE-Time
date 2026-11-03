# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Human footer suggests suppress tokens that IssueKind::parse does not recognize for eight sections

Follow-up from the review of #1820, which fixed the singular/plural mismatch for the Unused files section. The same surface has a wider gap: `section_suppress_rule` in `crates/cli/src/report/human/mod.rs` emits suppression hint tokens that `fallow_types::suppress::parse_suppression_target` does not recognize, so following the printed hint produces a comment that suppresses nothing and then surfaces a stale-suppression finding.

Verified unparseable footer tokens (present only as `config_key`/`mcp_issue_type`, no alias): `unused-exports`, `unused-types`, `unused-dependencies`, `unused-enum-members`, `unused-class-members`, `unresolved-imports`, `unlisted-dependencies`, `duplicate-exports`.

Not broken (registered aliases): `circular-dependencies`, `unused-store-members`, `unprovided-injects`, `unrendered-components`, `unused-component-props`, `unused-component-emits`.

Two-part fix:
1. Correct the emitted tokens (or add plural aliases where that is the better contract; the dependency sections may want no hint at all, since those findings live in `package.json` where inline comments are impossible).
2. Add a parse-roundtrip guard test asserting every token `section_suppress_rule` can emit parses via `parse_suppression_target`, so this whole surface stays locked down.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2e9313ddd139a994e38c004b67e31d4dd21415ab`.  There
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
{"case_id": "fallow_rs_fallow__1828__2e9313d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
