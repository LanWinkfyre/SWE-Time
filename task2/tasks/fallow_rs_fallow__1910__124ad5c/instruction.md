# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
False positive: `unused-class-members` for a derived client method referenced through a generic base-class property

### What happened?

`fallow dead-code` reports a class method as unused even though it is referenced and executed.

The false positive appears when:

1. A service base class stores a client in a property typed as a generic parameter, for example `TClient extends BaseClient`.
2. A derived service specializes that generic to a concrete derived client.
3. The derived service calls a method that exists only on the derived client through `this.client.someMethod()`.

In that pattern, `fallow` reports the derived client method as an unused class member.

`fallow dead-code` reports the derived client method as unused:

```text
── Unused Code ─────────────────────────────────────

● Unused class members (2)
  src\base-client.ts
    :2 BaseClient.inheritedMethod
  src\derived-client.ts
    :4 DerivedClient.getSyntheticRecords
```

`DerivedClient.getSyntheticRecords` is a false positive here. It is called from `DerivedService.fetchSyntheticRecords()`.

### Reproduction

## Minimal reproduction

This reproduction uses only synthetic names and data.

### `package.json`

```json
{
  "name": "fallow-unused-class-member-repro",
  "private": true,
  "type": "commonjs",
  "devDependencies": {
    "fallow": "^3.6.0",
    "typescript": "^7.0.2"
  }
}
```

### `.fallowrc.json`

```json
{
  "$schema": "./node_modules/fallow/schema.json",
  "entry": ["src/main.ts", "src/main-direct.ts"],
  "rules": {
    "unused-class-members": "error",
    "unused-files": "off",
    "unused-types": "off",
    "unused-exports": "off",
    "unused-dependencies": "off",
    "unused-dev-dependencies": "off",
    "unresolved-imports": "off"
  }
}
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2019",
    "module": "commonjs",
    "strict": true,
    "noEmit": true
  },
  "include": ["src/**/*.ts"]
}
```

### `src/base-client.ts`

```ts
export abstract class BaseClient {
  async inheritedMethod(): Promise<string> {
    return "base";
  }
}
```

### `src/derived-client.ts`

```ts
import { BaseClient } from "./base-client";

export class DerivedClient extends BaseClient {
  async getSyntheticRecords(): Promise<string> {
    return "ok";
  }
}
```

### `src/base-service.ts`

```ts
import { BaseClient } from "./base-client";

export abstract class BaseService<TClient extends BaseClient> {
  protected readonly client: TClient;

  constructor(client: TClient) {
    this.client = client;
  }
}
```

### `src/derived-service.ts`

```ts
import { BaseService } from "./base-service";
import { DerivedClient } from "./derived-client";

export class DerivedService extends BaseService<DerivedClient> {
  async fetchSyntheticRecords(): Promise<string> {
    return await this.client.getSyntheticRecords();
  }
}
```

### `src/main.ts`

```ts
import { DerivedClient } from "./derived-client";
import { DerivedService } from "./derived-service";

async function main(): Promise<void> {
  const service = new DerivedService(new DerivedClient());
  console.log(await service.fetchSyntheticRecords());
}

void main();
```

## Control case

I added a nearly identical non-generic version as a control. This one is not reported by `fallow`, which suggests the problem is specifically tied to the generic base-class property.

### `src/derived-client-direct.ts`

```ts
export class DerivedClientDirect {
  async getSyntheticRecordsDirect(): Promise<string> {
    return "ok";
  }
}
```

### `src/direct-service.ts`

```ts
import { DerivedClientDirect } from "./derived-client-direct";

export class DirectService {
  private readonly client: DerivedClientDirect;

  constructor(client: DerivedClientDirect) {
    this.client = client;
  }

  async fetchSyntheticRecordsDirect(): Promise<string> {
    return await this.client.getSyntheticRecordsDirect();
  }
}
```

### `src/main-direct.ts`

```ts
import { DerivedClientDirect } from "./derived-client-direct";
import { DirectService } from "./direct-service";

async function mainDirect(): Promise<void> {
  const service = new DirectService(new DerivedClientDirect());
  console.log(await service.fetchSyntheticRecordsDirect());
}

void mainDirect();
```

With both entry points present, `fallow` reports only the generic-path method as unused.

## Reproduction steps

```bash
npm install
npx fallow dead-code
```

## Why this looks like a bug

The call is statically visible:

```ts
return await this.client.getSyntheticRecords();
```

At that point, `this.client` is the `client` property from:

```ts
export abstract class BaseService<TClient extends BaseClient> {
  protected readonly client: TClient;
}
```

and `DerivedService` concretizes `TClient` as `DerivedClient`:

```ts
export class DerivedService extends BaseService<DerivedClient> {
```

So `getSyntheticRecords()` appears reachable through the generic specialization, but it is still counted as unused.

## Real-world pattern that triggered this report

The same shape exists in a larger TypeScript codebase where:

- a base service stores `protected readonly client: TClient`
- a derived service extends that base with a concrete client type
- the derived service calls a derived-client-only method through `this.client`

That real-world call is also reported as an unused class member even though it is used.

### Expected behavior

`DerivedClient.getSyntheticRecords` should not be reported, because it is referenced from reachable entry-point code.

### Fallow version

3.6.0

### Operating system

Windows

### Configuration

```toml
{
  "$schema": "./node_modules/fallow/schema.json",
  "entry": ["src/main.ts", "src/main-direct.ts"],
  "rules": {
    "unused-class-members": "error",
    "unused-files": "off",
    "unused-types": "off",
    "unused-exports": "off",
    "unused-dependencies": "off",
    "unused-dev-dependencies": "off",
    "unresolved-imports": "off"
  }
}
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `124ad5cc84484f890cfd728240d6688d3b68df4d`.  There
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
{"case_id": "fallow_rs_fallow__1910__124ad5c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
