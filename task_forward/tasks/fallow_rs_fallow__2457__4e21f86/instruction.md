# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Coverage geometry is pinned only by hand-written fixtures, and the committed one has drifted

Every geometry assertion in the Istanbul matcher is hand-written JSON in the Rust test module, and the committed fixture has drifted from what the producer emits.

`crates/mcp/src/tools/coverage_fixture.rs` writes a coverage map for a source it also writes. For that source, `istanbul-lib-instrument` 6 emits:

```
fn 0: name=branchy decl=3:9-3:16 loc=3:36-11:1
```

The fixture asserts `loc.start.column: 35` and `loc.end: { line: 11, column: 10 }`. The tests pass either way, which means they are currently insensitive to the fields they exist to pin.

That is the shape of the risk in general. The matcher's core invariant is where each producer anchors a function record, and nothing in CI would notice if a producer moved an anchor in a minor release. During recent matcher work, a hand-written fixture twice asserted geometry no producer emits, and each time the test passed while proving something other than what it claimed.

## What would help

A conformance harness that pins the producers and asserts the anchors, rather than more hand-written maps. The repository already runs producer-conformance harnesses in JavaScript under `scripts/`, so this is an established pattern here rather than a new category of thing.

Worth covering: `istanbul-lib-instrument` (jest, and vitest with the istanbul provider), `ast-v8-to-istanbul` (recent vitest default), `v8-to-istanbul` (c8, nyc), and `oxc-coverage-instrument`.

## What needs deciding

- Does a Rust CI job gain a Node step, or does the harness run on its own schedule?
- Are the maps committed as golden files, or generated at test time from pinned versions?
- What is the policy when a producer legitimately moves an anchor: refresh the golden file, or treat it as a matcher change?

The last one is the real cost of this work: a four-producer matrix with pinned versions is a maintenance surface, not a file. Fixing the drifted fixture above is worth doing either way.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4e21f86a386ceae6a2a9dce0ebdd0607e7c2e33d`.  There
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
{"case_id": "fallow_rs_fallow__2457__4e21f86",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
