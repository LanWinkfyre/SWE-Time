# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Standalone dupes command skips the configured duplication threshold

### What happened?

`fallow dupes` exits 0 even when its reported duplication percentage exceeds both the CLI threshold and the resolved config threshold.

### Reproduction

Create `package.json`:

```json
{"name":"fallow-dupes-repro","private":true,"type":"module"}
```

Create `src/first.ts` and `src/second.ts` with the same body, only renaming the exported function:

```ts
export const firstTotal = (values: readonly number[]): number => {
  const positive = values.filter((value) => value > 0);
  const doubled = positive.map((value) => value * 2);
  const total = doubled.reduce((sum, value) => sum + value, 0);
  const average = doubled.length === 0 ? 0 : total / doubled.length;
  return Math.round(average * 100) / 100;
};
```

Run:

```sh
fallow dupes --mode strict --min-tokens 10 --min-lines 3 --threshold 1 --fail-on-issues --format json --quiet --no-cache
printf 'exit=%s\n' "$?"
```

### Actual behavior

The JSON reports one clone group and `stats.duplication_percentage: 100.0`, but the command exits 0 and emits no threshold diagnostic.

The same failure occurs when `threshold: 1` is read from `.fallowrc.json`; `fallow config` correctly reports the resolved threshold as `1.0`.

### Expected behavior

The command exits 1 and reports that 100% exceeds the configured 1% threshold.

### Likely cause

On current main, `run_dupes` calls `print_dupes_result_with_grouping`, which returns the renderer exit code without applying `exceeds_threshold`. The threshold gate still exists in `print_dupes_result`, but standalone `dupes` no longer calls that path. This appears to date to the grouping refactor in `c7bcdd3e51`.

### Version

Fallow 3.9.1. Also reproduced from current main at `45f1642a21b049771ecf54fb92133dda4ce0c1fe`.

### Operating system

macOS 26.5.2, arm64.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e0ae72ba0344f3ab2cf9daa555463f5229672ca7`.  There
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
{"case_id": "fallow_rs_fallow__2009__e0ae72b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
