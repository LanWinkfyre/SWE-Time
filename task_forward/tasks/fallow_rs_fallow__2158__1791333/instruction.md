# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
health: Svelte {:then} reports as complexity kind `if`, needs an Await/Then kind

Follow-up to #2150 / #2152, raised during review of that PR.

## What happens

The template complexity breakdown shipped in #2152 attributes each decision point to a `ComplexityContributionKind`. Svelte's `{#await}` block continuations map onto the closest existing kinds:

- `{:catch ...}` maps to `Catch`, which reads correctly.
- `{:then ...}` maps to `If`, because no `Await`/`Then` variant exists.

So a reader hovering a `{:then}` line in the VS Code breakdown sees the increment labelled "if", which does not match the source in front of them. The number is right; only the label is misleading.

`crates/extract/src/template_complexity/svelte.rs`, in the `"then" | "catch"` arm of `scan_block_continuation`.

## Why it is its own issue

Fixing it properly means adding a variant to `ComplexityContributionKind`, which is a public output-contract type: it appears in the health JSON breakdown, the generated TypeScript contract, and the VS Code extension's rendering. That is a schema addition with its own regeneration and compatibility checks, so it did not belong in the fix PR.

## Shape of the change

- Add an `Await` (or `Then`) variant to `ComplexityContributionKind`.
- Map `{:then}` to it, and consider whether `{#await}` itself should use it instead of `If`.
- Regenerate the contract surfaces and check the extension renders the new kind sensibly rather than falling through to a default.
- Consumers switching exhaustively on the kind need to handle the new variant, so treat it as an additive contract change and confirm the backwards-compatibility policy for this enum.

## Not urgent

Mislabelled, not miscounted. Totals and weights are correct today.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1791333192526e898de933a5245ba9dcfd22d48e`.  There
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
{"case_id": "fallow_rs_fallow__2158__1791333",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
