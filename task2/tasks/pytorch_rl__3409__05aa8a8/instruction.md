# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Composite tensor spec encode does not set batch size correctly.

## Describe the bug

<!--- A clear and concise description of what the bug is. --->

The `encode` of the tensor spec `Composite` does not set the `batch_size` of the output `TensorDict` to the shape of itself but to an empty size.

## To Reproduce

<!---
Steps to reproduce the behavior.

Please try to provide a minimal example to reproduce the bug. Error messages and stack traces are also helpful.

Please use the markdown code blocks for both code and stack traces.
--->

Tun the following.

```python
import torch
from torchrl.data import Composite, Bounded


def main():
    shape = (2,)
    ts = Composite(
        obs=Bounded(
            torch.zeros(*shape, 3),
            torch.ones(*shape, 3),
        ),
        shape=shape,
    )
    r = ts.rand()
    raw_vals = {"obs": r["obs"].cpu().numpy()}
    encoded_vals = ts.encode(raw_vals)
    print(ts.shape)
    print(r.batch_size)
    print(encoded_vals.batch_size)


if __name__ == "__main__":
    main()
```

The output will be.

```bash
torch.Size([2])
torch.Size([2])
torch.Size([])
```

So the `batch_size` after `encode` is incorrect.

## Expected behavior

<!--- A clear and concise description of what you expected to happen. --->

The `TensorDict` returned from the `encode` should have the same `batch_size` as the shape of the tensor spec.

<!---
## Screenshots

If applicable, add screenshots to help explain your problem.
--->

## System info

Describe the characteristic of your environment:
 * Describe how the library was installed (pip, source, ...)
 * Python version
 * Versions of any other relevant libraries

- Python 3.12.3
- Installed tensordict via pip and torchrl from source

```python
import torchrl, numpy, sys
print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
```
results in
```
0.11.0+gb6e8bbfe 2.4.1 3.12.3 (main, Jan  8 2026, 11:30:50) [GCC 13.3.0] linux
```

<!---
## Additional context

Add any other context about the problem here.

## Reason and Possible fixes

If you know or suspect the reason for this bug, paste the code lines and suggest modifications.
--->

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `05aa8a8029e989a6091ff1b14a60892d194397fb`.  There
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
{"case_id": "pytorch_rl__3409__05aa8a8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
