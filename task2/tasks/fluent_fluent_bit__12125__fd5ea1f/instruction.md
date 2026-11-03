# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
mp: flb_mp_chunk_cobj_record_next recurses per non-matching record under conditional processors

### Bug Report

**Describe the bug**

`flb_mp_chunk_cobj_record_next()` in `src/flb_mp.c` advances past records that do not match a processor `condition` by calling **itself recursively**:

```c
if (ret == FLB_FALSE) {
    /* Record doesn't match the condition, continue to next record */
    return flb_mp_chunk_cobj_record_next(chunk_cobj, out_record);
}
```

There are three such self-calls (one per branch). Because a new stack frame is pushed for every non-matching record, the recursion depth grows **proportionally to the number of consecutive non-matching records** in a chunk.

When a condition filters out a large run of records — a common case for a selective `condition` on a processor — the depth can reach tens of thousands of frames for a single chunk and **exhaust the stack, crashing the process**. The compiler is not guaranteed to apply tail-call optimization (especially in debug/unoptimized builds), so this is a real risk, not just theoretical.

Note: the recursion does terminate — this is not an infinite loop — so the defect is the unbounded recursion **depth**, not non-termination.

**Affected path**

Reachable whenever a processor has a `condition` configured and a chunk contains a long run of records that do not match it.

**Expected behavior**

Skipping non-matching records should use constant stack space regardless of how many records are skipped.

**Proposed fix**

Convert the tail recursion into an explicit loop (behavior-preserving). PR incoming.

**Your Environment**

- Version used: current `master`
- Component: `mp` / conditional processors
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fd5ea1f0d5038a12f36421151299e0376e3d650c`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fluent_fluent_bit__12125__fd5ea1f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
