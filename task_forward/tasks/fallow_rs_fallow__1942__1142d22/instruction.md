# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
False positive: ignored TypeScript paths alias reported as unlisted dependency

### What happened?

Related to https://github.com/fallow-rs/fallow/issues/1911.

The TypeScript `paths` alias fix in Fallow 3.7.1 works for normal local targets, but a resolved alias is again classified as an npm package when its local target matches `ignorePatterns`.

### Reproduction

Create a new directory containing these files.

### package.json

```json
{
	"name": "fallow-ignored-alias-repro",
	"private": true,
	"devDependencies": {
		"fallow": "3.7.1",
		"typescript": "^5.9.3"
	}
}
```

### tsconfig.json

```json
{
	"compilerOptions": {
		"module": "commonjs",
		"target": "ES2022",
		"paths": {
			"@synthetic/*": ["./sparta/*"]
		}
	},
	"include": ["src/**/*.ts", "sparta/**/*.ts"]
}
```

### .fallowrc.json

```json
{
	"entry": ["src/entry.ts"],
	"ignorePatterns": ["sparta/api/local-module.ts"],
	"rules": {
		"unlisted-dependencies": "error",
		"unresolved-imports": "error"
	}
}
```

### src/entry.ts

```ts
import { localValue } from "@synthetic/api/local-module";

console.log(localValue);
```

### sparta/api/local-module.ts

```ts
export const localValue = "resolved inside the workspace";
```

Run:

```sh
npm install
npx tsc --noEmit
npx fallow dead-code --format json --unlisted-deps --unresolved-imports --explain
```

## Actual behavior

TypeScript resolves the alias successfully.

Fallow 3.7.1 reports:

```text
unlisted_dependencies : 1
unresolved_imports    : 0

package_name  : @synthetic/api
imported_from : src/entry.ts
```

### Expected behavior

`@synthetic/api/local-module` matches `compilerOptions.paths` and resolves to a local workspace file. It should remain an internal module edge, irrespective of whether the destination file is ignored for dead-code analysis.

`unlisted_dependencies` should be `0`.

## Control case

Removing this configuration line makes the report disappear:

```json
"ignorePatterns": ["sparta/api/local-module.ts"]
```

So the regression appears to be the interaction between `ignorePatterns` and already-resolved TypeScript path aliases, not the basic alias registration issue fixed by #1911.

### Fallow version

3.7.1

### Operating system

Windows

### Configuration

```toml
{
	"entry": ["src/entry.ts"],
	"ignorePatterns": ["sparta/api/local-module.ts"],
	"rules": {
		"unlisted-dependencies": "error",
		"unresolved-imports": "error"
	}
}
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1142d229914e21b25dba587d48983ecd6fb06fd4`.  There
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
{"case_id": "fallow_rs_fallow__1942__1142d22",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
