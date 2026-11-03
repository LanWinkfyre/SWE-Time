# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] Download of categorical data in MinariExperienceReplay is completely broken

## Describe the bug

When downloading datasets from Minari that have categorical data (like missions), the download of the dataset is broken, as every step in the dataset will get assigned the array of categorical values for the first episode.

This error originates from treating the Minari categorical data as NonTensorData instead of NonTensorStack.

## To Reproduce

Take this code, for example:

```python
from torchrl.data.datasets.minari_data import MinariExperienceReplay

BATCH_SIZE = 1      # Small batch size to minimize processing
SAVE_ROOT = None    # Set to your desired save location, or None for default


def download_minari_datasets(dataset_id):
    a = MinariExperienceReplay(
        dataset_id=dataset_id,
        batch_size=BATCH_SIZE,
        root=SAVE_ROOT,
    )
    print(f"✓ Successfully downloaded {dataset_id}")


if __name__ == "__main__":
    download_minari_datasets("minigrid/BabyAI-Pickup/optimal-v0")

```
And now watch very closely what happens when we ask for mission values across random steps in random episodes:

```python
In [3]: a[0][('observation', 'mission')][:5], len(a[0][('observation', 'mission')])
Out[3]: 
(array([b'pick up a blue box', b'pick up a blue box',
        b'pick up a blue box', b'pick up a blue box',
        b'pick up a blue box'], dtype=object),
 109)

In [4]: a[200][('observation', 'mission')][:5], len(a[0][('observation', 'mission')])
Out[4]: 
(array([b'pick up a blue box', b'pick up a blue box',
        b'pick up a blue box', b'pick up a blue box',
        b'pick up a blue box'], dtype=object),
 109)

In [5]: a[5000][('observation', 'mission')][:5], len(a[0][('observation', 'mission')])
Out[5]: 
(array([b'pick up a blue box', b'pick up a blue box',
        b'pick up a blue box', b'pick up a blue box',
        b'pick up a blue box'], dtype=object),
 109)
```
It is the same array copied over and over again!

## Expected behavior

Minari datasets that have missions clearly need this dataset to be able to function. And the dataset clearly is intended to be used in a stacked manner.

## Additional context

I opened one PR and one issue in pytorch/tensordict incorrectly handling this issue:
https://github.com/pytorch/tensordict/issues/1399
https://github.com/pytorch/tensordict/pull/1400

In [this comment](https://github.com/pytorch/tensordict/issues/1399#issuecomment-3131769835), @vmoens pointed me to the correct way of dealing with this issue, which is to use the set_list_to_stack function.

## Reason and Possible fixes

I have manually corrected this in the MinariExperienceReplay. I will attach the PR as soon as I can

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c5ca88e53874d812fc8b8163550a82ab94709882`.  There
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
{"case_id": "pytorch_rl__3105__c5ca88e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
