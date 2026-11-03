# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
docs(unrendered-component): module contract claims a never-false-flag guarantee that ambiguity handling no longer meets

The module header of `crates/core/src/analyze/unrendered_component.rs` states the detector is:

> Built to never false-flag (degrade by abstaining)

and explains the mechanism as:

> The "rendered/used" set is built LIBERALLY (any reference, auto-import, dynamic import, side-effect import, through barrel chains): over-crediting a component can only suppress a finding, never create one.

That reasoning holds only while every uncertain case resolves toward more credit. Since the effective-binding model landed, a name supplied by two colliding `export *` sources resolves to `Ambiguous`, and the crediting paths skip it (see #2263). Ambiguity therefore *under*-credits, and under-crediting is exactly the direction that can create a finding rather than suppress one. A component reachable only through an ambiguous barrel name can now be reported as unrendered.

The code may well be fine to leave as is pending #2263; the problem is that the header tells the next reader the failure mode is impossible, which will cost someone a debugging session when they hit it.

**Ask:** either soften the guarantee to describe the actual invariant (liberal crediting for resolvable names, abstain-on-ambiguity as a known exception), or state the ambiguity carve-out explicitly and link the tracking issue.

Found while reviewing #2210.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8b32aa4f6a285d1ae6897986f99dde834ecb7579`.  There
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
{"case_id": "fallow_rs_fallow__2264__8b32aa4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
