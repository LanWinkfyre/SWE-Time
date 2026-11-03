# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] VideoRecorder Crashes When Passing fps

## Describe the bug
Creating an instance of `VideoRecorder` crashes when we pass `fps`.

## To Reproduce
```python
from torchrl.record import VideoRecorder
VideoRecorder(None, None, "", None, fps=1)
```  
```bash
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/mila/b/browna/.conda/envs/maniskill3_env/lib/python3.10/site-packages/torchrl/record/recorder.py", line 127, in __init__
    self.video_kwargs["fps"] = fps
  File "/home/mila/b/browna/.conda/envs/maniskill3_env/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1928, in __getattr__
    raise AttributeError(
AttributeError: 'VideoRecorder' object has no attribute 'video_kwargs'
```
## Expected behavior
No crash  

## System info

Describe the characteristic of your environment:
 * Describe how the library was installed (pip, source, ...) `torchrl==0.7.1`
 * Python version `3.10`

```python
print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
0.7.1 1.26.4 3.10.14 | packaged by conda-forge | (main, Mar 20 2024, 12:45:18) [GCC 12.3.0] linux
```

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6e40548ab16f36f757b5289482a7b4880d2043fe`.  There
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
{"case_id": "pytorch_rl__2826__6e40548",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
