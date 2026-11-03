# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-component-props (2.102.0): Svelte bind:/style: directive shorthands counted as non-usage (false positives)

### Summary

fallow `2.102.0`'s `unused-component-props` check reports Svelte props as "declared but referenced nowhere" when they are in fact used via **directive shorthands** — `bind:prop` and `style:prop` — and it also flags the conventional **`_`-prefix "accepted-but-unused"** destructure pattern. On a SvelteKit 5 codebase this produced **55 findings that were all false positives**, forcing us to disable the rule.

### Repro 1 — `bind:` shorthand counted as non-usage (false positive)

```svelte
<script lang="ts">
  interface Props { file: FileListItem | null; open: boolean; onClose: () => void; }
  let { file, open = $bindable(), onClose }: Props = $props();
</script>
{#if file}
  <ResizableModal bind:open title={file.filename} {onClose}>
    <!-- … -->
  </ResizableModal>
{/if}
```

fallow reports: `open is declared but referenced nowhere in this component`.
**Actual:** `open` is used by the `bind:open` directive shorthand.

### Repro 2 — `style:` shorthand counted as non-usage (false positive)

```svelte
<script lang="ts">
  let { height = '200px', /* … */ } = $props();
</script>
<div class="cascade-graph-container" style:height>…</div>
```

fallow reports `height … referenced nowhere`. **Actual:** used by `style:height` shorthand.

### Repro 3 — `_`-prefix accepted-but-unused convention (arguably out of scope / should be configurable)

```svelte
let { stage: _stage, variant: _variant = 'badge', /* … */ } = $props();
```

fallow flags `stage`/`variant`. These are intentionally received-and-ignored props (public-API stability), renamed with a leading `_` per a common lint convention.

### Expected

- `bind:prop` / `style:prop` (and by extension the other directive shorthands — `class:`, `use:`, `transition:`/`in:`/`out:`, `animate:`) that reference a declared prop should count as a usage → no finding.
- Optionally, a config to treat `_`-prefixed destructured props as intentionally unused.

### Likely cause

The check appears to walk `{expression}` mustache usages and explicit attribute values but miss shorthand **directive bindings**, where the attribute name *is* the prop reference.

### Environment

- fallow 2.102.0 (`@fallow-cli/*` pinned binaries)
- SvelteKit 5 (runes: `$props()`, `$bindable()`), `framework: svelte`, whole-repo `fallow` run

Until this is fixed we've set `rules.unused-component-props: "off"`.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2a348354c0102d245827e063e16b07ac43e38ba4`.  There
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
{"case_id": "fallow_rs_fallow__1641__2a34835",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
