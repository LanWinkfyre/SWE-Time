# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
SCSS partial imported through tsconfig alias is unresolved and cascades to unused-file

# SCSS partial imported through tsconfig alias is unresolved and cascades to unused-file

## Summary

Fallow resolves these independently:

- a tsconfig path alias targeting an ordinary `.scss` file;
- an extensionless relative Sass import targeting an underscore partial.

It does not resolve their valid combination: a tsconfig path alias whose target
is an underscore Sass partial while the import omits the underscore and
extension.

## Minimal reproduction

Repository/fixture contents are in the attached
`fallow-sass-alias-repro` directory.

```json
// tsconfig.json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*"]
}
```

```scss
// src/alias-partial-entry.scss
@use "@/styles/tokens";

.alias-partial {
  color: tokens.$color;
}
```

```scss
// src/styles/_tokens.scss
$color: red;
```

```sh
corepack enable
pnpm dlx fallow@3.9.1 dead-code --no-cache --format json
```

## Expected

Exit 0 with no issues. Sass resolves `@/styles/tokens`, after alias expansion,
to `src/styles/_tokens.scss`.

## Actual

Exit 1:

```text
unresolved-import  src/alias-partial-entry.scss:1  @/styles/tokens
unused-file       src/styles/_tokens.scss
```

The unused-file finding is a cascade from the missing graph edge.

## Controls

The attached fixture also proves:

- `@use "@/styles/plain"` resolves through the same alias to
  `src/styles/plain.scss`;
- `@use "./styles/palette"` resolves through the Sass partial convention to
  `src/styles/_palette.scss`;
- spelling `@use "@/styles/_tokens.scss"` explicitly returns 0 issues on
  Fallow 3.10.0.

Only alias expansion followed by Sass partial probing is missing.

## Versions

Tested on macOS arm64 with Node.js 24:

| Fallow | Result |
| --- | --- |
| 2.103.0 | pass |
| 2.104.0 | fail |
| 3.0.0 | fail |
| 3.5.0 | fail |
| 3.5.1 | fail |
| 3.9.1 | fail |
| 3.10.0 | fail |

The boundary coincides with `oxc_resolver` 11.21.0 → 11.21.3. The relevant
Fallow SCSS/alias algorithm is otherwise unchanged between 2.103.0 and
2.104.0, so that dependency update may have exposed the latent composition
gap.

The issue is still present in current Fallow 3.10.0.

## Analysis ownership

On the included changed Git fixture, these both emit the identical two
`dead_code` findings:

```sh
npm run audit:no-css
npm run audit:css
```

Therefore this is dead-code/module-graph resolution, not CSS styling analytics.

## Relevant implementation

- `try_scss_partial_fallback` probes `_filename`, but from the original
  specifier and importer:
  <https://github.com/fallow-rs/fallow/blob/v3.9.1/crates/graph/src/resolve/fallbacks.rs#L78-L121>
- `try_tsconfig_alias_target` expands the alias and probes normal extensions
  and `index.*`, but not an underscore-prefixed basename:
  <https://github.com/fallow-rs/fallow/blob/v3.9.1/crates/graph/src/resolve/specifier.rs#L790-L822>
- Fallow documents both tsconfig aliases and SCSS underscore partials:
  <https://github.com/fallow-rs/docs/blob/main/configuration/workspaces.mdx>
  and
  <https://github.com/fallow-rs/docs/blob/main/analysis/css-analysis.mdx>.

## Suggested regression test/fix

After expanding a tsconfig alias target for an SCSS/Sass or SFC-style edge,
apply the Sass candidate order to that expanded path, including:

```text
target.scss
_target.scss
target/_index.scss
```

and the equivalent `.sass`/plain-index candidates. The regression test should
assert both:

1. no unresolved import for the alias + underscore-partial edge;
2. no unused-file finding for the reached partial.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `92623a5f54a52e1834318256218ba989efadeefc`.  There
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
{"case_id": "fallow_rs_fallow__2075__92623a5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
