# Recover the symbolic verification state this change produces

A regression report was filed against `dyninst/dyninst`.  The report is quoted verbatim below.

## Report

```
Replace O(n^2) algorithm in Loop::containsAddress with O(nlogn)

**Is your feature request related to a problem? Please describe.**

The `libmpi.so.12.5.0` library from Aurora takes a long time for
hpcstruct and triggers a bad case of insufficient parallelism for
`getLoopTree()`.  Here's a trace of hpcstruct with 20 threads.

<img width="1374" height="892" alt="Image" src="https://github.com/user-attachments/assets/f344127f-86bf-4c90-92b6-8427c3396ac9" />

Hpcstruct analyzes the binary in two phases.  First is
`CodeObject::parse()` which ends at the thin speckled line at about
120 sec.  Then we call `getLoopTree()` for every function.

All the green area (both green and light green) is idleness, either
`__futex_wait` or `__lll_lock_wait`, and there is a LOT of idleness.

**Describe the solution you'd like**

The problem is that although hpcstruct calls `getLoopTree()`
separately for each function from a separate thread, there is one
function that dominates the entire time.

In this case, the bad function is `MPIR_Bcast`, the speckled line at
the top of the trace from 120 sec to 405 sec.  This one function has
8794 separate loops, including 186 top-level loops and ParseAPI
analyzes them all sequentially.

I was thinking that the 186 top-level loops would be a great
opportunity to add parallelism to getLoopTree.  Maybe some kind of
linear strongly connected components variation could split the work
into separate loop trees that could be analyzed independently.

**Additional context**

The `libmpi.so.12.5.0` binary is from Aurora.
Copied to ufront.cs: /home/krentel/Files/libmpi.so.12.5.0
md5: 75f5aecb1e1e4a72df547f10616716b0  libmpi.so.12.5.0

But I analyzed it on gpu.cs at Rice, RHEL 8.x, Intel Xeon with 36 cores,
72 threads, 2.1 GHz and 128 Gig RAM.

Dyninst master as of Mar 3, 2026 (ef72799e5cb2),
Hpctoolkit develop as of Mar 4, 2026 (57b1740fa76e2).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3f69a18f46e4c088f81b9a0bb8ef76d056d8bb98`.  There
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
{"case_id": "dyninst_dyninst__2167__3f69a18",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
