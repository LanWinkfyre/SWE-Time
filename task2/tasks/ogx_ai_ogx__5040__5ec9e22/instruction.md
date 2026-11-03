# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
feat: inference passthrough provider for forwarding request headers

## Describe the new functionality needed

Add an inference passthrough provider that forwards per-request auth headers to a downstream OpenAI-compatible service. Follows the `forward_headers` pattern established by the safety passthrough provider (PR #5004).

The provider reads a `forward_headers` mapping from config — a `dict[str, str]` of provider-data keys to outbound HTTP header names. Only the keys listed are forwarded from `X-LlamaStack-Provider-Data` to the downstream service (default deny). This lets deployers wire per-request credentials through to backend inference services without
hard-coding them in the stack config.

**Config example:**
```yaml
providers:
  inference:
    - provider_id: maas-inference
      provider_type: remote::passthrough
      config:
        base_url: http://inference-service:8080
        forward_headers:
          maas_api_token: "Authorization"
          tenant_id: "X-Tenant-ID"
```

Clients pass per-request credentials via `X-LlamaStack-Provider-Data`. Only keys listed in `forward_headers` are mapped to outbound HTTP headers on each downstream call.

## Why is this needed? What if we don't build it?

Multi-tenant deployments need to forward user-specific auth tokens to downstream inference backends on a per-request basis. Without this, every request uses the same static credentials from config, making it impossible to support per-user authorization against backends like IBM watsonx, Azure, or internal endpoints.

This is the inference counterpart to the safety passthrough in PR #5004.

## Other thoughts

- Extends the existing inference passthrough adapter rather than adding a new one
- Refactor common `forward_headers` logic from the safety provider into a shared
  base so each subsequent provider is a thin integration
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5ec9e22753a9ca4a0354e55f595937be178c4a1a`.  There
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
{"case_id": "ogx_ai_ogx__5040__5ec9e22",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
