# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Plugin config files used for activation but never parsed (semantic-release, Nx)

An audit of plugin config coverage found the same class of gap that hid Vitest's `vite.config` handling: a plugin knows a config filename for *activation* but that filename is absent from `config_patterns()`, so the file is never parsed and everything it declares is invisible.

Two concrete instances remain, both demonstrated on fixtures:

**semantic-release** (`crates/core/src/plugins/semantic_release.rs`): `CONFIG_PATTERNS` covers only `release.config.{js,cjs,mjs}` and `.releaserc.{js,cjs}`, while `ALWAYS_USED` already names `.releaserc.{json,yaml,yml}`. The JSON form is the most common shape, so third-party plugins declared there are reported as unused. `extract_from_source` already paren-wraps `.json`, the same path `.babelrc.json` uses, so only the pattern needs adding. Deliberately not `.yaml`/`.yml` (the parser is JS/JSON only) or bare `.releaserc` (ambiguous). The hardcoded list in `crates/engine/src/discover_walk.rs` needs the same entry.

**Nx** (`crates/core/src/plugins/nx.rs`): `config_patterns` is `["**/project.json"]` while `always_used` is `["nx.json", "**/project.json"]`, so `nx.json` is protected from unused-file reporting but never parsed. Its `plugins`, `targetDefaults` executors and `tasksRunnerOptions.*.runner` name packages that go uncredited.

### Structural guard

Worth adding alongside: a registry-wide invariant asserting every activation-list entry carrying a JS/TS source extension is matched by at least one `config_patterns` glob, with a small named allowlist for deliberate exclusions. That assertion would have caught the original `vite.config` bug and both instances above, instead of each being found by hand.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1faf718e4589333a9d1a82e8f3810c17cdf5e0f3`.  There
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
{"case_id": "fallow_rs_fallow__2015__1faf718",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
