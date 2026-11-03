# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
migrate: knip's ignore becomes ignorePatterns, which removes files from the module graph

`fallow migrate` maps knip's `ignore` onto `ignorePatterns`, but the two mean different things:

- knip `ignore`: do not report findings in these files. The files stay in the module graph.
- fallow `ignorePatterns`: exclude the files from analysis. They leave the module graph.

A knip config that ignores tests, stories and barrel files is common. Migrating it verbatim removes exactly the modules whose imports prove the rest of the code is reachable, so everything downstream of them is reported as dead.

On a Next.js app with Storybook and Vitest, migrating an existing knip config took the report from 310 findings to 531, and unused files from 19 to 269. Roughly 250 live files became phantom findings. The migration looks successful: it writes a valid config, the warnings list only skipped fields, and nothing indicates the output got worse.

## Suggested fixes

### 1. Report the before/after delta (highest value, most generic)

Have `migrate` run the analysis with and without the generated config and print the difference:

```
Before: 310 findings (19 unused files)
After:  531 findings (269 unused files, +250)

The generated config increases findings. This usually means files were removed
from the module graph rather than silenced. Review ignorePatterns before adopting.
```

Analysis is sub-second, so running it twice is cheap. This catches the whole class of "migrated config breaks the graph" without needing to special-case each source field.

### 2. Translate `ignore` to something faithful

Either introduce a field with knip's semantics (suppress findings, keep in graph), or pattern-match the common cases during migration:

- test and story globs: drop them and note that the vitest and storybook plugins already handle these
- `**/index.ts` style globs: translate to `dynamicallyLoaded` and say why

### 3. Diagnose a broken graph in the report itself

When a file is reported unused and its only importers were excluded by an `ignorePattern`, that is derivable. Surfacing it turns a silent failure into a self-diagnosing one:

```
142 of 269 unused-file findings have importers excluded by ignorePatterns.
Your config may be hiding the graph rather than the noise.
```

### 4. Offer `dynamicallyLoaded` in the `actions` array

For the barrel case, `dynamicallyLoaded` is the correct tool, but the name describes a mechanism (loaded at runtime) rather than the effect (treat as used). Finding it means reading the full config field list.

Unused-file findings currently offer `remove-file` and `suppress-line`. Adding an `add-to-config` action for `dynamicallyLoaded` would surface it at the moment it is needed, matching what unused-dependency findings already do for `ignoreDependencies`.

### 5. Validate carried-over `ignoreDependencies`

Of three entries carried over from knip, two were unnecessary because fallow's own plugins already resolve those packages, and the third was not a false positive at all: the dependency was genuinely unused and should have been removed rather than ignored.

`migrate` could check each entry against a real run:

```
3 ignoreDependencies carried over:
  2 redundant (plugins resolve these): <pkg>, <pkg>
  1 genuinely unused: <pkg>. Consider removing the dependency instead of ignoring it.
```

That turns migration into a cleanup opportunity.

### 6. Drop a redundant `entry`

The migrated `entry` field produced byte-identical output with and without it, because the Next.js plugin already covered those paths. Detecting and dropping a redundant `entry` keeps the config smaller and reduces drift.

## Notes

Related to #457, which covered warnings for silently dropped rule names and unsupported globs. This is about a field that migrates without warning but changes meaning.

Worth saying: the sub-second analysis is what made this diagnosable. It was cheap enough to A/B test config fields one at a time instead of guessing. `--trace` and `--trace-dependency` then settled every individual finding in one command each.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e207ccdcdd2f44b18d28030ef791e70ac5b1588c`.  There
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
{"case_id": "fallow_rs_fallow__1991__e207ccd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
