# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
filename placeholder support

**Is your feature request related to a problem? Please describe.**
I am replacing fluentd with fluentbit.but when output is file.the file name can not be set dependng on some label,record fields,time

path /path/to/${tag}/${key1}/file.%Y%m%d

https://docs.fluentd.org/output/file#path

**Describe the solution you'd like**
I expect that fluent-bit can also support it like fluentd.



**Describe alternatives you've considered**
<!--- A clear and concise description of any alternative solutions or features you've considered. -->
no

**Additional context**
td-agent 4.5.2 fluentd 1.16.3 (d3cf2e0f95a0ad88b9897197db6c5152310f114f)
Fluent Bit v5.0.9
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a1d6fb1ba85e84f160c3fcc948aff26157e3a6dc`.  There
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
{"case_id": "fluent_fluent_bit__12233__a1d6fb1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
