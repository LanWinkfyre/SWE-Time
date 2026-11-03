# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Trace replay and deterministic snapshot for agent runs

## Problem

Agentic runs are non-deterministic. When an eval fails in CI, re-running rarely reproduces the failure: different model sampling, different tool ordering, different temp workspace state. Reviewers and authors waste cycles trying to recreate failures that never reappear the same way twice, and regressions in waza itself (runner/grader logic) can't be safely verified without burning LLM calls.

## Proposal

Two complementary features, with **redaction designed in from day one**.

### 1. Snapshot

Each task run can emit a `snapshot.json` capturing enough to replay it:

- Full prompt sequence (system, user, assistant).
- Every tool call: name, args, response, timing.
- Engine/model config (model id, temperature, top-p, etc.).
- Random seed *if the engine surfaces one* (best-effort metadata; not required).
- Fixture file hashes.
- Env vars — **default-deny**; only vars in a configurable allow-list are captured.
- Snapshot schema is **versioned** (`schemaVersion`); readers handle older versions or refuse with a clear error.

Snapshots are written under `--output-dir` with stable paths and referenced from `results.json`.

### 2. Replay

`waza replay <snapshot.json>` with two modes:

- **`--mode model-replay`** — stub the engine using captured events. Deterministic, no LLM call. Used to verify runner/grader changes don't break old runs.
- **`--mode live`** — re-run against the real engine with the same inputs; compare against snapshot with configurable tolerances. Used to detect model/engine drift.
- **`--bisect <baseline.json> <failing.json>`** — identify the first divergent turn between two snapshots.

### Redaction policy (designed first)

- Prompts, tool args, tool results, and outputs default to **captured as-is** unless `--redact <policy>` is set; the policy file lists regexes and JSON-paths to scrub.
- Env vars: **default-deny**, allow-list only.
- Documented redaction defaults shipped for common patterns (API keys, tokens, emails).

## Why this matters for agentic-first

Non-deterministic runs are the #1 source of "works on my machine." Snapshots turn flaky failures into reproducible bug reports. `model-replay` lets reviewers verify a fix without paying for an LLM call. `--bisect` makes "what changed?" answerable.

## Acceptance criteria

- [ ] `waza run --snapshot` writes `snapshot.json` per task under `--output-dir`; referenced from `results.json`.
- [ ] Snapshot has `schemaVersion`; reader includes a backward-compatibility test against at least one prior version.
- [ ] `waza replay` implements `model-replay` and `live` modes with documented exit codes.
- [ ] `--bisect` identifies the first divergent turn between two snapshots.
- [ ] Env capture is default-deny with an explicit allow-list.
- [ ] Redaction policy file format defined; shipped defaults for API keys/tokens/emails.
- [ ] Tests cover: round-trip fidelity, divergence detection, redaction, schema-version mismatch behavior.
- [ ] Docs in `site/` with a worked CI example.

## Related

- Engine event abstraction: #10
- Multi-turn coverage: #358 (replay should cover per-turn checkpoints once they land)
- OTel export is complementary, not required: #362
- Schema versioning policy: see new schema-version issue
- Roadmap: #66
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `48421cc86adbeee1370ceab8382c5ff519efdd4d`.  There
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
{"case_id": "microsoft_waza__367__48421cc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
