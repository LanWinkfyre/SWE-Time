# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Regression gates — baseline comparison with thresholds and statistical confidence

## Problem

`waza compare` shows diffs, but there's no opinionated **gate** for CI:

- No "fail the build if pass rate dropped >5%."
- No first-class concept of a **golden task** that must always pass regardless of aggregate score.
- No machine-readable exit codes or summary that CI annotators can parse.
- Adding or removing tasks between baseline and current breaks naive comparison.

Skill authors copy-paste shell glue to make this work.

## Proposal

Add `waza gate`, a CI-first command that consumes a baseline `results.json` and a current `results.json`:

```bash
waza gate \
  --baseline baseline.json \
  --current results.json \
  --max-regression-pct 5 \
  --golden-must-pass \
  --on-new-tasks=allow \
  --on-removed-tasks=warn \
  --format=github-actions
```

- **Regression threshold:** `--max-regression-pct N` fails when aggregate pass rate drops > N%.
- **Golden tasks:** `eval.yaml` task field `golden: true` — any failure is a hard fail, independent of aggregate.
- **Task set changes:** `--on-new-tasks` and `--on-removed-tasks` each accept `allow|warn|fail`.
- **Exit codes:** documented and stable (0 = pass, 1 = regression, 2 = golden failure, 3 = config error).
- **Output formats:** `human`, `json`, `markdown`, `github-actions` (creates inline annotations).

Statistical significance (p-values from multiple trials) is **out of scope for MVP** — add later if `trials > 1` data is consistently available.

## Why this matters for agentic-first

Agentic eval results are noisy. Without a gate that knows about golden tasks and task-set deltas, CI is either too strict (blocks on noise) or useless (always green). This issue makes "ship safely" a one-liner.

## Acceptance criteria

- [ ] `waza gate` command implemented.
- [ ] `golden: true` task field absorbed from former #359; any golden failure exits 2 regardless of aggregate.
- [ ] Configurable behavior for added/removed tasks.
- [ ] Stable, documented exit codes.
- [ ] `github-actions` output emits inline annotations and a job summary.
- [ ] Docs in `site/` with a CI snippet (GitHub Actions + Azure DevOps).
- [ ] Tests cover: regression threshold, golden hard-fail, task-set delta behaviors, exit codes.

## Non-goals

- Statistical significance / confidence intervals — defer until multi-trial data is standard.
- Dataset versioning — see #17.

## Related

- Roadmap: #66
- Golden-task absorption from former #359 (closed).
- Existing: `waza compare`.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5af9038ba478c9bca700a4f71a847db85a85a7b9`.  There
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
{"case_id": "microsoft_waza__364__5af9038",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
