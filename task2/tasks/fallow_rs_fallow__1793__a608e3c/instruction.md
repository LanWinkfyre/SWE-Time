# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
False positive: `unused-class-members` reports methods used from an entry script

### What happened?

`fallow dead-code` reports these methods as unused even though they are called from an entry file that is explicitly listed in the fallow config:

- `SyntheticSchemaWriter.resetSchema`
- `SyntheticSchemaWriter.writeGraphDiagram`
- `SyntheticSchemaWriter.writeSchemaTyped`

### Reproduction

## Actual behavior

The following methods are reported as unused even though the entry script calls them:

- `resetSchema`
- `writeGraphDiagram`
- `writeSchemaTyped`

## Synthetic repro

### `.fallowrc.json`

```json
{
	"$schema": "https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json",
	"entry": [
		"main.ts"
	],
	"rules": {
		"unused-class-members": "error",
		"unused-files": "off",
		"unused-types": "off",
		"unused-exports": "off",
		"unused-dependencies": "off",
		"unused-dev-dependencies": "off",
		"unresolved-imports": "off",
		"unlisted-dependencies": "off",
		"unused-enum-members": "off"
	}
}
```

### `service.ts`

```ts
export type ExportFlavor = "Golden" | "Typed";

export class SyntheticSchemaService {
	constructor(private readonly _name: string) {}

	async initialize(): Promise<void> {
		if (!this._name) {
			throw new Error("Missing name");
		}
	}

	async resetSchema(_exportFlavor: ExportFlavor): Promise<void> {
		return Promise.resolve();
	}

	async writeSchemaData(_exportFlavor: ExportFlavor): Promise<void> {
		return Promise.resolve();
	}

	async writeGraphDiagram(): Promise<void> {
		return Promise.resolve();
	}

	async createTypedSchema(): Promise<string> {
		return Promise.resolve("export type SyntheticRow = { id: string };");
	}
}
```

### `schema-writer.ts`

```ts
import fs from "node:fs";

import { ExportFlavor, SyntheticSchemaService } from "./service";

export class SyntheticSchemaWriter {
	constructor(private readonly _schemaService: SyntheticSchemaService) {}

	async resetSchema(exportFlavor: ExportFlavor): Promise<void> {
		if (exportFlavor === "Golden") {
			await this._schemaService.initialize();
		}
		await this._schemaService.resetSchema(exportFlavor);
	}

	async writeSchemaData(exportFlavor: ExportFlavor): Promise<void> {
		if (exportFlavor === "Golden") {
			await this._schemaService.initialize();
		}
		await this._schemaService.writeSchemaData(exportFlavor);
	}

	async writeGraphDiagram(): Promise<void> {
		await this._schemaService.initialize();
		await this._schemaService.writeGraphDiagram();
	}

	async writeSchemaTyped(): Promise<void> {
		await this._schemaService.initialize();
		const typeDeclarations = await this._schemaService.createTypedSchema();
		await fs.promises.writeFile("./synthetic-typed-schema.ts", typeDeclarations, { encoding: "utf-8" });
	}
}
```

### `main.ts`

```ts
import { SyntheticSchemaService } from "./service";
import { SyntheticSchemaWriter } from "./schema-writer";

type CreatedDb = {
	name: string;
	writer: SyntheticSchemaWriter;
	close: () => Promise<void>;
};

enum WriteMode {
	Golden = "golden",
	Typed = "typed",
}

if (require.main === module) {
	const args = process.argv.slice(2);

	if (args.length === 0) {
		console.error("WriteMode is required. Use golden or typed.");
		process.exit(1);
	}

	const arg = args[0].toLowerCase();
	const mode = Object.values(WriteMode).find((x) => x === arg);

	if (mode) {
		generate(mode).catch((error) => {
			console.error("Synthetic script failed:", error);
			process.exit(1);
		});
	} else {
		console.error(`Invalid mode: ${args[0]}`);
		process.exit(1);
	}
}

async function generate(mode: WriteMode): Promise<void> {
	const createdDbs = await Promise.all(["alpha", "beta"].map(async (schemaName) => createDb(schemaName)));

	if (mode === WriteMode.Golden) {
		await resetSchemas(createdDbs);
	}

	await Promise.all(
		createdDbs.map(async (createdDb) => {
			try {
				if (mode === WriteMode.Golden) {
					await createdDb.writer.writeSchemaData("Golden");
					await createdDb.writer.writeGraphDiagram();
				} else {
					await createdDb.writer.writeSchemaTyped();
				}
			} finally {
				await createdDb.close();
			}
		}),
	);
}

async function createDb(name: string): Promise<CreatedDb> {
	const service = new SyntheticSchemaService(name);
	const writer = new SyntheticSchemaWriter(service);

	return {
		name,
		writer,
		close: async () => Promise.resolve(),
	};
}

async function resetSchemas(createdDbs: CreatedDb[]): Promise<void> {
	for (const createdDb of createdDbs) {
		await createdDb.writer.resetSchema("Golden");
	}
}
```

## Reproduction steps

1. Create the three files above plus the `.fallowrc.json` file in an empty folder.
2. Run:

   ```powershell
   npx fallow dead-code --format json
   ```

3. Observe that fallow reports all 4 `SyntheticSchemaWriter` methods as unused, even though `main.ts` calls them through the configured entry flow.

## What this shows

This repro demonstrates a missed reachability edge in a small, synthetic call graph that mirrors the real `scripts/generate-schema.ts` pattern:

- entry script guarded by `require.main === module`
- argument parsing
- `Promise.all([...].map(async ...))`
- object creation and method calls through the created object
- conditional branch selection for which methods are called

Because the repro uses only synthetic data and no project-specific fixtures, it should be straightforward to validate in the fallow repository itself.

### Expected behavior

Methods that are called from a configured entry script should not be reported as `unused-class-members`.

### Fallow version

3.2.0

### Operating system

Windows

### Configuration

```toml
{
	"$schema": "https://raw.githubusercontent.com/fallow-rs/fallow/main/schema.json",
	"entry": [
		"main.ts"
	],
	"rules": {
		"unused-class-members": "error",
		"unused-files": "off",
		"unused-types": "off",
		"unused-exports": "off",
		"unused-dependencies": "off",
		"unused-dev-dependencies": "off",
		"unresolved-imports": "off",
		"unlisted-dependencies": "off",
		"unused-enum-members": "off"
	}
}
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a608e3c28c54d92fc1f7907b7d98b61ee5f18f67`.  There
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
{"case_id": "fallow_rs_fallow__1793__a608e3c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
