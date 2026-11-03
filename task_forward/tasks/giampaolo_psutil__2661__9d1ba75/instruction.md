# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[macOS] CI build segfaults

This is an old problem, which I never managed to solve. Often times, macOS builds segfault for no apparent reason. 

```
2025-10-24T19:47:36.2288240Z   
2025-10-24T19:47:36.2288340Z     warn(stderr)
2025-10-24T19:47:36.2288420Z 
2025-10-24T19:47:36.2288730Z -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2025-10-24T19:47:36.2289060Z ================ 376 passed, 318 skipped, 5 warnings in 24.69s =================
2025-10-24T19:47:36.3336590Z /Users/runner/work/_temp/dd665b0d-2f1e-4bbe-9da3-789bc1952906.sh: line 1:  4599 Segmentation fault: 11  "/Users/runner/work/_temp/cibw/bin/cibuildwheel" "." --output-dir "wheelhouse" 2>&1
2025-10-24T19:47:36.3350410Z ##[error]Process completed with exit code 139.
2025-10-24T19:47:36.3460480Z Post job cleanup.
2025-10-24T19:47:36.3525150Z Post job cleanup.
2025-10-24T19:47:36.8476810Z [command]/opt/homebrew/bin/git version
2025-10-24T19:47:36.8723010Z git version 2.50.1
2025-10-24T19:47:36.8740870Z Copying '/Users/runner/.gitconfig' to '/Users/runner/work/_temp/ff7a4887-d387-40bd-819f-b10a715a5894/.gitconfig'
2025-10-24T19:47:36.8747860Z Temporarily overriding HOME='/Users/runner/work/_temp/ff7a4887-d387-40bd-819f-b10a715a5894' before making global git config changes
2025-10-24T19:47:36.8748580Z Adding repository directory to the temporary git global config as a safe directory
2025-10-24T19:47:36.8750580Z [command]/opt/homebrew/bin/git config --global --add safe.directory /Users/runner/work/psutil/psutil
2025-10-24T19:47:36.8846710Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp core\.sshCommand
2025-10-24T19:47:36.9160700Z [command]/opt/homebrew/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2025-10-24T19:47:37.1356390Z [command]/opt/homebrew/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2025-10-24T19:47:37.1404050Z http.https://github.com/.extraheader
2025-10-24T19:47:37.1409410Z [command]/opt/homebrew/bin/git config --local --unset-all http.https://github.com/.extraheader
2025-10-24T19:47:37.1635030Z [command]/opt/homebrew/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2025-10-24T19:47:37.3066270Z Cleaning up orphan processes
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9d1ba7529f68275697d5bcd1b0785ebd02743683`.  There
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
{"case_id": "giampaolo_psutil__2661__9d1ba75",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
