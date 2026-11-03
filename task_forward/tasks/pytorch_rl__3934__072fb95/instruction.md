# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Partial pose constraints in the robotics IK / macro-action API (e.g. keep the end-effector level)

## Motivation

The macro-action stack (`RobotMacroAction.reach_pose` + `URScriptPrimitiveTransform` + `CartesianSolver`) currently supports two flavors of Cartesian target:

- **position-only** (quaternion omitted / zero): all 3 rotational DOF are free;
- **full 6D pose** (position + quaternion): all 3 rotational DOF are locked.

Many practical constraints live in between, and today they can't be expressed:

- *"the gripper must stay horizontal / level"* — align one tool axis with a world axis (2 rotational DOF constrained), leave the spin about it free;
- *"hold a rod vertically while translating it"* — same axis-alignment constraint plus a straight-line position path;
- *"keep the camera pointing at the target, roll free"*.

Working on a UR12e task ("translate a vertically held rod along a vertical line, no lateral motion"), the only options were (a) lock the full quaternion — over-constrained, burns all 3 rotational DOF and degrades near singularities, or (b) write a custom `cartesian_solver` closure with a hand-rolled DLS loop and a bespoke error vector. (b) works but everyone reimplements it, and nothing documents that this is the intended extension point.

A second, related gap: constraints only apply to the **endpoint** of a macro action. The expansion interpolates in joint space, so the intermediate waypoints can violate the constraint even when both endpoints satisfy it (we measured several mm of lateral drift mid-macro on a straight-line task; the workaround is chopping the motion into many small macros).

## Solution

1. **Docs first**: document the `CartesianSolver` contract (currently a bare `Callable` alias with no docstring) — signature, expected shapes, batching, and the fact that it is the sanctioned place to implement custom IK behavior. A worked example of a partial-orientation solver would cover most needs even without new primitives.
2. **Partial orientation constraints on `reach_pose`**: e.g. an `orientation_mask` / per-axis weights, or a dedicated `axis_align=(tool_axis, world_axis)` kwarg that constrains 2 rotational DOF and leaves the spin free. Internally this is just row selection / reweighting of the rotation error in the DLS loop.
3. **Path (per-waypoint) constraints**: optionally re-solve IK per interpolation waypoint (`movel`-style linear Cartesian paths) instead of joint-space interpolation between endpoint solutions, so constraints like "stay on the line" and "stay level" hold along the whole macro action, not just at its end.

## Alternatives

- Keep everything in user-space `cartesian_solver` closures (status quo) and only add documentation + an example. Acceptable minimum, but axis-alignment is common enough (level gripper, vertical tool, pouring) that a first-class primitive seems justified.
- Full task-based IK (stacked weighted tasks with nullspace projection, à la pink/mink). Probably overkill for the macro-action API, but worth keeping in mind so the constraint API doesn't paint us into a corner.

## Checklist

- [x] I have checked that there is no similar issue in the repo (required)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `072fb956ae1988bbe49aab5489508bd4f4470c9a`.  There
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
{"case_id": "pytorch_rl__3934__072fb95",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
