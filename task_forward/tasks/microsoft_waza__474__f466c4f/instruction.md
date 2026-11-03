# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
tool_calls grader's expect[].args reads stale session_digest data, not the new tool_events[].args

## Summary

The `tool_calls` grader's new structured argument matchers (`expect: [{tool, args}]`, added in #388 / v0.38.0) fail even when the recorded tool call's arguments exactly match the declared expectation. Root cause: the grader's argument-reading path appears to use `session_digest.tool_calls[].arguments`, not the new `tool_events[].args` field also added in #388 — and `session_digest.tool_calls[].arguments` reports an unrelated placeholder shape (fields from other built-in tools like `edit`/`bash`), not the actual arguments of the call being graded.

#388's own description says the `expect` grader "checks every entry against the recorded tool calls for the run (the same data that is also serialized into `tool_events[]` in `results.json`)" — in practice this doesn't hold for the argument values.

## Reproduction

`eval.yaml` (schemaVersion 1.1, native `mcp_mocks`):

```yaml
name: repro
skill: repro-stub
schemaVersion: "1.1"
version: "1.0"
config:
  trials_per_task: 1
  executor: copilot-sdk
  model: claude-sonnet-5
  inject_skill_body: false
  disabled_skills: ["*"]
mcp_mocks:
  - name: nessie-candidate
    tools:
      entity_search_clients:
        input_schema:
          type: object
          required: [query]
        responses:
          - match:
              query: "Bissell"
            return:
              results:
                matches:
                  - name: "Bissell"
                    client_id: "c-4471"
tasks:
  - "tasks/*.yaml"
```

`tasks/entity-search-clients.yaml`:

```yaml
id: repro-001
name: Call entity_search_clients and report the client_id
inputs:
  prompt: >-
    Call the entity_search_clients tool with exactly {"query": "Bissell"} and report the
    exact client_id it returns for the match named "Bissell".
graders:
  - name: tool_was_called
    type: tool_calls
    config:
      expect:
        - tool: nessie-candidate-entity_search_clients
  - name: called_with_expected_args
    type: tool_calls
    config:
      expect:
        - tool: nessie-candidate-entity_search_clients
          args:
            query: { equals: "Bissell" }
```

Run:

```
waza run eval.yaml --model claude-sonnet-5 --no-cache -o result.json
```

## Expected

Both graders pass — the model calls `entity_search_clients` with exactly `{"query": "Bissell"}` (confirmed in the raw transcript's `tool.execution_start.arguments` and in `results.json`'s own `tool_events[].args`, both of which correctly show `{"query": "Bissell"}`).

## Actual

- `tool_was_called` (no `args:`) — **passes**.
- `called_with_expected_args` (with `args:`) — **fails**, with feedback:
  ```
  expectation tool="nessie-candidate-entity_search_clients" not satisfied: argument "query": not present on tool call
  ```

Inspecting the same `result.json`'s `session_digest.tool_calls[].arguments` for this call shows:

```json
{
  "path": "",
  "file_text": "",
  "command": "",
  "description": "",
  "skill": ""
}
```

— an unrelated placeholder shape (looks like a merged/zeroed superset of several built-in tools' argument schemas), not the actual `{"query": "Bissell"}` sent. The correctly-populated data is present a few keys over, in the same result file's `tool_events[]` array:

```json
{
  "tool_call_id": "...",
  "tool_name": "nessie-candidate-entity_search_clients",
  "args": {"query": "Bissell"},
  ...
}
```

## Environment

- waza version 0.38.4
- executor: copilot-sdk
- Confirmed via both a live run and `waza grade <eval.yaml> --results result.json` (offline re-grading against the same captured result), isolating the failure to the args-matching path specifically (tool-name-only matching passes on the identical data).

## Notes

- This may be the same underlying `session_digest.tool_calls[].arguments` placeholder-shape issue independently observed with `mcp_servers` (not just the new `mcp_mocks`) prior to v0.38 — happy to share more detail if useful, but wanted to file this against the new `expect[].args` grader specifically since that's the feature this affects most directly.
- Workaround in the meantime: read `tool_events[].args` (or the raw transcript) directly rather than relying on the `tool_calls` grader's `args:` matching.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f466c4fddf71144f42311d7c4157e8c8b3f0fed6`.  There
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
{"case_id": "microsoft_waza__474__f466c4f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
