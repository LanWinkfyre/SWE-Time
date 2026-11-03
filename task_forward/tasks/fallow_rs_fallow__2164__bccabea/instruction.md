# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
`--gate new-only` fails the only safe sequence for a clone-removal refactor

## Summary

A *correct and complete* clone-removal refactor ends with fewer clones than it started
with — but its intermediate steps report **newly introduced** clones, so `--gate new-only`
fails them. In a repo that requires small, reviewable commits, the gate rejects the only
safe way to perform the refactor.

**Version:** fallow 3.14.0
**Command:** `fallow audit --base <sha> --gate new-only`

## Setup

Four sibling scripts. Each carries its own copy of a small comparison helper (`eq()`), plus
a self-test harness and a `fail()` reporter.

Two of the four `eq()` are byte-identical. The other two are **semantically different** —
one sorts both sides before comparing, an order-insensitive contract that would silently
change behaviour if merged with the others.

So the correct refactor is: extract the two identical `eq()` to a shared lib, **leave the
two that differ**, then extract `fail()`, then extract the self-test harness.

## Reproduction

Measured after each step, with `--base` pinned to the pre-refactor commit:

```
step 0   nothing yet                        introduced = 0    pass
step 1   unify the 2 identical eq()         introduced = 2    FAIL   <- the refactor created them
step 2   + extract fail() to the lib        introduced = 1    FAIL
step 3   + extract the self-test harness    introduced = 0    pass
```

## Why step 1 *adds* clones

Removing the duplication **inside** one region made the *surrounding* self-test scaffolding
identical across files — which gave that scaffolding the shape the detector recognizes.

**Deduplicating within a file can create a clone across files.**

The refactor is monotonically correct at every step. The metric is not monotonic along it.
A reviewer looking at step 1 in isolation sees strictly less duplication than at step 0;
the gate sees two new clone groups.

## Impact

Any workflow that gates per-commit or per-PR — rather than on the terminal state of a
branch — cannot land this refactor without either squashing the whole thing into one
unreviewable commit, or disabling the gate for that branch. Both are worse than the
problem the gate exists to prevent.

## Ask

Any one of these would resolve it:

1. Evaluate `new-only` against the **terminal state of a branch** rather than each tip commit.
2. A flag (`--allow-transient`) or a per-group suppression that expires at the end of a refactor.
3. Failing both — document that `new-only` is not safe to gate on mid-refactor, so users
   pick a different gate for those branches. Right now nothing warns you, and the failure
   looks like the refactor was wrong.

## Secondary, smaller

The detector groups by **form**, so N same-named symbols are reported as N copies even when
their contracts differ and merging them would be a behaviour change. That is defensible for
a *detector* — but the *gate* reads "reported" as "should be merged", which pushes users
toward an incorrect merge.

A way to annotate a clone group as **intentionally divergent, with a reason**, would let the
gate stay strict without that pressure. (A plain suppression is not quite the same thing: the
useful property is that the reason is recorded next to the divergence, and that a *new*
member joining the group still fails.)

Thanks for the tool — the detector itself found real duplication in our repo that manual
review had missed. This is only about the gate's behaviour along a refactor.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bccabead68a9e9968f40cedf5aa8314f26389504`.  There
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
{"case_id": "fallow_rs_fallow__2164__bccabea",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
