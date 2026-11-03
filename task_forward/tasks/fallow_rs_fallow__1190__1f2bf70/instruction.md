# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-class-members false positive through a Playwright fixture getter/factory chain

### What happened?

`fallow` reports class methods as `unused-class-members` even though they are called from an entry test.

The minimal shape is:

1. A class instance is created lazily behind a getter in a factory class.
2. That instance is exposed through a nested `base.extend(...)` Playwright fixture object.
3. A test calls methods on that nested fixture property.

The methods are clearly used from the test, but they are still reported as unused.

This does not look like an `entry` problem, because the spec file is an entry point and the class file is reachable. It also does not look like an `ignoreDecorators` problem, because `@step` is explicitly opted into analysis.

### Reproduction

Create these files.

### `package.json`

```json
{
  "name": "fallow-playwright-getter-repro",
  "private": true,
  "devDependencies": {
    "@playwright/test": "^1.60.0",
    "fallow": "^2.92.1",
    "typescript": "^6.0.3"
  },
  "scripts": {
    "dead-code": "fallow dead-code --unused-class-members --format json --quiet"
  }
}
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "experimentalDecorators": true
  }
}
```

### `.fallowrc.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json",
  "entry": [
    "tests/**/*.test.ts",
    "fixture.ts"
  ],
  "rules": {
    "unused-class-members": "error"
  },
  "ignoreDecorators": [
    "@step"
  ]
}
```

### `step.ts`

```ts
export function step(_label: string): MethodDecorator {
  return () => undefined;
}
```

### `message-checks.ts`

```ts
import { step } from "./step";

export class MessageChecks {
  @step("Assert if the sample record matches")
  async hasExpectedRecord(): Promise<void> {
    console.log("expected record");
  }

  @step("Assert if the sample message exists for ID '{{recordId}}'")
  async hasMessageForRecordId(recordId: string): Promise<void> {
    console.log(recordId);
  }
}
```

### `asserter-factory.ts`

```ts
import { MessageChecks } from "./message-checks";

export class AsserterFactory {
  private _messageChecks?: MessageChecks;

  get messageChecks(): MessageChecks {
    this._messageChecks ??= new MessageChecks();
    return this._messageChecks;
  }
}
```

### `fixture.ts`

```ts
import { test as base } from "@playwright/test";
import { MessageChecks } from "./message-checks";
import { AsserterFactory } from "./asserter-factory";

type MyFixtures = {
  app: {
    assert: {
      messageChecks: MessageChecks;
    };
  };
};

export const test = base.extend<MyFixtures>({
  app: async ({}, use) => {
    const asserterFactory = new AsserterFactory();

    await use({
      assert: {
        messageChecks: asserterFactory.messageChecks,
      },
    });
  },
});
```

### `tests/repro.test.ts`

```ts
import { test } from "../fixture";

test("uses nested fixture member", async ({ app }) => {
  await app.assert.messageChecks.hasExpectedRecord();
  await app.assert.messageChecks.hasMessageForRecordId("ID-123");
});
```

## Command

```bash
npm install
npx fallow dead-code --unused-class-members --format json --quiet
```

## Actual behavior

`fallow` reports both methods as `unused-class-members`, with findings shaped like:

```json
{
  "path": "message-checks.ts",
  "parent_name": "MessageChecks",
  "member_name": "hasExpectedRecord",
  "kind": "class_method"
}
```

```json
{
  "path": "message-checks.ts",
  "parent_name": "MessageChecks",
  "member_name": "hasMessageForRecordId",
  "kind": "class_method"
}
```

### Expected behavior

No `unused-class-members` findings for these methods, because they are called from the entry test.

## Why this looks like a bug

`fallow` can see the file and class export as reachable, but the method calls are not credited through this chain:

`getter-created instance -> nested Playwright fixture property -> method call from test`

That suggests a member-crediting gap rather than a config or entry-point issue.

### Fallow version

2.92.1

### Operating system

Windows

### Configuration

```toml
### `.fallowrc.json`


{
  "$schema": "https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json",
  "entry": [
    "tests/**/*.test.ts",
    "fixture.ts"
  ],
  "rules": {
    "unused-class-members": "error"
  },
  "ignoreDecorators": [
    "@step"
  ]
}
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1f2bf7070b2650dd2e613fe0b84df61f7363a741`.  There
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
{"case_id": "fallow_rs_fallow__1190__1f2bf70",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
