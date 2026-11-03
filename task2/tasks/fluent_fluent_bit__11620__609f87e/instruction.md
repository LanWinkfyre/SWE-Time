# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
v5 package available but not release notes

Hi,

This morning I find that v5.0 is available on your Debian repository and it seems to break some things (expected, on a major update), at least the "health" api.

I was searching for release notes, but I couldn't find any : nothing in the [releases](https://github.com/fluent/fluent-bit/releases) section on GitHub, nothing on the [announcements](https://www.fluentbit.io/announcements/) page on the website…

This is confusing, to say the least.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `609f87ea65d6a46389d21be6a9c7a2a1d29f4c77`.  There
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
{"case_id": "fluent_fluent_bit__11620__609f87e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
