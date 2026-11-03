# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
LSP diagnostics ignore overrides[].rules after loading .fallowrc.json

## Summary

`fallow-lsp` loads `.fallowrc.json` but still publishes inline diagnostics for rules that `overrides[].rules` set to `"off"` for the matching file.

`fallow dead-code` (and the VS Code Unused Code sidebar, which shells out to that CLI) applies the override and reports no finding.

## Expected

After the language server loads the project config, inline diagnostics should match `fallow dead-code` for file-scoped rules. A path that matches `overrides[].files` with `unused-exports: "off"` or `private-type-leaks: "off"` should not get those squiggles.

## Actual

The server logs `loaded config: <root>/.fallowrc.json`, then still paints:

- `Export 'X' is unused` (`unused-export`)
- `Export 'X' references private type 'Y'` (`private-type-leak`)

on files whose override turns those rules off.

## Repro

```jsonc
// .fallowrc.json
{
  "rules": {
    "unused-exports": "warn",
    "private-type-leaks": "warn"
  },
  "overrides": [
    {
      "files": ["src/ui/**"],
      "rules": {
        "unused-exports": "off",
        "private-type-leaks": "off"
      }
    }
  ]
}
```

```ts
// src/ui/kit.ts
type Props = { label: string }

export const Unused = (props: Props) => props.label
```

1. Open `src/ui/kit.ts` in VS Code / Cursor with Fallow 3.25.0 (CLI + extension).
2. Run `fallow dead-code --file src/ui/kit.ts`.
3. Compare the Unused Code sidebar to the inline marks.

CLI / sidebar: 0 findings for those rules on that file.  
LSP: unused-export and/or private-type-leak marks remain.

## Where it diverges

Override filtering for file-scoped dead-code rules lives in the CLI:

- `crates/cli/src/check/rules.rs` → `apply_rules` / `apply_core_dead_code_override_rules`
- that pass calls `ResolvedConfig::resolve_rules_for_path` and drops findings whose per-file severity is `Off`

The language server uses the editor analysis facade (`crates/api/src/editor.rs`) and then `build_diagnostics`. That path does not run `apply_rules`, so it publishes the unfiltered result set.

## Environment

- `fallow` 3.25.0 (local `node_modules/@fallow-cli/.../fallow`)
- Fallow VS Code extension 3.25.0
- `fallow lsp-server` from the same local binary
- Confirmed the server loaded the project `.fallowrc.json` (Fallow output channel)

## Ask

Run the same per-file override filter on the editor/LSP analysis path (or move `apply_rules` into the shared engine/API so CLI, sidebar, and inline diagnostics share one result set).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `75ac87337420156a40bd622c43f4245a4f2ba1d4`.  There
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
{"case_id": "fallow_rs_fallow__2621__75ac873",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
