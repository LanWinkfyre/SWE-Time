# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
audit --gate new-only misattributes unchanged high-CRAP functions as introduced when --coverage is supplied

### What happened?

When `--coverage` is passed to `fallow audit`, the internal base-commit re-analysis used for `--gate new-only` attribution does not receive that coverage data. The base commit's health findings are scored from module-graph estimation while the head commit is scored from real Istanbul coverage. For a pre-existing, unmodified high-CRAP function whose real coverage differs meaningfully from its estimated coverage (common for services covered only by an integration suite outside the coverage file — e.g. the testing-trophy pattern), the base-side and head-side CRAP scores diverge enough that the finding fails to pair across the base/head comparison and is reported `introduced: true`, even though the function is byte-identical on both sides.

Practical effect: a PR that edits any part of a file containing such a function gets its audit gate failed for code it never touched. We reproduced this both with a pure line-shift (function pushed down 19 lines by an addition above it) and with no line shift at all (a new function appended at the end of the file flipped an untouched earlier function to `introduced: true`), so it is distinct from the line-number-shift attribution issue fixed around #961 and from the rename-awareness work in #2093/#2104.

Verification that the function is genuinely unchanged: checking out the base commit separately, generating coverage there, and running `fallow health --coverage` on it directly yields the identical CRAP score to the head side (90.0 in our case, cyclomatic 9, coverage 0%) — only `audit`'s attribution differs, because its internal base pass has no coverage input.

### Reproduction

1. A repo with a function whose only tests live outside the suite that produces the coverage file fed to `--coverage` (unit-coverage 0%, but referenced from several modules so the module-graph estimate scores it below threshold).
2. On a branch that does **not** modify that function (touching any other part of the same file suffices — even appending a new function), run:
   `fallow audit --changed-since <base> --coverage coverage/coverage-final.json --format json`
3. The unmodified function is reported with `introduced: true` and a CRAP score well above threshold (exact-0%-coverage scoring).
4. Control: check out `<base>` alone, generate coverage there, run `fallow health --coverage coverage/coverage-final.json` — the same function scores identically, confirming it is unchanged.

No CLI flag or config field routes coverage into the base-commit pass (checked `fallow audit --help`, `fallow audit-cache --help`, `fallow config-schema`).

### Expected behavior

Either (a) an input such as `--base-coverage` so both sides of the attribution are scored consistently, or (b) attribution falling back to identity matching (file + function + category, ignoring the absolute score) when `--coverage` is supplied and no base-side coverage exists.

Workaround we are using: a manually-maintained health baseline generated with `fallow health --coverage ... --baseline-mode identity --save-baseline`, wired via `audit.healthBaseline`. It works, but requires regenerating the baseline on the base branch after merges — a maintenance step the automatic `--gate new-only` attribution otherwise removes.

### Fallow version

3.17.0 (via `npx -y fallow`, Linux x86_64)

### Configuration

Config is `.fallowrc.json` (JSON form): `audit` block wires `healthBaseline` / `deadCodeBaseline` / `dupesBaseline` with gate `new-only`; `ignoreUnresolvedImports` entries for a gitignored generated client. Happy to share the full file or a minimal repro repo on request.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8c092538693f8b442293245fea81db5bd2917c92`.  There
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
{"case_id": "fallow_rs_fallow__2347__8c09253",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
