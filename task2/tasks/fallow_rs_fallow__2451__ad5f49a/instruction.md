# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
config: an unknown key fails the run with exit 2, so a new field cannot be adopted before the whole fleet upgrades

## What happens

`FallowConfig` carries `#[serde(deny_unknown_fields)]` (`crates/config/src/config/mod.rs:253`), so any key fallow does not recognize fails config load with exit 2 rather than being ignored.

Measured on 3.20.0 with a `.fallowrc.json` containing one unknown key:

```
Error: unknown field `traverseHiddenDirs`, expected one of `$schema`, `extends`, `entry`, ...
```

Exit code 2 on the human surface, and on `--format json` the run emits `{"error":true,"message":"unknown field ..."}` and exits 2 as well.

## Why it matters

This makes every new config field a coordinated fleet upgrade rather than an additive change. A team that commits a field introduced in version N to a shared `.fallowrc.json` breaks every runner still on N-1: local machines, CI jobs, and pre-commit hooks. The break lands on the commit that adds the field, not on the upgrade that would explain it, and the error names the field rather than the version skew, so the reader's first guess is a typo.

The strictness is worth keeping for what it is good at. A misspelled `ignorePaterns` should not silently do nothing, and today it does not.

## The tension

Those two goals conflict under one rule. Catching a typo and tolerating a forward-declared field are the same shape to serde: a key the current binary does not know.

Some directions worth weighing:

- Warn instead of failing for keys that match a known field within a small edit distance, and fail for the rest. Inverts today's behavior on exactly the typo case it is meant to catch, so probably wrong on its own.
- A `$schema` or explicit `minimumVersion` in the config that lets fallow say "this config asks for a newer fallow" instead of "unknown field".
- A reserved namespace whose keys are ignored by older versions by construction.
- Keep failing, and treat the fleet upgrade as the intended cost. Defensible, but it should then be a documented, deliberate contract rather than a side effect of a derive attribute.

No recommendation here. The point of the issue is that the decision has not been made explicitly, and it gates any new config field.

## Prerequisite for

The deferred hidden-directory traversal field in #461. That field is exactly the shape that hurts: something a team commits once, to a config shared by everyone.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ad5f49ac14abd4326570d75f4156e5e9577294c2`.  There
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
{"case_id": "fallow_rs_fallow__2451__ad5f49a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
