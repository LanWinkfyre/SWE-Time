# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Containers API: core API structure (src/ogx_api/containers)

Sub-issue of #5892 covering the declarative API surface only — no provider implementation, no router wiring, no policy enforcement.

Scope (issue #5892 tasks 1–7):

- [ ] 1. Add `Api.containers` and `Api.container_runtime` to the Api enum in `src/ogx_api/datatypes.py`
- [ ] 2. Create Containers API data models — `Container`, `ContainerFile`, `ExpiresAfter`, `NetworkPolicy`, `NetworkPolicyExtended`, `NetworkDomainCredential`, `NetworkCredential`, `ContainerCreateRequest`
- [ ] 3. Create `ShellEnvironment` model — discriminated union of `container_auto`, `container_reference`, `local`
- [ ] 4. Create `ShellCallOutput`, `ShellOutcome` execution models
- [ ] 5. Create Containers API protocol in `src/ogx_api/containers/api.py`
- [ ] 6. Create ContainerRuntime protocol — lifecycle + file management + `execute_shell()` + `mount_skills()`
- [ ] 7. Create Containers FastAPI routes — all endpoints under `/v1alpha`

Out of scope (tracked in #5892): tasks 8–36 — policy enforcement, the `inline::builtin` Containers provider, ContainerRuntime registries, router and resolver wiring, the `inline::local` Docker/Podman runtime, Responses shell-tool integration, distribution configs, OpenAI coverage updates, and tests.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `96dc3656af7eb5773986fa5523ca569365c158ea`.  There
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
{"case_id": "ogx_ai_ogx__5912__96dc365",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
