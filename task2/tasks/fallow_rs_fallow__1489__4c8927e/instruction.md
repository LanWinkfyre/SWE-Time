# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
`unused-store-members`: false positives for members accessed through indirection (inline `useStore().member`, or a store passed as a typed param/prop)

### What happened?

`unused-store-members` only credits a Pinia store member (state / getter / action) when the
member is accessed on a store instance that was **bound to a variable straight from a
`useXStore()` call**. Any indirection between `useXStore()` and the member access loses the
crediting and the member is reported as unused — a false positive. Two indirections trigger it:

1. **Inline access** — `useXStore().member` without binding the return value first.
2. **Store passed as a typed param / prop** — a function receives the store as
   `ReturnType<typeof useXStore>` and accesses `param.member` (or destructures it).

The control case — `const store = useXStore(); store.member` — is credited correctly.

Reproduces on every version from 2.98.0 through the latest 2.102.0. (The related `storeToRefs`
false positive was fixed in 2.98.0; these indirection cases were not.)

### Reproduction

`.fallowrc.json`:

```json
{ "entry": ["src/main.ts"], "rules": { "unused-store-members": "error" } }
```

`src/store.ts`:

```ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const viaBoundConst = () => 1
  const viaInlineCall = () => 2
  const viaTypedParam = () => 3
  const viaParamDestructure = ref(0)
  return { viaBoundConst, viaInlineCall, viaTypedParam, viaParamDestructure }
})
```

`src/consumer.ts`:

```ts
import { useCounterStore } from './store'

type CounterStore = ReturnType<typeof useCounterStore>

export function boundConst() {
  const store = useCounterStore()
  return store.viaBoundConst() // credited correctly
}

// Case 1: inline access on the useStore() return value
export function inlineCall() {
  return useCounterStore().viaInlineCall() // genuine use, reported unused
}

// Case 2: store passed in as a typed param (e.g. an injected store)
export function memberViaTypedParam(props: { store: CounterStore }) {
  return props.store.viaTypedParam() // genuine use, reported unused
}

export function destructureFromTypedParam(props: { store: CounterStore }) {
  const { viaParamDestructure } = props.store // genuine use, reported unused
  return viaParamDestructure.value
}
```

`src/main.ts`:

```ts
import { boundConst, inlineCall, memberViaTypedParam, destructureFromTypedParam } from './consumer'
export { boundConst, inlineCall, memberViaTypedParam, destructureFromTypedParam }
```

Run `fallow dead-code`.

### Actual behavior

```
flagged: ['viaInlineCall', 'viaParamDestructure', 'viaTypedParam']
```

All three are genuinely used; only `viaBoundConst` is correctly not flagged.

### Expected behavior

A store member used anywhere should be credited regardless of how the store instance reaches the
access site — inline on the `useXStore()` return value, or through a variable/parameter typed as
the store.

### Workaround

- Case 1 (inline): bind the store first — `const store = useXStore(); store.member()`, or
  `const { member } = useXStore()`, or `storeToRefs(useXStore())` for state/getters.
- Case 2 (typed param): no clean workaround when the store is intentionally injected as a
  parameter — calling `useXStore()` inside the function instead of receiving it defeats the
  injection. These sites need a suppression.

### Fallow version

Reproduces on 2.98.0 through 2.102.0 (latest at time of filing).

### Operating system

macOS
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4c8927efaf8a3677d36986701e43f4a1ed574758`.  There
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
{"case_id": "fallow_rs_fallow__1489__4c8927e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
