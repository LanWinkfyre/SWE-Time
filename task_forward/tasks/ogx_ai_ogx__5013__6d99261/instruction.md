# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Allow llama stack to deploy with OpenAIMixin models in registered_resources without Provider API Keys

### 🚀 Describe the new functionality needed

Add a skip_model_availability configuration option for remote providers and models that bypasses model availability checks during llama-stack server startup. This would allow models consuming the OpenAIMixin to be registered with placeholder API keys, deferring authentication to inference time when real API keys are provided via the X-LlamaStack-Provider-Data header.

**Example:**
```
providers:
    inference:
      - provider_id: openai
        provider_type: remote::openai
        config:
          api_key: placeholder_key
          skip_model_availability: true  # Skip checks at startup

  registered_resources:
    models:
      - provider_id: anthropic
        model_id: claude-haiku-4-5-20251001
        model_type: llm
        skip_model_availability: true  # Or override at model level
```

### 💡 Why is this needed? What if we don't build it?

In environments where a single llama-stack instance serves multiple users/tenants, the current architecture forces operators to mount a shared API key when they want to make a model visible for all users through `/v1/models` and just want them to provide auth. This creates several problems:
  1. A shared API key represents a single point of compromise and violates the principle of least privilege
  2. Usage from all tenants is billed to a single API key, making it impossible to track per-user costs
  3. All tenants share the same rate limits instead of having independent quotas
  4. One tenant's usage can exhaust the quota for all others

If we don't build it: Users deploying llama-stack for multi-tenant use will need to provide a shared API key when making a model visible for everyone in that instance.

### Other thoughts

Added complexity: If the skip_model_availability field is added to the schema for providers and registered, the openAIMixin would just need something like this added to `register_model`

```python
    async def register_model(self, model: Model) -> Model:
        # START OF CHANGE
        # Check if we should skip availability check (model-level overrides provider-level)
        model_level_skip = model.metadata.get('skip_model_availability') if model.metadata else None
        provider_level_skip = hasattr(self.config, 'skip_model_availability') and self.config.skip_model_availability

        should_skip = model_level_skip if model_level_skip is not None else provider_level_skip

        if should_skip:
            logger.debug(f"Skipping model availability check for {model.provider_model_id} (skip_model_availability=true)")
            return model
        # END OF CHANGE

        if not await self.check_model_availability(model.provider_model_id):
            raise ValueError(f"Model {model.provider_model_id} is not available from provider {self.__provider_id__}")  # type: ignore[attr-defined]
        return model
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6d99261ccced8d55b5080b388cecf75334756063`.  There
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
{"case_id": "ogx_ai_ogx__5013__6d99261",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
