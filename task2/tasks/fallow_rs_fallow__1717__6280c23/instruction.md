# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-class-member false positive: Angular @for / *ngFor in an external templateUrl

Follow-up to #1712, which covered inline `template:` decorators. An Angular `@for` / `*ngFor` loop variable over a component field typed as an array of a class does NOT credit member accesses on the loop item when the template lives in an external `templateUrl` file, so the class members false-report as `unused-class-member`. The inline `template:` form is covered by #1712.

### Reproduction

`src/utils/Util.ts`:
```ts
export class Util {
  public get getter() { return 'x' }
  public hello() { console.log('h') }
}
```

`src/app.component.ts`:
```ts
import { Component } from '@angular/core'
import { Util } from './utils/Util'

@Component({ selector: 'app-root', templateUrl: './app.component.html' })
export class AppComponent {
  utils: Util[] = [new Util()]
}
```

`src/app.component.html`:
```html
@for (util of utils; track util) { <p>{{ util.getter }} {{ util.hello() }}</p> }
```

`getter` / `hello` report as `unused-class-member`.

### Root cause

#1712 types an `@for` / `*ngFor` loop variable to a component-field array's element class inside `record_angular_inline_template`, which has the owning class (and thus its field types) in scope. External `.html` templates are parsed in isolation by `html.rs` at extract time and have no access to the owning component's field types, so the loop variable stays untyped.

### Suggested approach

Either (a) emit a loop-var -> iterable semantic fact from the HTML scanner plus an analyze-time bridge that resolves the iterable against the component's `array_binding_element_types` field map, or (b) a two-phase re-scan that pairs each `templateUrl` `.html` with its component's field types. Over-credit only, same posture as #1712.

Refs #1707, #1710, #1712.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6280c23c3709f69691ebdaef9172c81a4883bdef`.  There
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
{"case_id": "fallow_rs_fallow__1717__6280c23",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
