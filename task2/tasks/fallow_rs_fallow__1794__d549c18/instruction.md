# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Ship a local config schema or document a local workflow to avoid VS Code untrusted-schema errors

### Problem

Using the documented `$schema` value in `.fallowrc.json` can trigger a VS Code JSON diagnostic instead of loading the schema:

```text
Unable to load schema from 'https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json': Location https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json is untrusted.
```

That leaves users without schema validation or autocomplete unless they manually trust the remote domain.

## Minimal reproduction

Use synthetic files only.

`package.json`

```json
{
	"name": "fallow-schema-repro",
	"private": true,
	"devDependencies": {
		"fallow": "^3.2.0"
	}
}
```

`.fallowrc.json`

```jsonc
{
	"$schema": "https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json",
	"entry": ["tests/**/*.test.ts"]
}
```

## Steps to reproduce

1. Open the synthetic workspace in VS Code.
2. Open `.fallowrc.json`.
3. Wait for JSON schema validation to load.

## Actual behavior

VS Code reports that the schema location is untrusted and does not load the schema.

## Expected behavior

Users should get config validation and autocomplete without having to trust an arbitrary remote URL manually.

## Notes

- `fallow config-schema` already makes it possible to generate a local schema.
- A local workaround is to generate a schema file and point `$schema` at that local path.
- There is also a documentation inconsistency today:
	- the generated schema description says to use `https://fallow.dev/schema.json`
	- the configuration docs still show `https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json`

### Proposed solution

Any of these would solve the problem cleanly:

1. Ship a stable `schema.json` file inside the npm package and document that local path.
2. Update the docs to recommend a local generated schema workflow via `fallow config-schema`.
3. Align the docs and schema text so there is one canonical recommended schema location.

### Alternatives considered

Maybe a typescript config file with a config Type
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d549c183e792fe48cb785db86dc5b7862d4d3b94`.  There
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
{"case_id": "fallow_rs_fallow__1794__d549c18",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
