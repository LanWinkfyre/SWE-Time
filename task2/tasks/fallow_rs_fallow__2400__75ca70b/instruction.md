# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Support SvelteKit v3

### Problem

[Release candidate is out](https://svelte.dev/blog/sveltekit-3-release-candidate) and there are a lot of breaking changes, new modules etc.

Migrations docs are here, covering most of the major changes: https://next.svelte.dev/docs/kit/migrating-to-sveltekit-3

### Proposed solution

Probably wait with implementation until its official release, but wanted to give a heads up, so one can read up on the docs.

### Alternatives considered

I tried adding support fully with Claude (as I am not well versed with Rust), testing against `version-3` branch of SvelteKit. Can make a PR if interesting.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `75ca70b881b768d3bb81573c23e0264443a5a422`.  There
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
{"case_id": "fallow_rs_fallow__2400__75ca70b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
