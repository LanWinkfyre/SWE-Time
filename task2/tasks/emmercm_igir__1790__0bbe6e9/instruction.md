# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
mame2003-plus.xml: 0.0B of 0 games, 0 parents parsed

`npx igir@latest`


```
TRACE: DATScanner: found 1 DAT file
TRACE: DATScanner: enumerating DAT archives
TRACE: DATScanner: parsing 1 DAT file
TRACE: DATScanner: .mame/mame2003-plus.xml: attempting to parse 20.9MiB of XML
TRACE: DATScanner: .mame/mame2003-plus.xml: parsed XML, deserializing to DAT
TRACE: DATScanner: .mame/mame2003-plus.xml: 0.0B of 0 games, 0 parents parsed
```

 - https://github.com/libretro/mame2003-plus-libretro/blob/master/metadata/mame2003-plus.xml
 - https://raw.githubusercontent.com/libretro/mame2003-plus-libretro/refs/heads/master/metadata/mame2003-plus.xml
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0bbe6e92da3e7eb92415061b7b6e22e4d779e3c8`.  There
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
{"case_id": "emmercm_igir__1790__0bbe6e9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
