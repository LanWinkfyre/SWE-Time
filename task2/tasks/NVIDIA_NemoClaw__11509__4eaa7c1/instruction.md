# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[DGX Spark][Docs] Hindsight plugin verification command raises AttributeError after successful installation

Build Information:

- Product: NemoClaw v0.0.120
- Component: NemoHermes documentation
- Platform: DGX Spark (Linux, ARM64)
- Documentation page: Install Hermes Plugins
- Package: hindsight-client 0.6.1

Description:

The documented post-installation verification command accesses `hindsight_client.__version__`. The installed `hindsight-client` package does not expose that module attribute, so the command fails even though the package imports successfully.

Steps to Reproduce:

1. Follow the Install Hermes Plugins documentation to configure a NemoHermes sandbox and install `hindsight-client`.
2. Run the documented verification command:

   `nemohermes SANDBOX_NAME exec -- python -c 'import os, sys; sys.path.insert(0, os.environ["HERMES_LAZY_INSTALL_TARGET"]); import hindsight_client; print(hindsight_client.__version__)'`

Expected Result:

The command exits successfully and prints the installed `hindsight-client` version.

Actual Result:

The command exits with status 1:

`AttributeError: module hindsight_client has no attribute __version__`

The package version can instead be obtained with Python package metadata, for example:

`from importlib.metadata import version; print(version("hindsight-client"))`

Reproducibility:

- Reproduced: 1/1 on DGX Spark with NemoClaw v0.0.120
- Other platforms: Not tested
- Regression status: Unknown; earlier releases were not tested

Impact:

Users following the documentation receive a false failure after installation and may incorrectly conclude that the Hindsight plugin installation is broken.

OpenShell Issue:

No. The failure is in the documented Python verification expression.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4eaa7c1c222acd38868cdfe8703884b3e99ab10e`.  There
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
{"case_id": "NVIDIA_NemoClaw__11509__4eaa7c1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
