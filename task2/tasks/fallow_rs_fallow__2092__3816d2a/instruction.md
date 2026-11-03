# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
typeAware + audit --gate new-only forces dual configs (poor enablement DX)

## Problem

Enabling persistent type-aware analysis:

```jsonc
{
  "typeAware": {
    "enabled": true,
    "require": "best-effort"
  }
}
```

…is great for `fallow dead-code` / `fix` / `health`, but it immediately breaks the recommended PR gate:

```bash
fallow audit --gate new-only --production --base origin/main
```

Error (exit 2):

```text
type-aware audit cannot compare base and head because their semantic analysis identities differ
```

That puts adopters in a bad place:

1. Docs and CI examples push `audit --gate new-only` as the day-one PR gate (legacy backlog stays non-blocking).
2. Type-aware docs push `typeAware.enabled` as the persistent opt-in.
3. Those two “happy paths” cannot share one config today.
4. There is no `--no-type-aware` (or equivalent) to keep audit syntactic while leaving type-aware on for cleanup commands.

So the practical DX becomes: “enable the good feature, then invent a second stripped config for CI.” That feels like fighting the product.

### Real adopter workaround

In [caniplay.today](https://github.com/mykiary/caniplay.today) we ended up with:

- `.fallowrc.json` → `typeAware.enabled: true` for local cleanup
- generated `.fallowrc.audit.json` → same config minus `typeAware` for `vp run fallow` + GitHub Action `command: audit` / `gate: new-only`

That works, but it is plumbing users should not need to discover.

### Secondary macOS footgun

On macOS, default temp dirs under `/var/folders/...` (symlink to `/private/var/...`) can fail earlier with:

```text
Type-aware analysis failed: type-aware path /var/folders/.../apps/engine/src/project.ts is outside project root /private/var/folders/...
```

Setting `TMPDIR` to a non-symlinked path surfaces the semantic-identity error instead. Linux CI may skip the path issue and still hit the identity mismatch.

## Environment

- fallow `3.10.0` (`fallow-type-aware@3.10.0`, protocol 6, typescript-go 7.0.2)
- pnpm monorepo (apps + packages), multiple `tsconfig.json`s
- macOS Darwin arm64 for local repro; CI on linux/arm64 with `fallow-rs/fallow` Action
- Companion discovery OK: `fallow type-aware status` → `available: true`

## Steps to Reproduce

1. Add `typeAware.enabled: true` to `.fallowrc.json` (or pass `--type-aware`).
2. Run against a non-empty changeset:

```bash
fallow audit --gate new-only --production --base HEAD~3 --format json --quiet
```

3. Observe exit 2 with the semantic-identity (or macOS path) error.
4. Note that the same tree works with:

```bash
fallow audit --gate all --production --type-aware --base HEAD~3
fallow dead-code --type-aware --production
```

## Expected Behavior

One of:

1. **Best:** `typeAware.enabled` works with `audit --gate new-only` — compare introduced findings under a compatible semantic identity, or degrade gracefully (syntactic attribution + advisory type-aware on head) instead of hard-failing the gate.
2. **Good:** If dual-mode is required, make it first-class:
   - `audit.typeAware: false` / `--no-type-aware`, or
   - documented `gate: new-only` + type-aware matrix in the Action/docs so adopters do not invent stripped configs.
3. **Also:** canonicalize temp/worktree paths on macOS so `/var` vs `/private/var` cannot abort type-aware audit.

## Actual Behavior

Enabling the advertised persistent type-aware config makes the advertised PR audit gate unusable until the user strips type-aware back out for CI.

## Why this matters

Type-aware is clearly valuable for cleanup confidence. The pain is enablement: the feature that improves trust in deletions cannot ride along with the feature that makes Fallow adoptable on existing repos. From an adopter’s seat, that split undercuts the “turn it on in config” story.

Happy to provide more repro logs from the caniplay.today monorepo if useful.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3816d2a8e4a4aefd8c8af70aa786abfc4f9af921`.  There
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
{"case_id": "fallow_rs_fallow__2092__3816d2a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
