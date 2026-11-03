# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
audit: new-vs-inherited attribution is not rename-aware, so git mv reports pre-existing findings as introduced

## Summary

`fallow audit`'s new-vs-inherited attribution compares changed files against the base snapshot **by path**, with no rename detection. A `git mv` therefore leaves the relocated file with no counterpart at its new path in the base, and every **pre-existing** complexity/duplication finding on it is reported `introduced: true`.

The practical effect: any PR that relocates files — a route rename, a directory restructure, a refactor — turns `fallow audit` from exit 0 into exit 1 for debt it did not introduce and cannot fix without editing the moved code.

## Repro

A monorepo PR that renamed ~40 Next.js route directories with `git mv`, zero content change (`git diff --shortstat` reports `N files changed, 0 insertions(+), 0 deletions(-)`, every entry `R100`):

```
fallow audit --base "$PR_BASE_SHA"
```

Result — `--gate new-only` (the default):

- `duplication_introduced: 37` of 45 clone groups
- `complexity_introduced: 49` of 80 findings
- `dead_code_introduced: 0` of 5 — **correct**, all 5 attributed as inherited

I reproduced the same shape on a smaller two-directory rename (17 files, `0 insertions(+), 0 deletions(-)`), where the mis-attribution is total:

```json
{ "gate": "new-only",
  "dead_code_introduced": 10, "dead_code_inherited": 0,
  "complexity_introduced": 16, "complexity_inherited": 0,
  "duplication_introduced": 5,  "duplication_inherited": 0 }
```

...and it reduces all the way down to a three-file fixture repo (one function over the CRAP/cognitive thresholds plus one unused export, `git mv src/old src/renamed`, nothing else), which is probably the cheapest test case to add:

```json
{ "complexity_introduced": 1, "complexity_inherited": 0,
  "dead_code_introduced": 1,  "dead_code_inherited": 0 }
```

Version: **2.78.1**. I also read through the 3.11.0 CLI surface and CHANGELOG and could not find anything that addresses this — no `--follow-renames`, no `-M`, no rename flag on `audit`; the newer `--dead-code-baseline` / `--health-baseline` / `--dupes-baseline` knobs are path-keyed too, so they break on a rename in the same way. Please correct me if I missed a flag.

## The asymmetry is probably the useful clue

On the 40-directory PR, `dead_code_introduced` was **correctly 0** while complexity and duplication were both badly wrong. Whatever the dead-code path does to establish "is this finding new?", the complexity and duplication paths appear not to do — that asymmetry inside a single `audit` run looks like the fastest way in.

## Request

Make the attribution pass rename-aware: consume `git diff -M` (or `--find-renames`) rename detection when building the base snapshot, so a finding on a moved file is matched against its **pre-rename** path.

Ideally this is the default (it matches what `git log --follow`, `git blame -C` and every review tool already do), but a `--follow-renames` opt-in flag would be plenty.

Important sub-case, since it's the one that makes this safe rather than just quiet: a file that was **moved and edited** should still be compared against its pre-rename baseline, so debt the changeset genuinely added on a moved file keeps reporting `introduced: true`. Rename-awareness should relocate the baseline, not suppress findings on moved files.

## Workarounds tried, and what we shipped

- **`--gate all`** — makes it worse, not better: it drops the new-vs-inherited split entirely, so the whole inherited backlog blocks the PR.
- **`fallow-ignore-next-line` sweep** — ~86 comments across 22 files would have silenced it, but that permanently marks pre-existing debt as intentional and masks genuine future regressions in exactly the heaviest files. Rejected.
- **Repo-config knobs** — nothing in `fallow.toml` is relevant; `duplicates.mode = "semantic"` is about renamed *variables*, not renamed files.
- **What we actually merged the first time**: a branch-protection ruleset bypass. Not something we want to normalise.

As a mitigation we now build a **synthetic base commit** in CI before invoking `audit`: read the base tree into a temporary index, replay every rename `git diff -M` reports (moving the *base* blob to the *head* path), `commit-tree` it, and pass that sha as `--base`. Pure relocations then diff to zero and drop out of the changed-file set; moved-and-edited files still get compared against their real pre-rename content, so new debt on them still fails the gate. It works, and it's ~100 lines of bash — which is roughly the argument that this belongs upstream, in the attribution pass, where the rename information is already one `git diff -M` away.

Happy to share the script or open a PR if you'd like a starting point.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `676a85502c3e40c8ef660edbe97e011e897a1e9c`.  There
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
{"case_id": "fallow_rs_fallow__2093__676a855",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
