# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
security: "use server" modules flagged as server-only-import — every Server Action call site is a false positive

## Summary

`fallow security` treats a `"use server"` directive as equivalent to `server-only` / `next/headers` / `node:fs` for the `server-only-import` rule. These markers mean opposite things, so in any Next.js App Router project that uses Server Actions, every client component that triggers a mutation is reported as `high`.

## What the rule conflates

- `server-only`, `next/headers`, `next/server`, `node:fs`, `node:child_process` — "this must never reach a client bundle". A `"use client"` file importing these is a genuine defect. The rule is correct here.
- `"use server"` — the inverse. It declares a network boundary whose *purpose* is to be imported by client components. The bundler replaces the import with an action reference (id + fetch stub); the function body never enters the client bundle. This has been the framework's recommended mutation pattern since Next 14.

The evidence string enumerates both in one breath:

> This "use client" file transitively imports a SERVER-ONLY module (it carries a "use server" directive **or** imports server-only code such as server-only, next/headers, next/server, or node:fs / node:child_process; …)

## Minimal repro

```
// app/actions/save.ts
"use server";
export async function save(input: unknown) { /* … */ }
```

```tsx
// components/save-button.tsx
"use client";
import { save } from "@/app/actions/save";
export function SaveButton() {
  return <button onClick={() => save({})}>Save</button>;
}
```

`fallow security` reports:

```
[H] high server-only-import  components/save-button.tsx:2
    import trace:
      components/save-button.tsx:2 (client boundary)
      app/actions/save.ts:1            (sink site)
```

The sink site is line 1 — the directive itself. The action module imports no server-only code.

## Impact

Observed on a real Next.js 16 App Router project: **9 of 9** `server-only-import` findings had this exact shape — two hops, sink site at line 1 of a `"use server"` module, and none of those modules imported `server-only`, `next/headers`, `next/server`, `node:fs` or `node:child_process`. That was the entire `high` band of the security surface, and all of it was noise.

Because the surface is opt-in and candidate-based, a 100 % false-positive rate in the top severity band means it gets switched off before the genuinely useful surfaces (`client-server-leak`, `tainted-sink`) are ever looked at.

## Secondary: the suggested false-positive criterion doesn't fit

The remediation hint says:

> If it is pulled in only through `next/dynamic(..., { ssr: false })`, it is the sanctioned client-only escape hatch and is a false positive.

That addresses a different scenario (a client-only-rendered component) and applies to none of these findings. A user following the hint literally would conclude all of them are real.

## Suggested fix

1. Separate the two marker classes. A `"use server"` module reached from a `"use client"` file is a sanctioned boundary, not a leak — either drop it from `server-only-import` or demote it to informational.
2. If a signal at that boundary is still wanted, the valuable question is what *crosses* it, not that it is imported: does the action validate its input, is it authorized, does it return secret-derived data? That would complement `tainted-sink` rather than duplicate a framework convention.

## Environment

- fallow 3.10.0 (darwin-arm64)
- Next.js 16.2.10, React 19.2.4, TypeScript 5
- No `security` block in `.fallowrc.jsonc` (defaults)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `52b30f51ec5639ccbefec3bb9a130f5a8afd436a`.  There
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
{"case_id": "fallow_rs_fallow__2074__52b30f5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
