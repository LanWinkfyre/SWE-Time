# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
unused-class-member false positive: Vue v-for over a member-expression source (props.items / store.items)

Follow-up to #1707 / #1710. The iteration-binding element-type crediting from #1710 covers a `v-for` whose source is a bare module-scope identifier, but NOT a member-expression source such as `props.items` or `store.items`. Member accesses on the loop item still false-report as `unused-class-member`.

### Reproduction

`src/utils/Util.ts`:
```ts
export class Util {
  public property = 42
  public get getter() { return 'x' }
  public hello() { console.log('h') }
}
```

`src/App.vue`:
```vue
<script setup lang="ts">
import { Util } from './utils/Util'
const props = defineProps<{ items: Util[] }>()
</script>

<template>
  <template v-for="(util, i) of props.items" :key="i">
    {{ util.getter }} {{ util.property }} {{ util.hello() }}
  </template>
</template>
```

`getter` / `property` / `hello` are reported as `unused-class-member` even though they are accessed via the loop item.

### Root cause

The Vue v-for element-type resolution (`sfc_template/vue.rs::v_for_element_binding`) looks the source expression up in `iterable_types`, which is keyed by simple binding name (`array_binding_element_types`). A member-expression source (`props.items`) is not a simple binding, so no element class is found and the item is left untyped.

### Suggested approach

Record array-element types for props fields (from the `defineProps<{ items: Util[] }>()` interface) as `props.<field> -> ElementClass`, and extend the v-for source matching to accept `props.<field>` (and likely `<ref>.value` / `store.<field>`) member-expression sources. Reuse `infer_array_binding_element_type` for the field type. Over-credit-only, same posture as #1710.

Refs #1707, #1710.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8ce42a141d471908771f79ae43471fb7494a375e`.  There
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
{"case_id": "fallow_rs_fallow__1711__8ce42a1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
