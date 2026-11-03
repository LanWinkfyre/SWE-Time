# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Playwright fixture method usages are missed through branch-selected aliases, and `mergeTests(...)` misses direct usages entirely

### What happened?

## Summary

I am seeing false positives from `fallow dead-code` in Playwright tests.

There appear to be two related cases:

1. Inside a normal `base.extend(...)` Playwright fixture callback, direct method calls are detected, but method calls made through a local variable selected by a ternary, multiline `if/else`, or `switch` are reported as unused.
2. Inside a `mergeTests(...)`-based fixture wrapper, even direct method calls are reported as unused.

- Plain TypeScript without Playwright works correctly.
- In Playwright fixture callbacks created with `base.extend(...)`, methods called through a branch-selected local variable are reported as unused.
- In Playwright fixture callbacks created through `mergeTests(...)`, even direct calls are reported as unused.

### Reproduction

### `reader.ts`

```ts
export class SingleReader {
	directControl(): void {}

	ternarySelected(): void {}

	ifElseSelected(): void {}

	switchSelected(): void {}

	ifElseDirect(): void {}

	switchDirect(): void {}
}

export class MergedReader {
	directControl(): void {}

	ternarySelected(): void {}

	ifElseSelected(): void {}

	switchSelected(): void {}

	ifElseDirect(): void {}

	switchDirect(): void {}
}
```

### `single-fixture.ts`

```ts
import { test as base } from "@playwright/test";

import { SingleReader } from "./reader";

type SingleFixtures = {
	readerA: SingleReader;
	readerB: SingleReader;
};

export const testSingle = base.extend<SingleFixtures>({
	readerA: async ({}, use) => {
		await use(new SingleReader());
	},
	readerB: async ({}, use) => {
		await use(new SingleReader());
	},
});
```

### `merged-fixture.ts`

```ts
import { mergeTests, test as base } from "@playwright/test";

import { MergedReader } from "./reader";

const testA = base.extend<{ readerA: MergedReader }>({
	readerA: async ({}, use) => {
		await use(new MergedReader());
	},
});

const testB = base.extend<{ readerB: MergedReader }>({
	readerB: async ({}, use) => {
		await use(new MergedReader());
	},
});

export const testMerged = mergeTests(testA, testB);
```

### `single-fixture-branch.test.ts`

```ts
import { testSingle } from "./single-fixture";

testSingle("single direct control", async ({ readerA }) => {
	readerA.directControl();
});

testSingle("single ternary selected", async ({ readerA, readerB }) => {
	const reader = process.env.DB_SCHEMA === "A" ? readerA : readerB;
	reader.ternarySelected();
});

testSingle("single if else selected", async ({ readerA, readerB }) => {
	let reader;
	if (process.env.DB_SCHEMA === "A") {
		reader = readerA;
	} else {
		reader = readerB;
	}
	reader.ifElseSelected();
});

testSingle("single switch selected", async ({ readerA, readerB }) => {
	let reader;
	switch (process.env.DB_SCHEMA) {
		case "A":
			reader = readerA;
			break;
		default:
			reader = readerB;
			break;
	}
	reader.switchSelected();
});

testSingle("single if else direct", async ({ readerA, readerB }) => {
	if (process.env.DB_SCHEMA === "A") {
		readerA.ifElseDirect();
	} else {
		readerB.ifElseDirect();
	}
});

testSingle("single switch direct", async ({ readerA, readerB }) => {
	switch (process.env.DB_SCHEMA) {
		case "A":
			readerA.switchDirect();
			break;
		default:
			readerB.switchDirect();
			break;
	}
});
```

### `merged-fixture-branch.test.ts`

```ts
import { testMerged } from "./merged-fixture";

testMerged("merged direct control", async ({ readerA }) => {
	readerA.directControl();
});

testMerged("merged ternary selected", async ({ readerA, readerB }) => {
	const reader = process.env.DB_SCHEMA === "A" ? readerA : readerB;
	reader.ternarySelected();
});

testMerged("merged if else selected", async ({ readerA, readerB }) => {
	let reader;
	if (process.env.DB_SCHEMA === "A") {
		reader = readerA;
	} else {
		reader = readerB;
	}
	reader.ifElseSelected();
});

testMerged("merged switch selected", async ({ readerA, readerB }) => {
	let reader;
	switch (process.env.DB_SCHEMA) {
		case "A":
			reader = readerA;
			break;
		default:
			reader = readerB;
			break;
	}
	reader.switchSelected();
});

testMerged("merged if else direct", async ({ readerA, readerB }) => {
	if (process.env.DB_SCHEMA === "A") {
		readerA.ifElseDirect();
	} else {
		readerB.ifElseDirect();
	}
});

testMerged("merged switch direct", async ({ readerA, readerB }) => {
	switch (process.env.DB_SCHEMA) {
		case "A":
			readerA.switchDirect();
			break;
		default:
			readerB.switchDirect();
			break;
	}
});
```

## Observed results

The direct non-Playwright control case works:

- A plain TypeScript file that selects an object through ternary, `if/else`, and `switch`, then calls methods on it, produces `0` issues.

The Playwright cases fail like this:

- In `single-fixture-branch.test.ts`, these are reported as unused even though they are called:
  - `SingleReader.ternarySelected`
  - `SingleReader.ifElseSelected`
  - `SingleReader.switchSelected`
- In `merged-fixture-branch.test.ts`, these are reported as unused even though they are called:
  - `MergedReader.directControl`
  - `MergedReader.ternarySelected`
  - `MergedReader.ifElseSelected`
  - `MergedReader.switchSelected`
  - `MergedReader.ifElseDirect`
  - `MergedReader.switchDirect`

### Expected behavior

Those methods should not be reported as dead code

### Fallow version

2.96.0

### Operating system

Windows

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d3e1c727cd39146c95bd1a8111971043e927f480`.  There
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
{"case_id": "fallow_rs_fallow__1270__d3e1c72",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
