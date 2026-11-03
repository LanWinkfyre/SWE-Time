# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
health.thresholdOverrides is ignored for synthetic <template> findings (Svelte)

Thanks for fallow — we adopted it last week over knip, largely because it catches unused class members that knip does not. The dead-code half has been accurate on our SvelteKit repo, including through a `window.__ns = await import(...)` namespace-assignment pattern that no static tool could see (we suppressed those explicitly).

Two things came up around `health` on `.svelte` files. The first is a concrete bug with a standalone repro.

## 1. `health.thresholdOverrides` never applies to synthetic `<template>` findings

**Version:** fallow 3.14.0 (npm)

**Repro** — three files, no private code:

`src/Widget.svelte`
```svelte
<script lang="ts">
	let { items = [] }: { items: { id: string; on: boolean; n: number }[] } = $props();
</script>

{#each items as it (it.id)}
	{#if it.on}
		{#if it.n > 10}<b>big</b>{:else if it.n > 5}<i>mid</i>{:else}<span>small</span>{/if}
	{:else if it.n > 0}
		{#if it.n > 3}<u>x</u>{:else}<em>y</em>{/if}
	{:else}
		<span>{it.n > 2 ? 'a' : it.n > 1 ? 'b' : 'c'}</span>
	{/if}
{/each}
```

`.fallowrc.json`
```json
{ "health": { "thresholdOverrides": [
    { "files": ["src/Widget.svelte"], "maxCognitive": 500, "maxCyclomatic": 500,
      "reason": "should exempt this file" } ] } }
```

`package.json` with `svelte` as a devDependency.

**Run:** `fallow health --format json`

**Expected:** no finding — the override sets both ceilings to 500.

**Actual:**
```
src/Widget.svelte <template> cyc=9 cog=21 high
```

The override is definitely parsed: a typo'd key is a hard error (`unknown field 'maxCognitiveTYPO', expected one of files, functions, maxCyclomatic, maxCognitive, maxCrap, maxUnitSize, reason`), so this is not a config-shape mistake. On our real repo I narrowed it from `**/*.svelte` to `src/**/*.svelte` to a single exact file path — the synthetic `<template>` finding survived all three.

Real-function findings in the same run respect the override normally, so it looks like the synthetic finding is constructed on a path that bypasses per-file threshold resolution.

## 2. `<template>` complexity on Svelte is an Angular-shaped metric

Lower priority, and arguably a docs/scope question rather than a bug.

`fallow explain "high complexity"` describes `<template>` findings entirely in Angular terms — `.html` templates and inline `@Component({ template: ... })` literals, counting `@if`/`@for`/`@case`/`@defer`/`*ngIf`/`*ngFor` — and the remediation advice is "split the template into child components, hoist data into the component class as computed signals". The metric nonetheless fires on `.svelte` files, where none of that syntax or structure exists.

The practical consequence is that it does not appear to model `{#snippet}` / `{@render}`, which is Svelte 5's own decomposition primitive. Measured on our repo: extracting a 49-line row body out of a nested `{#each}` into a top-level `{#snippet}` moved the component 74 → 62 cognitive, and it stayed `critical` and stayed in `Refactoring targets`. Since a snippet is markup reuse in the same file, the score reads an organised template much like a monolithic one, and the only move that meaningfully changes it is splitting into additional `.svelte` files.

In a SvelteKit app that split has real costs a complexity score cannot see — props plumbing, element `id`s that E2E selectors key off, and copy that an i18n extractor pulls from markup — so we ended up ranking seven components as targets that we concluded were not work.

Would you consider either treating `{#snippet}` bodies as their own units for Svelte, or scoping the synthetic `<template>` finding to the frameworks it is calibrated for? Happy to test a patch against a real SvelteKit codebase if that is useful.

Either way, issue 1 is the one that matters — without it there is no way to opt out per file.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6b61518bb8d55ad8e8eca7eff525cd3445c4e0f0`.  There
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
{"case_id": "fallow_rs_fallow__2163__6b61518",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
