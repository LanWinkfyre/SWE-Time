# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
Support skill detection in APM-installed projects (.apm/ convention)

## Problem

When using [APM (Agent Package Manager)](https://aka.ms/apm) to manage skills, `waza run` fails with workspace detection:

```
no eval.yaml specified and workspace detection failed: no skills detected in workspace
```

This happens because APM installs compiled skills to a nested path:

```
skills/
  my-skill/
    apm.yml               ← source definition
    .apm/
      skills/
        my-skill/
          SKILL.md        ← compiled output (what agents actually receive)
```

But waza's workspace detection looks for `SKILL.md` one level deep:

```
skills/
  my-skill/
    SKILL.md              ← waza expects here
```

Since waza ignores dotfolders (`.apm`), the SKILL.md is never found.

## Context

`.apm/` is APM's standard output directory for compiled primitives — analogous to `node_modules/` for npm or `.venv/` for Python. Every skill installed or compiled via APM places its resolved `SKILL.md` at:

```
<skill-dir>/.apm/skills/<skill-name>/SKILL.md
```

This is the canonical file that agent clients (Copilot, Claude, Cursor, etc.) receive — not a deployment-specific artifact.

## Expected Behavior

`waza run` (and workspace detection in general) should recognize skills installed via APM, either by:

1. **Traversing `.apm/skills/` within each skill directory** as a known convention, or
2. **Adding a `paths.skillFile` config option** to `.waza.yaml` that lets projects specify the relative path to the SKILL.md within each skill folder (e.g., `.apm/skills/{name}/SKILL.md`), or
3. **Documenting an official integration path** for APM-managed workspaces.

## Current Workaround

Creating symlinks after `apm install`:

```bash
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  ln -s ".apm/skills/${skill_name}/SKILL.md" "${skill_dir}SKILL.md"
done
```

This works but is fragile (breaks on Windows, requires gitignore hygiene, not a first-class integration).

## Environment

- waza version: `x.x.x`
- APM version: `0.20.0`
- OS: macOS
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6157165282fcd4e39b4335d4aee502610b58cead`.  There
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
{"case_id": "microsoft_waza__400__6157165",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
