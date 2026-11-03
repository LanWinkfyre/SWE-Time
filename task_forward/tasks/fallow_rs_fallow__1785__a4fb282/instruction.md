# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-class-members: propagate binding-target resolution across module boundaries

## Summary

`unused-class-member` detection credits an impressive range of receiver shapes — but only when the class and its consumer share a file. The moment the same patterns split across modules, every member reports as unused. Codebases that wire classes through constructor-injected options objects (class defined in one module, consumed through a typed property in another) get a near-100% false-positive rate from this rule, with no config remedy short of turning it off.

## Reproduction (fallow 3.2.0)

Same-file — all six receiver shapes are correctly credited:

```ts
// src/index.ts
export class OptDep { optM(): void {} }
interface Opts { c: OptDep }
class UserA { constructor(private opts: Opts) {} run(): void { this.opts.c.optM(); } }
new UserA({ c: new OptDep() }).run();
// … typed params, typed locals, fixture properties, call-result
// receivers, typed class properties: all credited. 0 findings. ✓
```

Cross-file — the identical patterns all flag:

```ts
// src/dep.ts
export class OptDep { optM(): void {} }

// src/user.ts
import type { OptDep } from "./dep.ts";
interface Opts { c: OptDep }
export class UserG { constructor(private opts: Opts) {} run(): void { this.opts.c.optM(); } }

// src/index.ts (entry)
import { OptDep } from "./dep.ts";
import { UserG } from "./user.ts";
new UserG({ c: new OptDep() }).run();
// → unused-class-member: OptDep.optM  ✗ (called on every run)
```

Matrix we measured: 6/6 receiver shapes credited same-file; 4/4 cross-file variants flagged (class-typed options property, interface-typed options property, class-typed store property, fixture-object property).

## Why this looks reachable

The per-file visitor already does the hard part: `resolve_bound_object_name` / `BindingTarget::Class` resolves dotted receivers (`this.opts.c`) to class bindings, and `resolve_structural_class_calls` credits typed-parameter member uses to argument classes. What's missing is only that these binding-target facts don't travel across import edges — while the codebase already has a cross-module fact channel (`SemanticFact` / `SemanticFactView`, used by e.g. the Playwright-fixture and factory-chain facts consumed in `analyze/unused_members.rs`).

A shape that would cover the dominant DI pattern: emit a fact for "class member accessed through a property/parameter whose declared type name is `X`" plus a fact for "class `C` (imported from `m`) flows into a property/argument typed `X`", and join the two at analysis time the way the existing facts join.

## Context

Evaluated on a TypeScript codebase (~32k LOC) with constructor-injected options objects throughout: the rule produced 39 findings, 0 real — ~32 interface/RPC-dispatch cases (handled by the excellent heritage-scoped `usedClassMembers` rules) and 7 cross-module receiver cases with no remedy. We've disabled the rule for now and kept the heritage allowlists ready for a re-enable if cross-module propagation lands.

Happy to provide the full matrix project or test against a branch.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a4fb282920ee12d521d48a2f13be9ad77d3665ef`.  There
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
{"case_id": "fallow_rs_fallow__1785__a4fb282",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
