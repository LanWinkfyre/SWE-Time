# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Support Svelte virtual modules in type-aware TypeScript projects

### Problem

Fallow's type-aware TypeScript-Go pass cannot analyze a valid SvelteKit project when a TypeScript barrel re-exports named module-script exports from a `.svelte` component. The project is clean under the framework-aware authority, `svelte-check`, but Fallow constructs a raw TypeScript program, sees only the ambient `"*.svelte"` module, reports structural `TS2614` diagnostics, and marks the whole selected project unavailable.

This blocks checker-backed Fallow questions for Svelte application code even though Fallow's syntactic Svelte support and the application's supported check are healthy.

Public reproduction: [`speechmetrics/speechcatcher`, `apps/test-builder`](https://github.com/speechmetrics/speechcatcher/tree/dev/apps/test-builder) (tracking issue [speechmetrics/speechcatcher#1560](https://github.com/speechmetrics/speechcatcher/issues/1560)).

Relevant source shape:

```svelte
<!-- button.svelte -->
<script lang="ts" module>
  export const buttonVariants = /* ... */;
  export type ButtonVariant = /* ... */;
  export type ButtonSize = /* ... */;
  export type ButtonProps = /* ... */;
</script>
```

```ts
// index.ts
export {
  type ButtonProps as Props,
  type ButtonProps,
  type ButtonSize,
  type ButtonVariant,
  buttonVariants,
  default as Root,
  default as Button,
} from "./button.svelte";
```

With Fallow 3.16.0 (protocol 6, TypeScript-Go 7.0.2):

```bash
fallow health \
  --root "$PWD" \
  --type-aware \
  --type-coupling \
  --type-aware-project apps/test-builder/tsconfig.json \
  --type-aware-require best-effort \
  --format json \
  --quiet
```

The type-aware metadata reports:

```json
{
  "identity": { "completeness": "unavailable" },
  "projects": [
    {
      "config": "apps/test-builder/tsconfig.json",
      "status": "unavailable",
      "blocking_diagnostic_count": 7,
      "source_file_count": 2381,
      "reason_code": "blocking-diagnostics"
    }
  ]
}
```

Raw TypeScript 6.0.3 and TypeScript-Go 7.0.2 both emit the same five `TS2614` source diagnostics for the named re-exports. In contrast, both the repository-pinned `svelte-check` 4.4.8 and current 4.7.6 report:

```text
svelte-check found 0 errors and 0 warnings
```

Fallow 3.15.0 and an isolated upgrade to 3.16.0 produce the same unavailable result. Current Svelte language-tools explicitly documents that TypeScript 7 needs Svelte's `--tsgo`/`--tsgo-experimental-api` host path, and a Svelte maintainer explains that tsgo currently has no equivalent to the TypeScript language-service plugin API that exposes named Svelte exports: [sveltejs/language-tools#3083](https://github.com/sveltejs/language-tools/issues/3083#issuecomment-5065008267).

### Proposed solution

Provide a supported Svelte-aware type-aware project path—ideally by integrating the Svelte language-tools TypeScript-Go host/preprocessing seam—so `.svelte` virtual modules participate in Fallow's semantic program and completeness can be `complete` for a healthy SvelteKit tsconfig.

If framework preprocessing cannot be integrated yet, it would still help to:

1. detect this Svelte/`TS2614` compatibility shape explicitly;
2. return a stable Svelte-specific reason code/remediation link rather than a generic blocking-diagnostics result; and
3. document whether a generated semantic project is supported (currently we are avoiding an application-maintained `svelte2tsx` mirror because it would duplicate `svelte-check`, complicate source identity/maps, and may not preserve Fallow's exact-symbol guarantees).

TypeScript and `svelte-check` should remain the compiler/framework authorities; the goal is to make Fallow's own project-wide semantic capabilities available without changing valid Svelte APIs solely to satisfy raw TypeScript.

### Alternatives considered

- **Upgrade Fallow:** 3.16.0 still reports the same seven blockers.
- **Upgrade Svelte tooling:** current `svelte-check` 4.7.6 is clean, but Fallow does not use its Svelte-aware host; package upgrades cannot change the raw sidecar program model.
- **Add `typescript-svelte-plugin`:** TypeScript-Go 7 currently lacks the corresponding plugin API, and Fallow's sidecar does not load the TypeScript language-service plugin path.
- **Move module-script exports into a `.ts` file:** rejected because these are valid component-owned Svelte APIs and the application should not be reshaped only to appease raw TypeScript.
- **Generate and maintain a `svelte2tsx` mirror tsconfig:** rejected as an unsupported repository workaround unless Fallow defines how virtual-file identity, source maps, diagnostics, and exact-symbol evidence remain trustworthy.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `95a7ae9faf9e987616fe2366b74e99626dfd58c6`.  There
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
{"case_id": "fallow_rs_fallow__2270__95a7ae9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
