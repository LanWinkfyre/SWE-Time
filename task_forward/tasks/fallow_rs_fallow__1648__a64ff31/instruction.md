# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-component-props: opt-in config to treat leading-underscore destructured props as intentionally-unused

### Summary

Follow-up to #1641 / #1643. The directive-shorthand fix (`bind:`/`style:`/`class:`) has landed in #1643 — thank you. The second half of #1641 (Repro 3) was deliberately left out of scope: the **`_`-prefix "accepted-but-intentionally-unused" destructure convention**. This requests an opt-in config to honor it.

### Motivation

Svelte 5 components frequently accept a prop for **public-API stability** while not consuming it internally (yet). The established lint convention — mirroring TypeScript `noUnusedParameters` and ESLint `@typescript-eslint/no-unused-vars` `argsIgnorePattern`/`varsIgnorePattern: "^_"` — is to alias the destructure with a leading underscore:

```svelte
<script lang="ts">
  interface Props { stage: string; variant?: string; onClose: () => void; }
  let { stage: _stage, variant: _variant = 'badge', onClose: _onClose }: Props = $props();
</script>
```

These are intentional (received-and-ignored), not dead code. On a SvelteKit 5 codebase this is **26 findings across 24 components** even after the #1643 directive-shorthand fix, which forces the whole `unused-component-props` rule to stay disabled.

### Request

A config flag mirroring the TS/ESLint precedent, e.g.:

```jsonc
"rules": { "unused-component-props": { "ignorePattern": "^_" } }
```

(or a boolean such as `ignoreUnderscorePrefixed: true`). Default behavior unchanged — opt-in only.

### Prior art

- TypeScript `noUnusedParameters` + leading-underscore exemption
- ESLint `@typescript-eslint/no-unused-vars` `argsIgnorePattern` / `varsIgnorePattern`

### Environment

fallow 2.102.0 (will retest against the first release carrying #1643), SvelteKit 5 runes (`$props()`, `$bindable()`).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a64ff318455f77583bbe9d4805792fc5da7e2962`.  There
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
{"case_id": "fallow_rs_fallow__1648__a64ff31",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
