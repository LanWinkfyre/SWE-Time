# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
review --brief: scoped package names render as empty strings in "new third-party dependencies"

**Version:** fallow 3.22.0 (linux-arm64-gnu)

In the closing summary line of `review --brief`, every package whose name starts with `@` prints as an empty string. Unscoped names print fine.

## Repro

A fresh repo, four files:

```bash
mkdir repro && cd repro && mkdir src && git init
echo '{ "name": "repro", "private": true, "type": "module" }' > package.json
echo "export const hi = (): string => 'hi'" > src/index.ts
git add -A && git commit -m base

cat > package.json <<'JSON'
{
  "name": "repro", "private": true, "type": "module",
  "dependencies": {
    "@scope/one": "^1.0.0", "@scope/two": "^1.0.0",
    "plain": "^1.0.0", "other": "^1.0.0"
  }
}
JSON
printf "import '@scope/one'\nimport '@scope/two'\nimport 'plain'\nimport 'other'\n\nexport const hi = (): string => 'hi'\n" > src/index.ts

fallow review --brief --base HEAD
```

**Observed:**

```
new third-party dependencies: , , other, plain
```

**Expected:**

```
new third-party dependencies: @scope/one, @scope/two, other, plain
```

## Only that line is affected

The `Decisions to make` block right above prints them correctly:

```
adds 4 third-party dependencies (`@scope/one`, `@scope/two`, `other`, `plain`)
```

and `--format json` carries `deltas.dependency_added` in full:

```json
["package.json::@scope/one", "package.json::@scope/two", "package.json::other", "package.json::plain"]
```

`--format github-summary` does not emit the line at all, so CI output is unaffected.

## Guess at the cause

Unverified, since the binary is precompiled: the line looks like it strips a version suffix with something like `name.split('@').next()`, which yields `""` for a scoped name because those begin with `@`. Splitting on the last `@`, or only past index 0, would fix it.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3f062cf9f5b08c2747aff0bd73f4a3c458e0bb98`.  There
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
{"case_id": "fallow_rs_fallow__2553__3f062cf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
