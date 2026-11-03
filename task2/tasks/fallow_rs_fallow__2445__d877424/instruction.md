# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Boundary violations exit 0 with --fail-on-issues when rules overrides exist

## What happened?

`fallow dead-code --boundary-violations --fail-on-issues` reports a configured `boundary-violation` with severity `error`, but exits with code 0 as soon as the config contains any per-path `overrides` entry. The override does not need to match either side of the violating import and can target an unrelated rule.

Without the unrelated `overrides` block, the same fixture exits with code 1 as expected.

Observed on Fallow 3.19.0. The same behavior was first observed on 3.14.0.

## Reproduction

Create this tree:

```text
.
├── .fallowrc.jsonc
├── package.json
└── src
    ├── adapter/value.ts
    ├── domain/value.ts
    └── main.ts
```

`package.json`:

```json
{
  "name": "fallow-boundary-override-repro",
  "private": true,
  "type": "module"
}
```

`.fallowrc.jsonc`:

```jsonc
{
  "entry": ["src/main.ts"],
  "rules": { "boundary-violation": "error" },
  "overrides": [
    {
      "files": ["src/other/**"],
      "rules": { "unused-exports": "off" }
    }
  ],
  "boundaries": {
    "zones": [
      { "name": "domain", "patterns": ["src/domain/**"] },
      { "name": "adapter", "patterns": ["src/adapter/**"] }
    ],
    "rules": [
      { "from": "domain", "allow": [] },
      { "from": "adapter", "allow": [] }
    ]
  }
}
```

`src/main.ts`:

```ts
import "./domain/value.ts";
```

`src/domain/value.ts`:

```ts
import { adapterValue } from "../adapter/value.ts";
console.log(adapterValue);
```

`src/adapter/value.ts`:

```ts
export const adapterValue = 1;
```

Run:

```bash
fallow dead-code \
  --boundary-violations \
  --fail-on-issues \
  --no-cache
printf 'exit=%s\n' "$?"
```

Observed output:

```text
● Boundary violations (1)
  src/domain/value.ts:1 → src/adapter/value.ts (domain → adapter)

✗ 1 violation
exit=0
```

Control case: remove only the unrelated `overrides` block and rerun the same command. The finding is unchanged, but the command correctly exits with code 1.

## Expected behavior

A reported `boundary-violation` with `rules."boundary-violation": "error"` should make `--fail-on-issues` exit with code 1, regardless of unrelated per-path overrides. This matches the documented default severity and gating behavior for boundary violations:

https://docs.fallow.tools/explanations/dead-code#boundary-violations

## Fallow version

```text
fallow 3.19.0
```

Also reproduced on 3.14.0.

## Operating system

macOS (Apple Silicon)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d877424ca12c71cb9490bfd1d05be4975285a195`.  There
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
{"case_id": "fallow_rs_fallow__2445__d877424",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
