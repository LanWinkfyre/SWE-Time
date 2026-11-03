# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
dupes: spread-aware ranking, a reviewed-clones ignore list, and near-miss clone detection

The most harmful duplicates are the ones sitting far apart: written similarly, spread across modules or separated by hundreds of lines in a large file. Nearby copies are easy for a human or an agent to spot during review; distant ones survive for years and drift independently. Three connected improvements would make `fallow dupes` rank, triage, and detect exactly those.

## 1. Spread-aware ranking

`DuplicationReport::sort()` orders groups alphabetically by first instance path (crates/types/src/duplicates.rs:140), `--top` re-sorts by instance count then line count, and the human renderer sorts by line count. None of these consider how far apart the copies live, so a 60-line clone duplicated across three packages ranks below a longer one sitting in adjacent files.

All inputs already exist on `CloneInstance` (paths, line ranges). Proposal:

- Per group, compute `spread`: the maximum over instance pairs of directory-tree distance (count of non-shared parent-dir components on both sides); for same-file groups, use the line gap in coarse steps (for example 250 lines per step).
- Rank score: `token_count * instance_count * (1 + log2(1 + min(spread, 8)) / log2(9) * 0.15)`, a capped multiplicative boost so distance amplifies size instead of replacing it.
- Make this the default order for the human report and `--top`, and expose `spread` as a field on `CloneGroupFinding` so agents and CI can re-rank without recomputing path math.

Deterministic, offline, pure path arithmetic.

## 2. Selective reviewed-clones ignore list

The dupes baseline (`--save-baseline`/`--baseline`, crates/engine/src/baseline.rs) is all-or-nothing: it accepts the entire current state. There is no way to say "this one clone group is reviewed and intentional, keep everything else live", which is the natural triage loop for an agent: inspect groups, discard the intentional ones, re-run, refactor what remains.

Proposal:

- A committable ignore list keyed on the existing group fingerprints, either `ignoredClones: ["dup:xxxxxxxx"]` in the config or a dedicated auto-created file with one hash per line, `#` comments, and a self-documenting header.
- Key on the existing `<fingerprint>:<instance_count>` shape so the semantics come for free: a reviewed group resurfaces when the fragment is edited or when a new copy appears, both of which genuinely warrant a re-review.
- One refinement while touching this: derive the fingerprint from the normalized token-hash sequence instead of the raw representative fragment (crates/engine/src/duplication_detector/deepdive.rs), so pure formatting edits do not resurface reviewed groups. The current raw-text hash is formatting-sensitive.

## 3. Near-miss (gapped) clone detection

The suffix-array detector finds contiguous runs of normalization-equal tokens; a two-line edit in the middle of an otherwise copied function splits or kills the match. Semantic mode already handles renamed identifiers and literals, but only for identical token structure. The clones that survive today's detector plus a light edit are invisible.

A deterministic, offline route that reuses existing machinery:

- Function-scoped candidates (boundary spans already exist in the token stream; see detect/boundary.rs).
- Per function, take the semantic-mode hashed token sequence (already computed), build k-token shingles (shingle_filter.rs already implements rolling shingles), and derive a banded MinHash signature; bucket collisions produce candidate pairs in roughly linear time.
- Verify candidates with exact Jaccard over shingle sets (or a token-LCS ratio), cluster via union-find with nesting/overlap exclusion, and reuse `min_tokens` as the size floor.
- Surface as an opt-in mode (for example `--near` or `mode = "near"`) emitting regular `CloneGroup`s with a `similarity` field, so all existing output formats, families, fingerprints, and the ignore list from point 2 apply unchanged.

## Phasing

1 and 2 are small and independently shippable; 3 is a larger detector addition that becomes much more useful once 1 and 2 exist, because near-miss groups need ranking and triage more than exact ones do.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4066db66e0b2251a54a9e4b8441025d2f35374fa`.  There
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
{"case_id": "fallow_rs_fallow__2155__4066db6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
