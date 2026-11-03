# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Fallow is extremely slow with Yarn PnP

### Problem

Fallow is extremely slow when Yarn PnP is turned on in Yarn Berry/Yarn 4.

For some context, read: https://yarnpkg.com/features/pnp

The source of the problem is the fact that Yarn PnP does away with `node_modules` in favour of a immutable `.yarn/cache/*.zip` folder which fallow doesn't know anything about currently.

```
┌─ Pipeline Performance ─────────────────────────────
│  discover files:      148.0ms  (17649 files)
│  workspaces:           75.1ms  (840 workspaces)
│  plugins:             503.6ms
│  script analysis:      12.3ms
│  parse/extract:       657.8ms  (17649 modules)  (parallel: ~5065ms CPU)
│  cache update:        666.6ms
│  entry points:        469.3ms  (10632 entries)
│  resolve imports:  494868.0ms
│  build graph:         504.4ms
│  analyze:           16577.7ms
│  (other):               0.0ms
│  ────────────────────────────────────────────────
│  TOTAL:            513061.9ms
└───────────────────────────────────────────────────
```

When setting `nodeLinker: node-modules` in .[yarnrc.yml](https://yarnpkg.com/configuration/yarnrc#nodeLinker) (i.e. disable Yarn PnP):

```
┌─ Pipeline Performance ─────────────────────────────
│  discover files:      146.7ms  (17698 files)
│  workspaces:           74.9ms  (840 workspaces)
│  plugins:             715.3ms
│  script analysis:     527.2ms
│  parse/extract:       601.3ms  (17698 modules, 17071 cached, 627 parsed)
│  cache update:        258.8ms
│  entry points:        466.4ms  (10672 entries)
│  resolve imports:   26947.5ms
│  build graph:         450.8ms
│  analyze:           15617.1ms
│  (other):               0.0ms
│  ────────────────────────────────────────────────
│  TOTAL:             44938.0ms
└───────────────────────────────────────────────────
```

### Proposed solution

From personal experience, Yarn PnP _does_ work with fallow it's just really slow.

My proposal is we just turn on the `yarn_pnp` feature in `oxc_resolver` crate: https://github.com/oxc-project/oxc-resolver/blob/b6a6125c5556ca1ae0e48b479d203e8f06effd10/Cargo.toml#L148

I've given this a go a #2435  and it more or less brings Yarn PnP to an identical speed as node_modules.

### Alternatives considered

Personally I don't think there's any other real option unless you just choose not to use Yarn PnP
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `94d5f7ad28fd921c6709bf4939c2d5fe0b76a273`.  There
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
{"case_id": "fallow_rs_fallow__2444__94d5f7a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
