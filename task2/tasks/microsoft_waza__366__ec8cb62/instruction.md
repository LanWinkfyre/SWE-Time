# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Agentic metrics — tool-call accuracy, tool selection, tool-input correctness

## Problem

Waza already has `tool_constraint`, `tool_calls`, and `action_sequence` graders, plus a `session_digest.tool_calls` field. The gaps are at the edges:

1. **Argument matching is shallow.** Current graders assert tool *names* and *counts* well; deep argument matching (JSON-schema, regex on specific fields, equality with tolerance) is hand-rolled per task.
2. **Cross-engine event normalization is uneven.** Different engines surface tool calls in different shapes; graders sometimes have to special-case.
3. **No aggregate "tool-use" metrics.** No equivalent of "tool selection accuracy" or "tool input correctness" across a suite — only per-task pass/fail.

## Proposal

Three focused enhancements to *existing* graders and the session digest:

### A. Richer argument matching in `tool_calls` / `tool_constraint`

```yaml
- type: tool_calls
  expect:
    - name: search_docs
      args:
        query: { regex: "^(authentication|auth)\\b" }
        limit: { equals: 10 }
```

Supported matchers: `equals`, `regex`, `json_schema`, `contains`, `range`.

### B. Normalized tool events in `results.json`

Add a stable, engine-agnostic `tool_events[]` array per task (alongside the existing `session_digest`). Each event: `{ turn, tool_name, args, result, success, duration_ms }`. Existing fields preserved for backward compatibility.

### C. Aggregate metrics in `waza compare` / dashboard

Surface per-suite metrics: tool selection accuracy (% tasks calling the expected tool first), tool input correctness (% tool calls with all required args matched), call count distribution.

## Why this matters for agentic-first

Tool use *is* the agentic behavior. Tightening argument matchers, normalizing events across engines, and exposing aggregate tool metrics gives authors the loop they need to debug *how* the agent works, not just whether the final answer was right.

## Acceptance criteria

- [ ] `tool_calls` and `tool_constraint` accept structured argument matchers (`equals`, `regex`, `json_schema`, `contains`, `range`).
- [ ] `results.json` gains a normalized `tool_events[]` array per task; existing `session_digest.tool_calls` preserved.
- [ ] `waza compare` outputs aggregate tool-use metrics (selection accuracy, input correctness).
- [ ] Cross-engine event normalization depends on #10; this issue specifies the *waza-side* shape.
- [ ] Tests cover all matcher kinds and ensure existing tasks keep working.
- [ ] Docs in `site/` showing migration patterns.

## Non-goals (filed separately)

- MCP-specific mock server — see #363.
- Tool-call assertions in adversarial packs — consumes the matchers from this issue (#365).
- Dashboard UI work beyond surfacing the metrics — follow-up.

## Related

- Existing: `internal/graders/{tool_calls,tool_constraint,action_sequence}_grader.go`, `session_digest`
- Engine event abstraction: #10
- MCP mocks: #363
- Adversarial packs: #365
- Roadmap: #66
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ec8cb6201653463f03524adcea1ced962a0d2a42`.  There
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
{"case_id": "microsoft_waza__366__ec8cb62",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
