# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Document that Action ref and CLI version are independent

## Summary

Make it obvious in the CI / GitHub Action docs that the Action ref (`uses: fallow-rs/fallow@…`) and the fallow **CLI** version are independent, and that the recommended way to keep local/CI scanner versions aligned is `version:` or the project `package.json` pin — not lockstepping the Action tag with the npm package.

## Motivation

Many scanner Actions (and common security-hardening habits) encourage pinning the Action SHA/tag to the same version as the npm CLI. That pattern leads users to assume that upgrading fallow (especially across majors like v2 → v3) requires bumping **both** the npm package and the Action ref in lockstep for every release.

fallow already supports decoupling:

1. Explicit `version` input on the Action
2. Auto-resolution from the project's `package.json` `fallow` dependency when `version` is omitted
3. Fallback to `latest`

This was already the root of the confusion in #944 (Action ref mistaken for CLI version). The behavior exists; discoverability is the gap. The README CI snippet shows `uses: fallow-rs/fallow@v3` and mentions floating `@v3` / pinning exact tags for reproducibility, but it does not spell out the `version` input or the `package.json` auto-pin path next to that example.

## Proposed Solution

In the [CI guide](https://docs.fallow.tools/integrations/ci) and the README GitHub Actions section:

- State explicitly that **Action ref ≠ CLI version**
- Document the resolution order: `version` input → `package.json` `fallow` dep → `latest`
- Show a recommended example that pins the Action major (or a SHA for supply-chain pinning) while letting the CLI come from the project pin:

```yaml
- uses: fallow-rs/fallow@v3 # Action wrapper major (or pin a SHA)
  with:
    # optional — omit to use the fallow version from package.json
    version: 3.9.1
    command: audit
```

- Note that **major** Action bumps (`@v2` → `@v3`) may still be required when the Action wrapper's inputs/behavior change, but patch/minor CLI upgrades should not require changing the Action ref when using `version` / `package.json` resolution.

## Acceptance Criteria

- [ ] CI docs describe Action ref vs CLI version and the resolution order
- [ ] README CI example (or adjacent prose) mentions `version` and/or `package.json` auto-detection
- [ ] Cross-link from the `version` input description in `action.yml` to the CI docs section (optional but helpful)

## Alternatives Considered

- Relying only on #944's explanation — easy to miss; users landing on the README/CI guide never see it
- Changing Action tagging so tags always embed the CLI — works against the existing intentional split and supply-chain pinning of Action code

## Additional Context

Came up while reviewing a workflow that SHA-pinned `fallow-rs/fallow@… # v2.88.3` to match npm `fallow@2.88.3`, under the assumption both must move together. The Action already installs the project-pinned CLI when `version` is omitted; the docs just don't make that the default mental model.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `52b30f51ec5639ccbefec3bb9a130f5a8afd436a`.  There
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
{"case_id": "fallow_rs_fallow__2079__52b30f5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
