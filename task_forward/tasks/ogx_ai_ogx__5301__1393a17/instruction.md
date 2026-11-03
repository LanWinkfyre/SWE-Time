# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
next_turn_messages.pop() in _separate_tool_calls corrupts conversation history when multiple MCP tool calls require approval

*This bug was identified by Claude.*

## Summary

In `_separate_tool_calls()`, `next_turn_messages.pop()` is called inside the loop over tool calls (lines 721 and 725 of `streaming.py`). When the model returns multiple MCP tool calls that require approval in a single turn, `.pop()` fires once per tool call — but only the first pop removes the intended assistant message. Subsequent pops silently destroy unrelated messages from the conversation history.

With 2 tool calls needing approval, the user message is eaten. With 3+, the system message is also removed (or `IndexError` if the list is exhausted).

## Affected code

https://github.com/llamastack/llama-stack/blob/main/src/llama_stack/providers/inline/responses/builtin/responses/streaming.py#L711-L725

```python
for tool_call in choice.message.tool_calls:
    # ... other branches ...
    else:
        if self._approval_required(tool_call.function.name):
            approval_response = self.ctx.approval_response(...)
            if approval_response:
                if approval_response.approve:
                    non_function_tool_calls.append(tool_call)
                else:
                    next_turn_messages.pop()   # <-- called per tool call
            else:
                approvals.append(tool_call)
                next_turn_messages.pop()       # <-- called per tool call
```

## Reproduction

This script mirrors the exact control flow from `_separate_tool_calls()` (lines 674-729), using simplified stand-ins for the Pydantic models. It simulates a model response containing 3 MCP tool calls that all require approval with no pre-approval response provided:

```python
from dataclasses import dataclass


@dataclass
class ToolCallFunction:
    name: str
    arguments: str = "{}"


@dataclass
class ToolCall:
    id: str
    function: ToolCallFunction


@dataclass
class AssistantMessage:
    content: str | None
    tool_calls: list[ToolCall] | None

    def __repr__(self):
        names = [tc.function.name for tc in (self.tool_calls or [])]
        return f"AssistantMessage(tool_calls={names})"


@dataclass
class ChoiceMessage:
    content: str | None = None
    tool_calls: list[ToolCall] | None = None


@dataclass
class Choice:
    message: ChoiceMessage


def _approval_required(tool_name, mcp_tool_to_server):
    return tool_name in mcp_tool_to_server


def _separate_tool_calls_BUGGY(choices, messages, mcp_tool_to_server):
    """Mirrors the current (buggy) code in streaming.py."""
    approvals = []
    next_turn_messages = messages.copy()

    for choice in choices:
        next_turn_messages.append(
            AssistantMessage(content=choice.message.content, tool_calls=choice.message.tool_calls)
        )

        if choice.message.tool_calls:
            for tool_call in choice.message.tool_calls:
                if _approval_required(tool_call.function.name, mcp_tool_to_server):
                    approval_response = None  # no pre-approval
                    if approval_response:
                        pass
                    else:
                        approvals.append(tool_call)
                        next_turn_messages.pop()  # BUG: called per tool call

    return approvals, next_turn_messages


messages = [
    "SystemMessage('You are a helpful assistant')",
    "UserMessage('What is the weather in NYC, London, and Tokyo?')",
]

tool_calls = [
    ToolCall(id="call_1", function=ToolCallFunction(name="get_weather", arguments='{"city":"NYC"}')),
    ToolCall(id="call_2", function=ToolCallFunction(name="get_weather", arguments='{"city":"London"}')),
    ToolCall(id="call_3", function=ToolCallFunction(name="get_weather", arguments='{"city":"Tokyo"}')),
]

choices = [Choice(message=ChoiceMessage(content=None, tool_calls=tool_calls))]
mcp_tools = {"get_weather": "mcp-server-config"}

approvals, result = _separate_tool_calls_BUGGY(choices, messages, mcp_tools)

print(f"Input messages:  {messages}")
print(f"Output messages: {result}")
print(f"Approvals:       {len(approvals)}")
```

Output:

```
Input messages:  ["SystemMessage('You are a helpful assistant')", "UserMessage('What is the weather in NYC, London, and Tokyo?')"]
Output messages: []
Approvals:       3

PROBLEM: started with 2 messages, ended with 0.
The user message and system message were destroyed.
```

- pop # 1 removes the `AssistantMessage` (correct — this is what the code intended)
- pop # 2 removes the `UserMessage` (history corruption)
- pop # 3 removes the `SystemMessage` (entire conversation history wiped)

## Impact

- **Single tool call needing approval**: works by accident (one pop, correct target)
- **Two tool calls**: silently destroys the user's most recent message — subsequent turns lose context
- **Three+ tool calls**: can crash with `IndexError` or wipe the entire conversation history

This compounds with #5287 (now fixed by #5288), which caused `ApprovalFilter.never` lists to be ignored, making *every* MCP tool require approval and dramatically increasing the likelihood of hitting this multi-pop path.

## Expected behavior

The assistant message should be removed from `next_turn_messages` **at most once** per choice, regardless of how many tool calls within that choice require approval. A flag should track whether removal is needed and execute a single `.pop()` after the inner loop completes.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1393a172bddcf1492602b8de6be4b139a99ef5e5`.  There
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
{"case_id": "ogx_ai_ogx__5301__1393a17",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
