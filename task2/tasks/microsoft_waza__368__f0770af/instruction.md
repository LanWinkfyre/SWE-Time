# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Schema versioning policy and migration tooling for public artifacts

## Problem

Multiple in-flight gap features mutate the public shapes of `eval.yaml`, `results.json`, transcripts, dashboard APIs, and (newly) `snapshot.json`. Without an explicit schema-version policy, every feature ships with a hidden risk of breaking older evals, baselines, and CI configs.

Examples already on the table:
- `checkpoints:` field on tasks (#358)
- `mcp_mocks:` field on tasks (#363)
- `golden: true` task field + new `waza gate` output shape (#364)
- `tool_events[]` normalized in `results.json` (#366)
- `snapshot.json` with full event capture (#367)
- `adversarial:` field (#365)

If we don't pin this down now, the second time someone tries to compare a baseline `results.json` to a current one across a waza version bump, it'll silently misbehave.

## Proposal

Adopt a single, documented schema-version policy for all public artifacts.

### Versioned artifacts

| Artifact | Field | Owner |
|---|---|---|
| `eval.yaml` | `schemaVersion` (top-level) | `internal/models/spec.go` |
| `results.json` | `schemaVersion` | `internal/models/outcome.go` |
| `snapshot.json` | `schemaVersion` | new (#367) |
| Dashboard/SSE event envelope | `schemaVersion` | `web/`, #178 |

### Versioning rules

- **Semver-shaped**: `MAJOR.MINOR` (no patch — schemas don't have hotfixes).
- **MINOR bumps** are backward-compatible additions (new optional fields). Readers ignore unknown fields.
- **MAJOR bumps** are breaking. Readers must refuse with a clear error and a pointer to a migration command.
- Default-on **unknown-field warnings** (not errors) for MINOR drift.
- `waza migrate <file>` command for explicit migrations across MAJOR boundaries.

### Compatibility tests

- `internal/validation/` ships golden fixtures for each prior schema version.
- CI test: every reader must parse every prior MINOR within the same MAJOR.

## Why this matters

Eval suites are long-lived. Authors check in `eval.yaml` and baseline `results.json` and expect them to keep working. Without versioning, a routine waza upgrade silently changes meaning — the worst kind of break.

## Acceptance criteria

- [ ] `schemaVersion` field added to `eval.yaml`, `results.json`, and any new artifact (`snapshot.json`, gate output, SSE envelope).
- [ ] Reader logic emits warnings on unknown fields within a MAJOR, errors across MAJOR.
- [ ] `waza migrate` command stubbed (no-op for v1 → v1; real migration when first MAJOR bump happens).
- [ ] Golden fixtures for each prior MINOR live in `internal/validation/testdata/`.
- [ ] Compatibility tests in CI assert every reader handles every prior MINOR.
- [ ] Policy documented in `site/` with a "schema changes" changelog page.

## Related

- Roadmap: #66
- All in-flight schema-touching features: #358, #363, #364, #365, #366, #367, #178
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f0770af7ba0a82e6e30c1fb360f75d3cc0d11bec`.  There
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
{"case_id": "microsoft_waza__368__f0770af",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
