# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
False positives as dead code when vue components exposed as namespaces

### What happened?

The design system exposes compound components as **namespaces**:

```ts
// design-system/index.ts
export * as Card from "./components/Card";
export * as List from "./components/List";
export * as Popover from "./components/Popover";
export * as Tabs from "./components/Tabs";
// ...Collapsible, Dialog, ExpansionPanel, Radio
```

Consumers import the namespace and render members with a dotted tag:

```vue
<script setup lang="ts">
import { List, Popover } from "@/design-system";
</script>
<template>
    <List.Root>
        <List.Item v-for="x in items" :key="x.id">{{ x.name }}</List.Item>
    </List.Root>
    <Popover.Root>
        <Popover.Activator>…</Popover.Activator>
        <Popover.Content>…</Popover.Content>
    </Popover.Root>
</template>
```

fallow's `unrendered-components` policy reports **every** namespace-rendered member as
"reachable but rendered nowhere", even `List.Item` / `List.Root` (rendered in ~27/28
files respectively), `Popover.*` (20 files), `Tabs.*` (9 files). It appears the render-usage
resolver does not follow `<Namespace.Member>` tags back to a `export * as Namespace` +
named-import binding.

### Reproduction

create few vue design system files as namespaces
```ts
// design-system/index.ts
export * as Card from "./components/Card";
export * as List from "./components/List";
export * as Popover from "./components/Popover";
export * as Tabs from "./components/Tabs";
// ...Collapsible, Dialog, ExpansionPanel, Radio
```

Consume them as e.g.
```vue
<script setup lang="ts">
import { List, Popover } from "@/design-system";
</script>
<template>
    <List.Root>
        <List.Item v-for="x in items" :key="x.id">{{ x.name }}</List.Item>
    </List.Root>
    <Popover.Root>
        <Popover.Activator>…</Popover.Activator>
        <Popover.Content>…</Popover.Content>
    </Popover.Root>
</template>
```



### Expected behavior

The components are declared as reachable but unused but they are used in many files

### Fallow version

2.100.0

### Operating system

Linux

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `48cb04fabb7375f32edaff7e635fe45c995076ae`.  There
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
{"case_id": "fallow_rs_fallow__1351__48cb04f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
