# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
bug: ApprovalFilter for MCP tools is non-functional — `never` list is ignored, all tools require approval

> *This bug was identified by Claude during a systematic audit of the Responses API code paths.*

### System Info

- Llama Stack version: latest dev:main
- File: `src/llama_stack/providers/inline/agents/builtin/responses/streaming.py`, lines 1552–1565

### 🐛 Describe the bug

`StreamingResponseOrchestrator._approval_required()` has an `isinstance` check on the wrong object, making the entire `ApprovalFilter` feature non-functional. Tools explicitly listed in `require_approval: { never: ["safe_tool"] }` still require approval.

The method checks `isinstance(mcp_server, ApprovalFilter)`, but `mcp_server` is an `OpenAIResponseInputToolMCP` — never an `ApprovalFilter`. The check is always `False`, so the filter's `always`/`never` lists are dead code. The method falls through to `return True`, requiring approval for every tool regardless of configuration.

```python
# streaming.py:1552-1565 (current)
def _approval_required(self, tool_name: str) -> bool:
    if tool_name not in self.mcp_tool_to_server:
        return False
    mcp_server = self.mcp_tool_to_server[tool_name]
    if mcp_server.require_approval == "always":
        return True
    if mcp_server.require_approval == "never":
        return False
    if isinstance(mcp_server, ApprovalFilter):          # BUG: always False
        if mcp_server.always and tool_name in mcp_server.always:
            return True
        if mcp_server.never and tool_name in mcp_server.never:
            return False
    return True                                          # <- always reached
```

### Steps to reproduce

```python
"""Minimal reproduction: ApprovalFilter.never list is ignored."""

from llama_stack_api.openai_responses import ApprovalFilter, OpenAIResponseInputToolMCP

mcp_server = OpenAIResponseInputToolMCP(
    server_label="my-server",
    server_url="http://localhost:9999/mcp",
    require_approval=ApprovalFilter(
        never=["safe_tool"],
        always=["dangerous_tool"],
    ),
)

mcp_tool_to_server = {"safe_tool": mcp_server, "dangerous_tool": mcp_server}


def _approval_required(tool_name: str) -> bool:
    """Verbatim from streaming.py:1552-1565"""
    if tool_name not in mcp_tool_to_server:
        return False
    mcp_server = mcp_tool_to_server[tool_name]
    if mcp_server.require_approval == "always":
        return True
    if mcp_server.require_approval == "never":
        return False
    if isinstance(mcp_server, ApprovalFilter):
        if mcp_server.always and tool_name in mcp_server.always:
            return True
        if mcp_server.never and tool_name in mcp_server.never:
            return False
    return True


print(f"isinstance(mcp_server, ApprovalFilter)                = {isinstance(mcp_server, ApprovalFilter)}")
print(f"isinstance(mcp_server.require_approval, ApprovalFilter) = {isinstance(mcp_server.require_approval, ApprovalFilter)}")
print()
print(f"_approval_required('safe_tool')      = {_approval_required('safe_tool')}")
print(f"  Expected: False (tool is in 'never' list)")
print(f"_approval_required('dangerous_tool') = {_approval_required('dangerous_tool')}")
print(f"  Expected: True  (tool is in 'always' list)")
```

**Output:**

```
isinstance(mcp_server, ApprovalFilter)                = False
isinstance(mcp_server.require_approval, ApprovalFilter) = True

_approval_required('safe_tool')      = True
  Expected: False (tool is in 'never' list)
_approval_required('dangerous_tool') = True
  Expected: True  (tool is in 'always' list)
```

`safe_tool` returns `True` (approval required) despite being explicitly in the `never` list.

### Fix

Change `isinstance(mcp_server, ApprovalFilter)` to `isinstance(mcp_server.require_approval, ApprovalFilter)` and update the field accesses accordingly:

```python
if isinstance(mcp_server.require_approval, ApprovalFilter):
    if mcp_server.require_approval.always and tool_name in mcp_server.require_approval.always:
        return True
    if mcp_server.require_approval.never and tool_name in mcp_server.require_approval.never:
        return False
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `008cbab03aafb6e2a319edf2729333ab9c43eb4e`.  There
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
{"case_id": "ogx_ai_ogx__5287__008cbab",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
