# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-class-members: member access through private class fields is not credited cross-module

First: thank you for the quick turnaround on #1785 — the fix shipped in the very next release, and the interface-property-hop shape from that report now credits correctly cross-module. Trialing the rule on our codebase at 3.3.0 surfaced two adjacent gaps, so here's one more report with the same probe discipline.

**Gap 1 (the main one):** a **private** class field — either syntax, `#dep` or TS `private dep` — typed by (or assigned from) an imported class, with members reached through `this.#dep.m()` / `this.dep.m()`, is not credited cross-module.

**Gap 2:** the #1785 close comment names "interface and type-literal alias property types" as covered, but at released 3.3.0 only the interface form credits — the same options-hop shape through `type Opts = { c: Dep }` still flags `Dep`'s members (matrix below).

## Reproduction (fallow 3.3.0)

`dep.ts`:

```ts
export class DepHashNew { hashNew(): number { return 1; } }
export class DepPrivParam { privParam(): number { return 2; } }
export class DepPubField { pubField(): number { return 3; } }
```

`index.ts` (package.json `main`):

```ts
import { DepHashNew, DepPrivParam, DepPubField } from "./dep.ts";

class ConsumerHashNew {
  readonly #dep = new DepHashNew();
  run(): number { return this.#dep.hashNew(); }
}
class ConsumerPrivParam {
  constructor(private dep: DepPrivParam) {}
  run(): number { return this.dep.privParam(); }
}
class ConsumerPubField {
  readonly dep = new DepPubField();
  run(): number { return this.dep.pubField(); }
}

console.log(new ConsumerHashNew().run());
console.log(new ConsumerPrivParam(new DepPrivParam()).run());
console.log(new ConsumerPubField().run());
```

`fallow dead-code` reports:

```
● Unused class members (2)
  dep.ts (2)
    :1 DepHashNew.hashNew
    :2 DepPrivParam.privParam
```

`DepPubField.pubField` (public field, same consumption shape) is credited; only the private-field receivers are flagged.

## Boundary as measured

| receiver shape | cross-module credit at 3.3.0 |
|---|---|
| public field (`readonly dep = new Dep()` or ctor-assigned) | ✅ |
| local variable | ✅ |
| interface-property hop (`private opts: Opts` + `this.opts.c.m()`, the #1785 shape) | ✅ |
| type-alias property hop (`type Opts = { c: Dep }`, same consumption) | ❌ (the #1785 close comment names alias property types as covered, but the released 3.3.0 credits only the interface form) |
| `#dep = new Dep()` (inline new) | ❌ |
| `#dep: Dep` + ctor assignment | ❌ |
| `constructor(private dep: Dep)` (param property, class-typed directly) | ❌ |
| `#dep: IDep` (interface-typed field, `implements` on the class) | ❌ |

All shapes credit fine when class and consumer share a file.

## Impact

Private-field DI is the dominant style in our codebase: with the rule enabled, one package produced 42 false positives of exactly this shape against 2 real findings, so `unused-class-members` stays off for us until private-field receivers are credited. (The asymmetry is easy to miss in mixed codebases: members also reached by tests or interface hops earn credit elsewhere, so the FPs concentrate in packages whose classes are consumed only through an orchestrator's private fields.)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8cd68866fadd5c274c7bf261a8fb7c2436622f35`.  There
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
{"case_id": "fallow_rs_fallow__1821__8cd6886",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
