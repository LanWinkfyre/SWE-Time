# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
`unused-class-members` false positive through Playwright `mergeTests(...)` and chained `fixture.extend(...)` after `#1190`

### What happened?

`fallow` `2.94.0` still reports used class methods as `unused-class-members` when the call path goes through Playwright fixture wrappers.

Confirmed failing wrapper shapes:

- `mergeTests(testDbDelphidba, testDbIntdba)`
- `testDbDelphidba.extend(...)`

Confirmed working control shape in the same synthetic repro:

- direct `testDbDelphidba` usage without an extra wrapper

This looks like a follow-up to `#1190`, which was fixed in `2.93.0` for the direct fixture case.

This reproduction uses only synthetic identifiers and stubbed logic:

- IDs: `ID-123`, `ID-456`, `ID-789`
- a local no-op `@step` decorator
- no production code, schemas, or real message data

### Reproduction

Create these files.

### `package.json`

```json
{
  "name": "fallow-merge-tests-repro",
  "private": true,
  "devDependencies": {
    "@playwright/test": "^1.60.0",
    "fallow": "^2.94.0",
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
  },
  "include": ["./**/*.ts"]
}
```

### `.fallowrc.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json",
  "entry": ["tests/**/*.test.ts"],
  "rules": {
    "unused-class-members": "error"
  },
  "ignoreDecorators": ["@step"]
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

  @step("Actually unused control method")
  async isActuallyUnused(): Promise<void> {
    console.log("unused");
  }

  @step("Assert if the extended fixture record matches")
  async hasExtendedRecord(): Promise<void> {
    console.log("extended record");
  }

  @step("Assert if the extended fixture message exists for ID '{{recordId}}'")
  async hasExtendedMessageForRecordId(recordId: string): Promise<void> {
    console.log(recordId);
  }

  @step("Actually unused extended control method")
  async isActuallyUnusedExtended(): Promise<void> {
    console.log("unused extended");
  }

  @step("Assert if the direct fixture record matches")
  async hasDirectRecord(): Promise<void> {
    console.log("direct record");
  }

  @step("Assert if the direct fixture message exists for ID '{{recordId}}'")
  async hasDirectMessageForRecordId(recordId: string): Promise<void> {
    console.log(recordId);
  }
}
```

### `checks-factory.ts`

```ts
import { MessageChecks } from "./message-checks";

export class ChecksFactory {
  private _messageChecks?: MessageChecks;

  get messageChecks(): MessageChecks {
    this._messageChecks ??= new MessageChecks();
    return this._messageChecks;
  }
}
```

### `primary-fixture.ts`

```ts
import { test as base } from "@playwright/test";
import { MessageChecks } from "./message-checks";
import { ChecksFactory } from "./checks-factory";

type AppFixtures = {
  app: {
    assert: {
      messageChecks: MessageChecks;
    };
  };
};

export const testPrimary = base.extend<AppFixtures>({
  app: async ({}, use) => {
    const checksFactory = new ChecksFactory();

    await use({
      assert: {
        messageChecks: checksFactory.messageChecks,
      },
    });
  },
});
```

### `secondary-fixture.ts`

```ts
import { test as base } from "@playwright/test";

type SecondaryFixtures = {
  noop: {
    value: string;
  };
};

export const testSecondary = base.extend<SecondaryFixtures>({
  noop: async ({}, use) => {
    await use({ value: "noop" });
  },
});
```

### `merged-fixture.ts`

```ts
import { mergeTests } from "@playwright/test";
import { testPrimary } from "./primary-fixture";
import { testSecondary } from "./secondary-fixture";

export const mergedTest = mergeTests(testPrimary, testSecondary);
```

### `extended-fixture.ts`

```ts
import { testPrimary } from "./primary-fixture";

type ExtendedFixtures = {
  extra: {
    value: string;
  };
};

export const extendedTest = testPrimary.extend<ExtendedFixtures>({
  extra: async ({}, use) => {
    await use({ value: "extended" });
  },
});
```

### `tests/repro.test.ts`

```ts
import { mergedTest } from "../merged-fixture";

mergedTest("uses nested fixture member via mergeTests", async ({ app }) => {
  await app.assert.messageChecks.hasExpectedRecord();
  await app.assert.messageChecks.hasMessageForRecordId("ID-123");
});
```

### `tests/extend-repro.test.ts`

```ts
import { extendedTest } from "../extended-fixture";

extendedTest("uses nested fixture member via extend", async ({ app }) => {
  await app.assert.messageChecks.hasExtendedRecord();
  await app.assert.messageChecks.hasExtendedMessageForRecordId("ID-456");
});
```

### `tests/direct-repro.test.ts`

```ts
import { testPrimary } from "../primary-fixture";

testPrimary("uses nested fixture member directly", async ({ app }) => {
  await app.assert.messageChecks.hasDirectRecord();
  await app.assert.messageChecks.hasDirectMessageForRecordId("ID-789");
});
```

## Command

```bash
npm install
npx fallow dead-code --unused-class-members --format json --quiet
```

## Actual behavior

Validated locally on Windows with `fallow 2.94.0`.

The used methods behind wrapper fixtures are still reported as unused:

```json
[
  {
    "path": "message-checks.ts",
    "parent_name": "MessageChecks",
    "member_name": "hasExpectedRecord"
  },
  {
    "path": "message-checks.ts",
    "parent_name": "MessageChecks",
    "member_name": "hasMessageForRecordId"
  },
  {
    "path": "message-checks.ts",
    "parent_name": "MessageChecks",
    "member_name": "isActuallyUnused"
  },
  {
    "path": "message-checks.ts",
    "parent_name": "MessageChecks",
    "member_name": "hasExtendedRecord"
  },
  {
    "path": "message-checks.ts",
    "parent_name": "MessageChecks",
    "member_name": "hasExtendedMessageForRecordId"
  },
  {
    "path": "message-checks.ts",
    "parent_name": "MessageChecks",
    "member_name": "isActuallyUnusedExtended"
  }
]
```

Notes:

- `hasExpectedRecord` and `hasMessageForRecordId` are used via `mergeTests(...)`, but still report.
- `hasExtendedRecord` and `hasExtendedMessageForRecordId` are used via chained `fixture.extend(...)`, but still report.
- `hasDirectRecord` and `hasDirectMessageForRecordId` are used via the direct `testPrimary` fixture and do **not** report.
- `isActuallyUnused` and `isActuallyUnusedExtended` report as expected.

### Expected behavior

Only genuinely unused methods should report.

Expected findings:

- `MessageChecks.isActuallyUnused`
- `MessageChecks.isActuallyUnusedExtended`

Non-findings:

- `MessageChecks.hasExpectedRecord`
- `MessageChecks.hasMessageForRecordId`
- `MessageChecks.hasExtendedRecord`
- `MessageChecks.hasExtendedMessageForRecordId`
- `MessageChecks.hasDirectRecord`
- `MessageChecks.hasDirectMessageForRecordId`

## Why this looks like a follow-up bug

- `#1190` fixed the direct Playwright fixture case in `2.93.0`.
- The same synthetic repro shows that direct `testPrimary` usage is credited correctly.
- The remaining false positives appear only after adding a wrapper layer:
  - `mergeTests(...)`
  - chained `fixture.extend(...)`
- That makes this look like a remaining correlation gap in wrapper fixture analysis rather than an entry-point or decorator configuration problem.

### Fallow version

2.94.0

### Operating system

Windows

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c187b94f0cddf9ea2e0f77e6a21707001764c434`.  There
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
{"case_id": "fallow_rs_fallow__1210__c187b94",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
