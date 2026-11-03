# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
security: add literal and constant propagation before sink matching

## Problem

Some security candidates are caused by sink arguments that are statically constant, or derived from non-secret environment metadata rather than a secret-shaped source.

Generic examples:

```ts
const MISSING_LINE_NUMBER_SENTINEL = -1;
sql.raw(String(MISSING_LINE_NUMBER_SENTINEL));
```

```ts
const tagRef = process.env.TAG_REF;
if (!tagRef.startsWith("release-v")) process.exit(1);
console.error(`unexpected TAG_REF: ${tagRef}`);
```

The first example is literal-only SQL. The second example is an environment value, but not secret-shaped and validated against a public release tag format.

## Suggested improvement

Add a small pre-sink value classifier:

- Propagate literal constants through `String(...)`, template literals with only constants, and simple module-local constants.
- Downgrade or omit raw SQL when the argument is fully literal or numeric-constant derived.
- Distinguish secret-shaped environment keys from public CI metadata keys such as tag, branch, ref, SHA, environment, or mode.
- Keep findings when non-literal request/user data reaches the same sinks.

## Expected result

Constant-only sink inputs should not carry the same priority as dynamic attacker-controlled inputs, and env-log findings should focus on secret-shaped values.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9ebddf7856116cc3239d6f79a5b192acc158d447`.  There
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
{"case_id": "fallow_rs_fallow__1138__9ebddf7",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
