# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
dead-code baselines rot silently: no partial-staleness warning, unlike health baselines

## Summary

`fallow health --baseline` warns when a saved baseline goes partially stale (#2065, released in v3.12.0). `fallow dead-code --baseline` has no equivalent: a dead-code baseline can rot indefinitely and every run still reports green, with nothing on stderr.

The data is already computed — the JSON envelope exposes `baseline.entries` and `baseline.matched` — so only the human-output surface (and, ideally, an opt-in gate) is missing.

## Reproduction

Verified on 3.22.0 and 3.25.0.

```console
$ # inject two entries that match no current finding
$ fallow dead-code --baseline=stale-baseline.json
Comparing against baseline: stale-baseline.json
✓ No issues found (0.18s)

$ fallow dead-code --baseline=stale-baseline.json --format json | jq .baseline
{ "entries": 29, "matched": 27 }
```

Two entries match nothing, and the human output says nothing. The equivalent health run does:

```console
$ fallow health --baseline=stale-health-baseline.json
Comparing against health baseline: stale-health-baseline.json
Warning: health baseline is partially stale: 60 of 67 entries matched no current finding,
so the gate protects less than what was saved. Re-save with: --save-baseline ...
```

## Why it matters

A dead-code baseline is regenerated wholesale by `--save-baseline`. When it has silently rotted, the refresh diff mixes two unrelated things: removals of entries for findings fixed long ago, and additions for issues introduced in the meantime. The reviewer sees one churny diff and cannot tell which lines are cleanup and which are newly suppressed problems.

This is the same failure mode `stale-suppressions` already protects against for inline `fallow-ignore` comments. The rule exists precisely because a suppression left behind after its issue was fixed is dead weight that hides the next one. A baseline is the file-level version of the same thing, and it currently has no such protection.

In our monorepo the baseline had accumulated three stale entries — two `*.test-d.ts` files that a later `dynamicallyLoaded` config change had covered, and an import cycle that had since been broken. Nothing surfaced them; we found them only by diffing a regeneration by hand.

## Proposal

1. **Parity with health**: emit the same partial-staleness warning for `dead-code` baselines, human output only, exit codes unchanged.
2. **Optionally, a way to gate on it.** The warning alone is advisory, and in CI advisory output is scrolled past. Either a `--fail-on-stale-baseline` flag or a `stale-baseline` rule (defaulting to `off`, or to `warn` for parity with `stale-suppressions`) would let a repo decide that a rotten baseline fails the build. We currently do this with a wrapper script around the JSON output, which works but feels like something the tool should own.

Happy to send a PR for (1) if the shape is agreed.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a013bc4285df07f9e706b1357de421222e9ebb4e`.  There
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
{"case_id": "fallow_rs_fallow__2627__a013bc4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
