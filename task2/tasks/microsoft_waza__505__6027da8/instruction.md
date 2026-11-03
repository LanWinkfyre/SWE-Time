# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
Update registry.json for Waza 0.38.4

## Summary

The Azure Developer CLI extension registry is stale. The registry served from:

https://raw.githubusercontent.com/microsoft/waza/main/registry.json

lists `0.37.0` as the newest available `microsoft.azd.waza` version, while Waza `0.38.4` is the latest release.

## Impact

The Azure Developer CLI installation instructions in `README.md` instruct users to add this registry and install the extension:

```bash
azd ext source add -n waza -t url -l https://raw.githubusercontent.com/microsoft/waza/main/registry.json
azd ext install microsoft.azd.waza
```

Because the registry does not include `0.38.4`, these instructions install `0.37.0` rather than the current release.

## Expected behavior

`registry.json` should include a complete `0.38.4` entry with the correct artifacts, download URLs, checksums, and metadata so `azd ext install microsoft.azd.waza` resolves to the latest Waza version.

## Actual behavior

The highest version currently listed in `registry.json` is `0.37.0`.

## Suggested fix

Update and publish `registry.json` as part of the `0.38.4` release process, and consider adding release automation or validation that verifies the registry's latest version matches the latest Waza release.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6027da837c8ed791ff20ed352892f7144ce670d1`.  There
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
{"case_id": "microsoft_waza__505__6027da8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
