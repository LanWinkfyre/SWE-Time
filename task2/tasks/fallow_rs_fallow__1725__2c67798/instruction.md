# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Add a repeatable styling corpus smoke harness

## Problem

The recent public-project smoke found a real false-positive family in Tailwind arbitrary-value detection. That was valuable enough that we should make this kind of corpus validation repeatable instead of ad hoc.

## Proposed direction

Add a styling corpus smoke harness:

- Maintain a small curated public corpus covering Tailwind, StyleX, vanilla-extract, PandaCSS, styled-components, Emotion, CSS Modules, Sass, Less, Vue, Svelte, Astro, and template-heavy repos.
- Run `health --css`, `health --css --production`, and `audit --css-deep` on representative changed anchors.
- Summarize findings by repo, issue code, sub-kind, confidence, and sample paths.
- Compare against a checked-in allowlist or snapshot of expected high-signal samples.
- Make it easy to run locally without cloning huge repos every time.

## Acceptance criteria

- One command runs the corpus smoke and writes bounded JSON plus a markdown summary.
- The harness highlights new issue-code spikes and new high-confidence sub-kind spikes.
- Corpus data is cached outside the repo or downloaded on demand.
- At least one project per styling stack is represented.
- The harness is documented for release and review use.

## Non-goals

- Running the corpus in every normal CI job.
- Treating all corpus findings as regressions. Some are real project changes.
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
{"case_id": "fallow_rs_fallow__1725__2c67798",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
