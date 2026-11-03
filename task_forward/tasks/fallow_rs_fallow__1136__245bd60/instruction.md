# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
security: reduce false positives for trusted sanitizer flows

## Problem

`fallow security` currently reports some sink candidates where the value is produced by a local trusted sanitizer or renderer helper. These are useful candidates at first, but they create noise once the helper can be proven safe from local source.

Generic examples:

```ts
const escapeHtml = (value: string): string =>
  value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const renderToken = (token: { content: string; color?: string }): string =>
  `<span style="color:${token.color ?? "inherit"}">${escapeHtml(token.content)}</span>`;

node.innerHTML = renderToken(token);
```

```ts
const quoteIdent = (name: string): string => `"${name.replace(/"/g, '""')}"`;
const table = rowFromSqliteMaster.name;
await db.execute(`SELECT count(*) FROM ${quoteIdent(table)}`);
```

## Suggested improvement

Add a small sanitizer summary layer for `security` sinks:

- Treat explicit HTML escaping helpers as trusted for `dangerous-html` when the sink value is entirely derived through that helper.
- Treat identifier-quoting helpers as trusted for SQL identifier positions, while keeping them separate from SQL value escaping.
- Preserve the finding when the sanitizer output is concatenated with unsanitized user-controlled fragments.

## Expected result

These cases should be downgraded or omitted when the trusted helper fully covers the sink input, while still reporting mixed sanitized and unsanitized flows.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `245bd6071b1a3d8ce2f13e93eda7c70cb28590f7`.  There
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
{"case_id": "fallow_rs_fallow__1136__245bd60",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
