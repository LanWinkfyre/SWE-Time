# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Regression: first streaming token duplicated in /v1/chat/completions


Affected versions: any build after 773489eeb175c7189303011cdcdc24725fa47ec7 / #9244

Symptom: In streaming mode, the first content token for non-reasoning models is sent to the client twice. Reasoning models, non-streaming mode, and /v1/completions are unaffected. Visible in backend traces: `chat_deltas.content` has the first token duplicated, while `response` is correct.

Root cause: 773489ee switched `PredictStream` to `TASK_RESPONSE_TYPE_OAI_CHAT`, which causes `server_task_result_cmpl_partial::to_json_oaicompat_chat()` to return a JSON array. For the first token (n_decoded == 1) that array has two elements: a role-init chunk `{role:"assistant", content:null}` followed by the actual content chunk `{content:"<first token>"}`.

In [`backend/cpp/llama-cpp/grpc-server.cpp`](https://github.com/mudler/LocalAI/blob/master/backend/cpp/llama-cpp/grpc-server.cpp), the loop that processes this array calls `attach_chat_deltas(reply, first_result.get())` for every element with the same `raw_result` pointer. Since `oaicompat_msg_diffs` contains the first token's diff, both the role-init reply and the content reply get `ChatDelta.Content = "<first token>"` stamped on them. Go receives both over gRPC, accumulates both into `allChatDeltas`, and the streaming callback emits the first token's content twice to the SSE client.

Fix: In the array iteration loops in `grpc-server.cpp` (PredictStream, lines ~1721 and ~1747), skip `attach_chat_deltas` for role-init elements — detectable by the presence of `"role"` in `choices[0].delta`:

```cpp
for (const auto & res : res_json) {
    auto reply = build_reply_from_json(res, result.get());
    // Skip role-init elements (delta has "role" key, no actual content/reasoning diffs)
    bool is_role_init = res.contains("choices") && !res["choices"].empty() &&
                        res["choices"][0].value("delta", json::object()).contains("role");
    if (!is_role_init) {
        attach_chat_deltas(reply, result.get());
    }
    writer->Write(reply);
}
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `706cf5d43c324184b8e1df6e8141ce335c591b31`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__9298__706cf5d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
