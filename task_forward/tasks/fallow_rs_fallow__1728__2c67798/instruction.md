# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Add raw styling value gate for design-token consistency

## Summary
Track a v3 styling follow-up: detect newly introduced raw styling values outside token and design-system conventions across CSS and CSS-in-JS.

## Scope
- Detect new raw colors, font sizes, spacing, radius, and shadow literals when source locations are reliable.
- Cover CSS, Sass/Less, CSS Modules, and CSS-in-JS object or tagged-template forms where parser confidence is high.
- Feed fallow audit introduced-vs-base gating, defaulting to advisory unless the project escalates the rule.
- Reuse the existing styling findings surface and avoid auto-fix.

## Acceptance criteria
- Existing aggregate value-sprawl metrics gain located first-use evidence for raw values.
- `audit --format json` can explain whether a raw-value finding is introduced or inherited.
- Public corpus smoke covers at least one positive example and one quiet design-system-heavy example.
- Sass/Less behavior stays conservative when mixins, loops, or imports prevent reliable source-location attribution.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2c67798f2629db09e82117ce345130c1c822bf6d`.  There
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
{"case_id": "fallow_rs_fallow__1728__2c67798",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
