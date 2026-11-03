# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: MCP tool-use evaluation primitives

## Problem

Skills increasingly call MCP tools. Today, evaluating an MCP-using skill in CI requires:

- A real MCP server (network, auth, side effects, flaky).
- Or hand-rolled stubs per skill (no shared shape).

There's no waza-native way to stand up a **deterministic MCP mock** for an eval run. Tool-call assertions and record/replay of MCP traffic are handled by sibling issues (see "Non-goals" below).

## Proposal

Ship a built-in MCP mock server that waza launches alongside the eval:

```yaml
mcp_mocks:
  - name: github
    fixtures: ./fixtures/github-mcp/
    tools:
      list_issues:
        responses:
          - match: { owner: "octocat" }
            return: { issues: [...] }
```

- Mock server speaks MCP over stdio/HTTP (matches existing `config.mcp_servers` shape).
- Fixtures are JSON files in a directory; matching is exact-args by default, with optional JSON-schema match.
- Mock runs in-process during the eval; no network, no port collisions in CI.
- Unknown tool calls fail loudly (not silently return null) so missing fixtures are visible.
- Recorded fixtures redact secrets via the same policy used by snapshots (#367).

## Why this matters for agentic-first

MCP is the primary tool surface for agents. Without deterministic MCP mocking, every MCP-using skill is untestable in CI — or worse, "tested" against a live service that mutates state. This is the single biggest blocker to CI-first agentic skill development.

## Acceptance criteria

- [ ] `mcp_mocks:` field in eval schema; backward compatible.
- [ ] Mock server runs in-process and registers as an MCP server the skill can call.
- [ ] Fixture matching: exact-args (default), JSON-schema, regex on individual fields.
- [ ] Unknown/unmatched calls fail the task with a clear error pointing at the missing fixture.
- [ ] No live network required in CI; tests in `internal/` verify this.
- [ ] Docs in `site/` with a worked MCP eval example.

## Non-goals (filed separately)

- MCP-specific grader assertions (tool name/args/sequence) — handled by enhanced tool graders in #366.
- Record-and-replay of real MCP traffic — handled by snapshot/replay in #367.
- Adversarial MCP test packs (poisoned responses, scope-bypass) — see #365.

## Related

- Existing: `config.mcp_servers`
- Tool graders: #366
- Snapshot/replay: #367
- Safety packs: #365
- Roadmap: #66
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3458ced5ce3d83fd88925097de5b93516644e1a9`.  There
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
{"case_id": "microsoft_waza__363__3458ced",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
