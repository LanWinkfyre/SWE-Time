# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
[Windows] Fluent-Bit service got exception code 0xc0000005 for v5.0.6

## Bug Report

**Describe the bug**
Windows: Windows Server 2019 Standand (v1809)
Fluent-Bit Version: v5.0.6

**To Reproduce**
We installed fluent-bit MSI and then use sc.exe to create windows service. After that, fluent-bit service could keep running about 30 seconds, then it will be terminated unexpectedly. Checking with windows event viewer logs, it shows the exception code 0xc0000005.

Windows event viewer shows: 

<img width="2030" height="1137" alt="Image" src="https://github.com/user-attachments/assets/fdda8d9a-14f7-4651-89e6-20ae9deb7f98" />

Fluent-Bit debug logs:

<img width="2322" height="1437" alt="Image" src="https://github.com/user-attachments/assets/fb69b09e-5b09-493c-b2c4-9ea8a477bf5e" />

**Expected behavior**

Using same config and same windows host, v5.0.3 works well as expected that does not met above issue.

**Configurations**

<img width="1174" height="1338" alt="Image" src="https://github.com/user-attachments/assets/8691f64c-5df4-4ec4-8c10-6352590a3884" />

<img width="1028" height="1345" alt="Image" src="https://github.com/user-attachments/assets/08c76ec9-401a-4cdc-98bf-852ed975ce72" />


**Additional context**
Based on exception code 0xc0000005, after google, maybe it is related with the compatibility of windows DLL(Dynamic Link Library), then I find the PR of #11727.
As we could not get MSI file of v5.0.4 and v5.0.5, therefore I could not make sure which PR introduced this issue.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f6126ebc3aba26882e8e1f2c20e93f04f6d7489c`.  There
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
{"case_id": "fluent_fluent_bit__11842__f6126eb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
