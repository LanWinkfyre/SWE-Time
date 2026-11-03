# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
json_schema grader rejects documented extract_json option in v0.37.0

## Description

Waza 0.37.0 fails while loading a task that uses the documented `extract_json` option for a `json_schema` grader.

The grader documentation lists `extract_json` as a supported boolean option:
https://microsoft.github.io/waza/guides/graders/#json-schema-json_schema

However, the runtime rejects the field while unmarshalling `models.JSONSchemaGraderParameters`.

## Environment

- Waza: `0.37.0`
- azd extension: `microsoft.azd.waza` (`0.37.0`, up to date)
- OS: Windows
- Invocation: `azd waza run`

## Minimal grader configuration

```yaml
graders:
  - type: json_schema
    name: output_matches_schema
    config:
      schema_file: "skills/architecture-mapper/schemas/architecture-mapper-output.schema.json"
      extract_json: true
```

## Actual result

```text
benchmark failed: failed to load test cases: failed to load test case C:\Users\asilverman\src\AzRel-CURe-Resilience.worktrees\ado-38750792-persona-entrypoint\evals\architecture-mapper\tasks\golden-supported.yaml: parsing test case YAML: invalid grader config for "output_matches_schema" (type "json_schema"): failed to decode grader parameters of type models.JSONSchemaGraderParameters: yaml: unmarshal errors:
  line 2: field extract_json not found in type models.JSONSchemaGraderParameters
```

The failure happens during test-case loading, before the benchmark runs.

## Expected result

Waza should accept `extract_json: true` and extract exactly one JSON document from prose or a Markdown JSON code block before validating it against `schema_file`, as documented.

## Notes

This appears to be a mismatch between the published grader documentation and the `JSONSchemaGraderParameters` model shipped in Waza 0.37.0. Either the runtime model needs the documented field, or the documentation/version availability should clarify when the option is supported.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `96e67ee3e2e60ef788b9269b834a7bd23824a5ca`.  There
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
{"case_id": "microsoft_waza__457__96e67ee",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
