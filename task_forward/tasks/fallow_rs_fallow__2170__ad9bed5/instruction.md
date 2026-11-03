# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
type-aware forces private-type-leaks on, no matter the config

### What happened?

I have recently enabled `type-aware`, and since then I get the "Private type leaks" when running the fallow audit. I tried to turn off the `private-type-leaks` rule (which it is by default), but it seems that with `type-aware` enabled that does not seem to be an option.

This seems like a bug to me, as with the rule explicitly turned off, I would generally expect the rule to be turned off, no matter what.

### Reproduction

1. Enable `type-aware`
2. Leave `private-type-leaks` to the default: `"off"`
3. Run fallow audit
4. Observe "Private type leaks"

### Expected behavior

With `private-type-leaks` turned off, I expect those findings to be omitted from the report, even when `type-aware` is enabled.

### Fallow version

3.14.0

### Operating system

Linux

### Configuration

This is our project's JSON config

```jsonc
{
  // This file is JSONC: fallow reads these comments; generic JSON tools may not.
  "$schema": "https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json",
  "entry": ["src/index.{ts,tsx,js,jsx}", "src/main.{ts,tsx,js,jsx}", "oxfmt.config.ts", "oxlint.config.ts"],
  "workspaces": {
    "patterns": ["admin", "980.tests", "981.tests.pipeline.e2e", "api-mock"],
  },
  "health": {
    // Permit cohesive medium-sized functions while still flagging functions that
    // are genuinely large or difficult to reason about.
    "maxCognitive": 30,
    "maxCrap": 200,
    "crapRefactorBand": 0,
    "maxUnitSize": 500,
  },
  "duplicates": {
    // Hide pair-only clones; focus on widespread copy-paste
    // worth refactoring. Lower to 2 to report every duplicate pair.
    "minOccurrences": 3,
    // Common additions (uncomment to enable):
    // "ignore": [
    //   "**/lib/**",          // for repos that publish transpiled output to lib/
    //   "**/legacy/**",       // for repos with legacy-build artifacts
    //   "**/__generated__/**", // Relay, GraphQL Code Generator
    //   "**/generated/**"     // OpenAPI, Protobuf codegen
    // ]
  },
  "rules": {
    "unused-dependencies": "warn",
    "private-type-leaks": "off"
  },
  "ignoreDependencies": [
    // admin/tsconfig paths: "*": ["./admin/src/*"] — bare imports are local, not npm packages
    "common",
    "features",
    "i18n",
    "menu",
    "pages",
    "routing",
    "test",
    "@emotion/styled",
    "@tanstack/react-query-devtools", // stripped from prod bundles via NODE_ENV guard in the package entry
    "cypress-multi-reporters",
    "mocha-junit-reporter",
    "postinstall-postinstall",
    "fallow-type-aware",
  ],
  "typeAware": {
    "enabled": true,
    "projects": ["tsconfig.json"],
    "require": "best-effort",
  },
}
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ad9bed5c1ee9971d94575f98a1ae88c7fa64a2d4`.  There
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
{"case_id": "fallow_rs_fallow__2170__ad9bed5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
