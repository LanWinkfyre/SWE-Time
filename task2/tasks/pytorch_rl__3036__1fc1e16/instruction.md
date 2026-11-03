# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] MultistepTransform is returning emtpy slice first valid datapoint

## Describe the bug

When using the MultistepTransform with the ReplayBuffer, the first time the inverse transform emits data (after it's accumulated `n_steps` datapoints) the data has size 0, which causes the lazy storage to be initialized to wrong dimensions so that when data is actually added in the next iteration, there is a mismatch causing an error.

## To Reproduce

Steps to reproduce the behavior.

Please try to provide a minimal example to reproduce the bug. Error messages and stack traces are also helpful.

Please use the markdown code blocks for both code and stack traces.

```python
import torch
from tensordict import TensorDict
from torchrl.data import ReplayBuffer, LazyTensorStorage
from torchrl.data.replay_buffers.samplers import RandomSampler
from torchrl.envs.transforms.rb_transforms import MultiStepTransform

# Configuration
buffer_size = 1000
n_step = 3
gamma = 0.99
device = "cpu"

# Create replay buffer with MultiStepTransform
rb = ReplayBuffer(
    storage=LazyTensorStorage(max_size=buffer_size, device=device, ndim=1),
    sampler=RandomSampler(),
    transform=MultiStepTransform(n_steps=n_step, gamma=gamma),
)

# Create a simple transition
# This mimics what happens in the training loop when processing single environment steps
obs_dict = {"observation": torch.randn(4)}  # 4-dim observation
next_obs_dict = {"observation": torch.randn(4)}



for _ in range(10):

    # Create transition with batch_size=[] (no batch dimension)
    transition = TensorDict(
        {
            "obs": TensorDict(obs_dict, batch_size=[]),
            "action": torch.randn(2),  # 2-dim action
            "next": TensorDict(
                {
                    "obs": TensorDict(next_obs_dict, batch_size=[]),
                    "done": torch.tensor(False, dtype=torch.bool),
                    "reward": torch.tensor(1.0, dtype=torch.float32),
                },
                batch_size=[],
            ),
        },
        batch_size=[],
    ).unsqueeze(0)


    rb.add(transition)
```

```bash
---------------------------------------------------------------------------

RuntimeError                              Traceback (most recent call last)

[/usr/local/lib/python3.11/dist-packages/tensordict/_td.py](https://localhost:8080/#) in __setitem__(self, index, value)
    856                         value = value.copy()
--> 857                         value.batch_size = indexed_bs
    858                     except RuntimeError as err:

8 frames

[/usr/local/lib/python3.11/dist-packages/tensordict/_td.py](https://localhost:8080/#) in batch_size(self, new_size)
   2306     def batch_size(self, new_size: torch.Size) -> None:
-> 2307         self._batch_size_setter(new_size)
   2308 

[/usr/local/lib/python3.11/dist-packages/tensordict/base.py](https://localhost:8080/#) in _batch_size_setter(self, new_batch_size)
   2948                     )
-> 2949         self._check_new_batch_size(new_batch_size)
   2950         has_names = self._has_names()

/usr/local/lib/python3.11/dist-packages/tensordict/base.py in _check_new_batch_size(self, new_size)
  11408             ):
> 11409                 raise RuntimeError(
  11410                     f"the {type(tensor).__name__} {key} has shape {_shape(tensor)} which "

RuntimeError: the TensorDict obs has shape torch.Size([1]) which is incompatible with the batch-size torch.Size([0]).


The above exception was the direct cause of the following exception:

RuntimeError                              Traceback (most recent call last)

[/tmp/ipython-input-4-2145852631.py](https://localhost:8080/#) in <cell line: 0>()
     45 
     46 
---> 47     rb.add(transition)

[/usr/local/lib/python3.11/dist-packages/torchrl/data/replay_buffers/replay_buffers.py](https://localhost:8080/#) in add(self, data)
    690         if data is None:
    691             return torch.zeros((0, self._storage.ndim), dtype=torch.long)
--> 692         return self._add(data)
    693 
    694     def _add(self, data):

[/usr/local/lib/python3.11/dist-packages/torchrl/data/replay_buffers/replay_buffers.py](https://localhost:8080/#) in _add(self, data)
    694     def _add(self, data):
    695         with self._replay_lock, self._write_lock:
--> 696             index = self._writer.add(data)
    697             self._sampler.add(index)
    698         return index

[/usr/local/lib/python3.11/dist-packages/torchrl/data/replay_buffers/writers.py](https://localhost:8080/#) in add(self, data)
    175         # Replicate index requires the shape of the storage to be known
    176         # Other than that, a "flat" (1d) index is ok to write the data
--> 177         self._storage.set(_cursor, data)
    178         index = self._replicate_index(index)
    179         for ent in self._storage._attached_entities_iter():

[/usr/local/lib/python3.11/dist-packages/torchrl/data/replay_buffers/storages.py](https://localhost:8080/#) in set(self, cursor, data, set_cursor)
    834                 self._init(data)
    835         if is_tensor_collection(data):
--> 836             self._storage[cursor] = data
    837         else:
    838             self._set_tree_map(cursor, data, self._storage)

[/usr/local/lib/python3.11/dist-packages/tensordict/_td.py](https://localhost:8080/#) in __setitem__(self, index, value)
    857                         value.batch_size = indexed_bs
    858                     except RuntimeError as err:
--> 859                         raise RuntimeError(
    860                             f"indexed destination TensorDict batch size is {indexed_bs} "
    861                             f"(batch_size = {self.batch_size}, index={index}), "

RuntimeError: indexed destination TensorDict batch size is torch.Size([0]) (batch_size = torch.Size([1000, 0]), index=1), which differs from the source batch size torch.Size([1])
```

## Expected behavior

As far as I can understand, I'm expecting this code to run without crashing and where the resulting transitions will have the reward, done, and next obs gotten from `n_steps` into the future.



## System info

Describe the characteristic of your environment:
 * Installed with pip
 * Python 3.10.15


```python
import torchrl, numpy, sys
print(torchrl.__version__, numpy.__version__, sys.version, sys.platform)
```

## Additional context

Add any other context about the problem here.

## Reason and Possible fixes
Right now, my current understanding is that things go wrong in this piece of code here:

```python
    def _inv_call(self, tensordict: TensorDictBase) -> TensorDictBase:
        if not self._validated:
            self._validate()

        total_cat = self._append_tensordict(tensordict)
        if total_cat.shape[-1] >= self.n_steps:
            out = _multi_step_func(
                total_cat,
                done_key=self.done_key,
                done_keys=self.done_keys,
                reward_keys=self.reward_keys,
                mask_key=self.mask_key,
                n_steps=self.n_steps,
                gamma=self.gamma,
            )
            return out[..., : -self.n_steps]  # <-- this will contain nothing the first iteration
```

In short, when you get `total_cat.shape[-1] >= self.n_steps` the first time, then `len(out[..., : -self.n_steps]) == 0`, which causes the issue. The code seems to run fine if I change `return out[..., : -self.n_steps]` to `return out[..., -self.n_steps]`, to just get the latest timestep that's accumulated enough future timesteps. However, there's a good chance that this is based on a flawed understanding.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1fc1e1634d0ec9b8ea89ebe293672e7494863600`.  There
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
{"case_id": "pytorch_rl__3036__1fc1e16",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
