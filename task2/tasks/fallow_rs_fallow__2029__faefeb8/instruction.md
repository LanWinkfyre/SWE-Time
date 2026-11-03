# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Duplication baselines stop matching after unrelated line shifts

### What happened?

A saved duplication baseline stops matching an unchanged clone group when an unrelated comment shifts one instance by one line.

The clone's raw fingerprint remains unchanged, but the saved baseline stores `path:start-end` pairs instead of that fingerprint.

### Reproduction

Create `package.json`:

```json
{"name":"fallow-dupe-baseline-repro","private":true,"type":"module"}
```

Create `src/first.ts` and `src/second.ts` with identical bodies, changing only the exported function name:

```ts
export const firstTotal = (values: readonly number[]): number => {
  const positive = values.filter((value) => value > 0);
  const doubled = positive.map((value) => value * 2);
  const total = doubled.reduce((sum, value) => sum + value, 0);
  const average = doubled.length === 0 ? 0 : total / doubled.length;
  const rounded = Math.round(average * 100) / 100;
  return rounded;
};
```

Save the baseline:

```sh
fallow dupes \
  --mode strict \
  --min-tokens 10 \
  --min-lines 3 \
  --save-baseline baseline.json \
  --no-cache
```

The baseline contains:

```json
{
  "clone_groups": [
    "src/first.ts:1-8|src/second.ts:1-8"
  ]
}
```

Add an unrelated comment before the function in `src/first.ts`, then run:

```sh
fallow dupes \
  --mode strict \
  --min-tokens 10 \
  --min-lines 3 \
  --baseline baseline.json \
  --fail-on-issues \
  --no-cache
```

### Actual behavior

Fallow reports:

```text
Warning: duplication baseline has 1 entries but matched 0 current clone groups.
```

The unchanged clone group is reported again at `src/first.ts:2-9` and `src/second.ts:1-8`.

The raw fingerprint remains `dup:3c774fb7` before and after the line shift.

The command also exits 0, but that standalone exit-code problem was tracked separately in #2009 and is now fixed. It is out of scope here.

### Expected behavior

An unchanged clone group should remain matched when unrelated edits only shift its line numbers.

Using the normalized clone fingerprint in the saved baseline would appear to preserve identity across line shifts. This also matches the location-independent duplication behavior described in #168.

### Version

Fallow 3.9.1 on macOS arm64.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `faefeb835a912403ea84b33187bccdd9b69b35e5`.  There
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
{"case_id": "fallow_rs_fallow__2029__faefeb8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
