# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Still not using mirror to download model

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**v4.0.0.0
<!-- Container Image or LocalAI tag/commit -->

**Environment, CPU architecture, OS, and Version:**
<!-- Provide the output from "uname -a", HW specs, if it's a VM  -->
DOCKER
Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz
Linux c3a894cd9475 6.12.33-production+truenas #1 SMP PREEMPT_DYNAMIC Wed Feb 18 21:29:07 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux

**Describe the bug**
<!-- A clear and concise description of what the bug is. -->
Still not using mirror to download model

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->
Download model from mirrors

**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

<img width="934" height="532" alt="Image" src="https://github.com/user-attachments/assets/faa03b3f-c02c-48ed-b6c8-dc552c369b70" />
<img width="2159" height="1161" alt="Image" src="https://github.com/user-attachments/assets/90b4da15-1b7a-4944-ac1f-0b3e2c778a76" />
<img width="2240" height="907" alt="Image" src="https://github.com/user-attachments/assets/b2152d33-7f73-4ce0-925c-040147a293ed" />

**Additional context**
<!-- Add any other context about the problem here. -->
Please add support GH_ENDPOINT environment variable to use github mirror website.
`GH_ENDPOINT = https://ghproxy.it`
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `31fcb1425dcae7abb593f8b38aebf43f5a8a1128`.  There
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
{"case_id": "mudler_LocalAI__9066__31fcb14",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
