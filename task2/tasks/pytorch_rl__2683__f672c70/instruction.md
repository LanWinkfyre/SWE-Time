# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] max_alpha only works in DiscreteSACLoss if min_alpha is provided as well

## Describe the bug

 The keyword argument `max_alpha` for the loss module `DiscreteSACLoss` only gets used if one also provides `min_alpha`. 

## To Reproduce

```python
"""
An example of using DiscreteSACLoss with a max_alpha parameter that does not get used.
"""

import torch
from torch import nn
from torchrl.collectors import SyncDataCollector
from torchrl.envs import GymEnv
from torchrl.envs.transforms import DTypeCastTransform, TransformedEnv
from torchrl.modules.distributions import OneHotCategorical
from torchrl.modules.tensordict_module.actors import (ProbabilisticActor,
                                                      ValueOperator)
from torchrl.modules.tensordict_module.common import SafeModule
from torchrl.objectives import DiscreteSACLoss, SoftUpdate


def main():
    device = torch.device("cpu")

    env = GymEnv("FrozenLake-v1")
    env = TransformedEnv(
        env,
        DTypeCastTransform(dtype_in=torch.int64, dtype_out=torch.float32, in_keys=["observation"]),
    )

    n_states = 16
    n_actions = 4 # Categorical
    actor_module = nn.Sequential(
        nn.Linear(n_states, 128),
        nn.ReLU(),
        nn.Linear(128, n_actions)
    ).to(device)
    actor_module = SafeModule(actor_module, in_keys=["observation"], out_keys=["logits"])

    actor_network = ProbabilisticActor(
        module=actor_module,
        in_keys=["logits"],
        out_keys=["action"],
        spec=env.action_spec,
        distribution_class=OneHotCategorical
    )

    qvalue_module = nn.Sequential(
        nn.Linear(n_states, 128),
        nn.ReLU(),
        nn.Linear(128, n_actions)
    ).to(device)

    qvalue_network = ValueOperator(
        module=qvalue_module,
        in_keys=["observation"],
        out_keys=["action_value"]
    )

    loss_module = DiscreteSACLoss(
        actor_network=actor_network,
        qvalue_network=qvalue_network,
        num_actions=n_actions,
        alpha_init=0.5,
        max_alpha=0.6,
    )
    loss_keys = ["loss_actor", "loss_alpha", "loss_qvalue"]

    update_eps = 0.99
    target_net = SoftUpdate(loss_module, eps=update_eps)

    lr = 1e-3
    optim = torch.optim.Adam(loss_module.parameters(), lr)

    batch_size = 20
    n_batches = 1000
    total_frames = n_batches * batch_size
    collector = SyncDataCollector(
        env,
        actor_network,
        frames_per_batch=batch_size,
        total_frames=total_frames,
        split_trajs=False,
        device=device,
    )

    for td in collector:
        loss_vals = loss_module(td.to(device))
        loss = 0
        for loss_key in loss_keys:
            loss += loss_vals[loss_key]
        loss.backward()

        print("Alpha: ", loss_vals["alpha"].item())

        optim.step()
        optim.zero_grad()

        # Update target network
        target_net.step()

if __name__ == "__main__":
    main()

```

```bash
Traceback (most recent call last):
  File ... 
```

## Expected behavior

`alpha` to get capped at 0.6, even if `min_alpha` is not provided.

## Screenshots

![image](https://github.com/user-attachments/assets/8c6284d0-48af-4a93-ac2a-7a632682a08a)

## System info

```
mamba create -n torchrl-bugs python=3.12
pip install torchrl
pip install gym
```

`mamba list` results in
```
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                 conda_forge    conda-forge
_openmp_mutex             4.5                       2_gnu    conda-forge
asttokens                 3.0.0              pyhd8ed1ab_1    conda-forge
bzip2                     1.0.8                h4bc722e_7    conda-forge
ca-certificates           2024.12.14           hbcca054_0    conda-forge
cloudpickle               3.1.0                    pypi_0    pypi
decorator                 5.1.1              pyhd8ed1ab_1    conda-forge
exceptiongroup            1.2.2              pyhd8ed1ab_1    conda-forge
executing                 2.1.0              pyhd8ed1ab_1    conda-forge
farama-notifications      0.0.4                    pypi_0    pypi
filelock                  3.16.1                   pypi_0    pypi
fsspec                    2024.12.0                pypi_0    pypi
gym                       0.26.2                   pypi_0    pypi
gym-notices               0.0.8                    pypi_0    pypi
ipython                   8.31.0             pyh707e725_0    conda-forge
jedi                      0.19.2             pyhd8ed1ab_1    conda-forge
jinja2                    3.1.5                    pypi_0    pypi
ld_impl_linux-64          2.43                 h712a8e2_2    conda-forge
libexpat                  2.6.4                h5888daf_0    conda-forge
libffi                    3.4.2                h7f98852_5    conda-forge
libgcc                    14.2.0               h77fa898_1    conda-forge
libgcc-ng                 14.2.0               h69a702a_1    conda-forge
libgomp                   14.2.0               h77fa898_1    conda-forge
liblzma                   5.6.3                hb9d3cd8_1    conda-forge
libnsl                    2.0.1                hd590300_0    conda-forge
libsqlite                 3.47.2               hee588c1_0    conda-forge
libuuid                   2.38.1               h0b41bf4_0    conda-forge
libxcrypt                 4.4.36               hd590300_1    conda-forge
libzlib                   1.3.1                hb9d3cd8_2    conda-forge
markupsafe                3.0.2                    pypi_0    pypi
matplotlib-inline         0.1.7              pyhd8ed1ab_1    conda-forge
mpmath                    1.3.0                    pypi_0    pypi
ncurses                   6.5                  he02047a_1    conda-forge
networkx                  3.4.2                    pypi_0    pypi
numpy                     2.2.1                    pypi_0    pypi
nvidia-cublas-cu12        12.4.5.8                 pypi_0    pypi
nvidia-cuda-cupti-cu12    12.4.127                 pypi_0    pypi
nvidia-cuda-nvrtc-cu12    12.4.127                 pypi_0    pypi
nvidia-cuda-runtime-cu12  12.4.127                 pypi_0    pypi
nvidia-cudnn-cu12         9.1.0.70                 pypi_0    pypi
nvidia-cufft-cu12         11.2.1.3                 pypi_0    pypi
nvidia-curand-cu12        10.3.5.147               pypi_0    pypi
nvidia-cusolver-cu12      11.6.1.9                 pypi_0    pypi
nvidia-cusparse-cu12      12.3.1.170               pypi_0    pypi
nvidia-nccl-cu12          2.21.5                   pypi_0    pypi
nvidia-nvjitlink-cu12     12.4.127                 pypi_0    pypi
nvidia-nvtx-cu12          12.4.127                 pypi_0    pypi
openssl                   3.4.0                h7b32b05_1    conda-forge
orjson                    3.10.14                  pypi_0    pypi
packaging                 24.2                     pypi_0    pypi
parso                     0.8.4              pyhd8ed1ab_1    conda-forge
pexpect                   4.9.0              pyhd8ed1ab_1    conda-forge
pickleshare               0.7.5           pyhd8ed1ab_1004    conda-forge
pip                       24.3.1             pyh8b19718_2    conda-forge
prompt-toolkit            3.0.48             pyha770c72_1    conda-forge
ptyprocess                0.7.0              pyhd8ed1ab_1    conda-forge
pure_eval                 0.2.3              pyhd8ed1ab_1    conda-forge
pygments                  2.19.1             pyhd8ed1ab_0    conda-forge
python                    3.12.8          h9e4cc4f_1_cpython    conda-forge
readline                  8.2                  h8228510_1    conda-forge
setuptools                75.6.0             pyhff2d567_1    conda-forge
stack_data                0.6.3              pyhd8ed1ab_1    conda-forge
sympy                     1.13.1                   pypi_0    pypi
tensordict                0.6.2                    pypi_0    pypi
tk                        8.6.13          noxft_h4845f30_101    conda-forge
torch                     2.5.1                    pypi_0    pypi
torchrl                   0.6.0                    pypi_0    pypi
traitlets                 5.14.3             pyhd8ed1ab_1    conda-forge
triton                    3.1.0                    pypi_0    pypi
typing_extensions         4.12.2             pyha770c72_1    conda-forge
tzdata                    2024b                hc8b5060_0    conda-forge
wcwidth                   0.2.13             pyhd8ed1ab_1    conda-forge
wheel                     0.45.1             pyhd8ed1ab_1    conda-forge
```

## Additional context

Add any other context about the problem here.

## Reason and Possible fixes

This is probably due to the if statement in the method
```python
def _alpha(self):
        if self.min_log_alpha is not None:
            self.log_alpha.data = self.log_alpha.data.clamp(
                self.min_log_alpha, self.max_log_alpha
            )
        with torch.no_grad():
            alpha = self.log_alpha.exp()
        return alpha
```
in the class `DiscreteSACLoss`.

## Checklist

- [X] I have checked that there is no similar issue in the repo (**required**)
- [X] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [X] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f672c708f964bc33d2518eef3238d826916982f3`.  There
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
{"case_id": "pytorch_rl__2683__f672c70",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
