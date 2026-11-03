# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] MultiAgentNetBase agent dim parameter doesn't change which dimension agents are applied

## Describe the bug

In the MultiAgentNetBase class, there's this agent_dim parameter, which I took to be the axis of the input that the agents are parallelizing over. Changing it, however, doesn't seem to do anything.

## To Reproduce

```
# -*- coding: utf-8 -*-
import torch
from torch import nn
from tensordict import TensorDict
from tensordict.nn import TensorDictModule
from torchrl.modules.models.multiagent import MultiAgentNetBase
from torchrl.modules import ProbabilisticActor
from torchrl.modules.distributions import TanhNormal
from tensordict.nn.distributions import NormalParamExtractor

# Hyperparameters
num_envs = 4
n_agents = 3
obs_dim = 5
seq_len = 6
action_dim = 2

# Action bounds (needed by TanhNormal)
action_low = -1.0
action_high = 1.0

class SingleAgentMLP(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 64),
            nn.Tanh(),
            nn.Linear(64, out_dim),
        )

    def forward(self, x):
        return self.net(x)

class MultiAgentPolicyNet(MultiAgentNetBase):
    def __init__(
        self,
        obs_dim,
        action_dim,
        n_agents,
        share_params=True,
        device=None,
    ):
        self.obs_dim = obs_dim
        self.action_dim = action_dim

        super().__init__(
            n_agents=n_agents,
            centralized=False,
            share_params=share_params,
            agent_dim=1,  # (..., agents, features)
            device=device,
        )

    def _build_single_net(self, *, device, **kwargs):
        # Output 2 * action_dim: loc + scale
        net = SingleAgentMLP(self.obs_dim, 2 * self.action_dim)
        return net.to(device) if device is not None else net

    def _pre_forward_check(self, inputs):
        # inputs: (B, A, obs_dim)
        return inputs

policy_net = MultiAgentPolicyNet(
    obs_dim=obs_dim,
    action_dim=action_dim,
    n_agents=n_agents,
    share_params=True,
)

policy_module = TensorDictModule(
    module= nn.Sequential(policy_net,NormalParamExtractor()),
    in_keys=[("agents", "observation")],
    out_keys=[("agents", "loc"), ("agents", "scale")],
)



actor = ProbabilisticActor(
    module=policy_module,
    in_keys=[("agents", "loc"), ("agents", "scale")],
    out_keys=[("agents", "action")],
    distribution_class=TanhNormal,
    distribution_kwargs={
        "low": action_low,
        "high": action_high,
    },
    return_log_prob=True,
)

td = TensorDict(
    {
        ("agents", "observation"): torch.randn(
            num_envs, n_agents, seq_len, obs_dim
        )
    },
    batch_size=[num_envs],
)

td_out = actor(td)

print("Keys in output TensorDict:")
for k in td_out.keys(True):
    print(" ", k)

print("\nShapes:")
print("observation:", td_out["agents", "observation"].shape)
print("action:", td_out["agents", "action"].shape)
print("log_prob:", td_out["agents", "action_log_prob"].shape)

```

```bash
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
RuntimeError: TensorDictModule failed with operation
    Sequential(
      (0): MultiAgentPolicyNet(
          SingleAgentMLP(
            (net): Sequential(
              (0): Linear(in_features=5, out_features=64, bias=True)
              (1): Tanh()
              (2): Linear(in_features=64, out_features=4, bias=True)
            )
          ),
          n_agents=3,
          share_params=True,
          centralized=False,
          agent_dim=1)
      (1): NormalParamExtractor(
        (scale_mapping): biased_softplus()
      )
    )
    in_keys=[('agents', 'observation')]
    out_keys=[('agents', 'loc'), ('agents', 'scale')].

The above exception was the direct cause of the following exception:

ValueError                                Traceback (most recent call last)
File e:\ai_assist\market_analysis\multi_agent_example_1.py:115
    101 td = TensorDict(
    102     {
    103         ("agents", "observation"): torch.randn(
   (...)    107     batch_size=[num_envs],
    108 )
    110 # td = TensorDict({f"agent_{i}":{"observation": torch.randn(num_envs, 
    111 #                                                           seq_len, 
    112 #                                                           obs_dim)} 
    113 #                  for i in range(n_agents)})
--> 115 td_out = actor(td)
    117 print("Keys in output TensorDict:")
    118 for k in td_out.keys(True):

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1751, in Module._wrapped_call_impl(self, *args, **kwargs)
   1749     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1750 else:
-> 1751     return self._call_impl(*args, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1762, in Module._call_impl(self, *args, **kwargs)
   1757 # If we don't have any hooks, we want to skip the rest of the logic in
   1758 # this function, and just call forward.
   1759 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1760         or _global_backward_pre_hooks or _global_backward_hooks
   1761         or _global_forward_hooks or _global_forward_pre_hooks):
-> 1762     return forward_call(*args, **kwargs)
   1764 result = None
   1765 called_always_called_hooks = set()

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\common.py:328, in dispatch.__call__.<locals>.wrapper(*args, **kwargs)
    325     return out[0] if len(out) == 1 else out
    327 if _self is not None:
--> 328     return func(_self, tensordict, *args, **kwargs)
    329 return func(tensordict, *args, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\utils.py:372, in _set_skip_existing_None.__call__.<locals>.wrapper(_self, tensordict, *args, **kwargs)
    370 self.prev = _skip_existing.get_mode()
    371 try:
--> 372     result = func(_self, tensordict, *args, **kwargs)
    373 finally:
    374     _skip_existing.set_mode(self.prev)

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\probabilistic.py:1364, in ProbabilisticTensorDictSequential.forward(self, tensordict, tensordict_out, **kwargs)
   1360             raise RuntimeError(
   1361                 f"Failed while executing module '{module_num_or_key}'. Scroll up for more info."
   1362             ) from e
   1363 else:
-> 1364     tensordict_exec = self.get_dist_params(tensordict_exec, **kwargs)
   1365     tensordict_exec = self._last_module(
   1366         tensordict_exec, _requires_sample=self._requires_sample
   1367     )
   1369 if self.inplace is True:

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\probabilistic.py:1116, in ProbabilisticTensorDictSequential.get_dist_params(self, tensordict, tensordict_out, **kwargs)
   1114         raise ValueError("Could not find a default interaction in the modules.")
   1115 with set_interaction_type(type):
-> 1116     return tds(tensordict, tensordict_out, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1751, in Module._wrapped_call_impl(self, *args, **kwargs)
   1749     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1750 else:
-> 1751     return self._call_impl(*args, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1762, in Module._call_impl(self, *args, **kwargs)
   1757 # If we don't have any hooks, we want to skip the rest of the logic in
   1758 # this function, and just call forward.
   1759 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1760         or _global_backward_pre_hooks or _global_backward_hooks
   1761         or _global_forward_hooks or _global_forward_pre_hooks):
-> 1762     return forward_call(*args, **kwargs)
   1764 result = None
   1765 called_always_called_hooks = set()

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\common.py:328, in dispatch.__call__.<locals>.wrapper(*args, **kwargs)
    325     return out[0] if len(out) == 1 else out
    327 if _self is not None:
--> 328     return func(_self, tensordict, *args, **kwargs)
    329 return func(tensordict, *args, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\utils.py:372, in _set_skip_existing_None.__call__.<locals>.wrapper(_self, tensordict, *args, **kwargs)
    370 self.prev = _skip_existing.get_mode()
    371 try:
--> 372     result = func(_self, tensordict, *args, **kwargs)
    373 finally:
    374     _skip_existing.set_mode(self.prev)

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\sequence.py:633, in TensorDictSequential.forward(self, tensordict, tensordict_out, **kwargs)
    631 for module in self._module_iter():
    632     try:
--> 633         tensordict_exec = self._run_module(
    634             module, tensordict_exec, **kwargs
    635         )
    636     except Exception as e:
    637         if _has_py311_or_greater:

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\sequence.py:579, in TensorDictSequential._run_module(self, module, tensordict, **kwargs)
    570 def _run_module(
    571     self,
    572     module: TensorDictModuleBase,
    573     tensordict: TensorDictBase,
    574     **kwargs: Any,
    575 ) -> Any:
    576     if not self.partial_tolerant or all(
    577         key in tensordict.keys(include_nested=True) for key in module.in_keys
    578     ):
--> 579         tensordict = module(tensordict, **kwargs)
    580     elif self.partial_tolerant and isinstance(tensordict, LazyStackedTensorDict):
    581         for sub_td in tensordict.tensordicts:

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1751, in Module._wrapped_call_impl(self, *args, **kwargs)
   1749     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1750 else:
-> 1751     return self._call_impl(*args, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1762, in Module._call_impl(self, *args, **kwargs)
   1757 # If we don't have any hooks, we want to skip the rest of the logic in
   1758 # this function, and just call forward.
   1759 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1760         or _global_backward_pre_hooks or _global_backward_hooks
   1761         or _global_forward_hooks or _global_forward_pre_hooks):
-> 1762     return forward_call(*args, **kwargs)
   1764 result = None
   1765 called_always_called_hooks = set()

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\common.py:328, in dispatch.__call__.<locals>.wrapper(*args, **kwargs)
    325     return out[0] if len(out) == 1 else out
    327 if _self is not None:
--> 328     return func(_self, tensordict, *args, **kwargs)
    329 return func(tensordict, *args, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\utils.py:372, in _set_skip_existing_None.__call__.<locals>.wrapper(_self, tensordict, *args, **kwargs)
    370 self.prev = _skip_existing.get_mode()
    371 try:
--> 372     result = func(_self, tensordict, *args, **kwargs)
    373 finally:
    374     _skip_existing.set_mode(self.prev)

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\common.py:1218, in TensorDictModule.forward(self, tensordict, tensordict_out, *args, **kwargs)
   1216 in_keys = indent(f"in_keys={self.in_keys}", 4 * " ")
   1217 out_keys = indent(f"out_keys={self.out_keys}", 4 * " ")
-> 1218 raise err from RuntimeError(
   1219     f"TensorDictModule failed with operation\n{module}\n{in_keys}\n{out_keys}."
   1220 )

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\common.py:1190, in TensorDictModule.forward(self, tensordict, tensordict_out, *args, **kwargs)
   1184         raise KeyError(
   1185             "Some tensors that are necessary for the module call may "
   1186             "not have not been found in the input tensordict: "
   1187             f"the following inputs are None: {none_set}."
   1188         ) from err
   1189     else:
-> 1190         raise err
   1191 if isinstance(tensors_out, (dict, TensorDictBase)) and all(
   1192     key in tensors_out for key in self.out_keys
   1193 ):
   1194     if isinstance(tensors_out, dict):

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\common.py:1174, in TensorDictModule.forward(self, tensordict, tensordict_out, *args, **kwargs)
   1165     tensors = tuple(  # type: ignore[unreachable]
   1166         tensordict._get_tuple_maybe_non_tensor(
   1167             _unravel_key_to_tuple(in_key),
   (...)   1171         for in_key in self.in_keys
   1172     )
   1173 try:
-> 1174     tensors_out = self._call_module(tensors, **kwargs)
   1175     if tensors_out is None:
   1176         tensors_out = ()

File E:\miniconda\envs\science\Lib\site-packages\tensordict\nn\common.py:1133, in TensorDictModule._call_module(self, tensors, **kwargs)
   1131 kwargs.update(self.method_kwargs)
   1132 if self.method is None:
-> 1133     out = self.module(*tensors, **kwargs)
   1134 else:
   1135     out = getattr(self.module, self.method)(*tensors, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1751, in Module._wrapped_call_impl(self, *args, **kwargs)
   1749     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1750 else:
-> 1751     return self._call_impl(*args, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1762, in Module._call_impl(self, *args, **kwargs)
   1757 # If we don't have any hooks, we want to skip the rest of the logic in
   1758 # this function, and just call forward.
   1759 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1760         or _global_backward_pre_hooks or _global_backward_hooks
   1761         or _global_forward_hooks or _global_forward_pre_hooks):
-> 1762     return forward_call(*args, **kwargs)
   1764 result = None
   1765 called_always_called_hooks = set()

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\container.py:240, in Sequential.forward(self, input)
    238 def forward(self, input):
    239     for module in self:
--> 240         input = module(input)
    241     return input

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1751, in Module._wrapped_call_impl(self, *args, **kwargs)
   1749     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1750 else:
-> 1751     return self._call_impl(*args, **kwargs)

File E:\miniconda\envs\science\Lib\site-packages\torch\nn\modules\module.py:1762, in Module._call_impl(self, *args, **kwargs)
   1757 # If we don't have any hooks, we want to skip the rest of the logic in
   1758 # this function, and just call forward.
   1759 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1760         or _global_backward_pre_hooks or _global_backward_hooks
   1761         or _global_forward_hooks or _global_forward_pre_hooks):
-> 1762     return forward_call(*args, **kwargs)
   1764 result = None
   1765 called_always_called_hooks = set()

File E:\miniconda\envs\science\Lib\site-packages\torchrl\modules\models\multiagent.py:166, in MultiAgentNetBase.forward(self, *inputs)
    161         output = output.expand(
    162             *output.shape[:-2], self.n_agents, n_agent_outputs
    163         )
    165 if output.shape[-2] != (self.n_agents):
--> 166     raise ValueError(
    167         f"Multi-agent network expected output with shape[-2]={self.n_agents}"
    168         f" but got {output.shape}"
    169     )
    171 return output

ValueError: Multi-agent network expected output with shape[-2]=3 but got torch.Size([4, 3, 6, 4])
Failed while executing module '0'.
```

## Expected behavior

I thought by specifying the agent_dim, the agents are to parallelize over the specified dimension instead of always sticking to dim=-2

```
td = TensorDict(
    {
        ("agents", "observation"): torch.randn(
            num_envs, seq_len, n_agents, obs_dim
        )
    },
    batch_size=[num_envs],
)
```
works as input, which means previous 
```
td = TensorDict(
    {
        ("agents", "observation"): torch.randn(
            num_envs, n_agents, seq_len, obs_dim
        )
    },
    batch_size=[num_envs],
)
```
was exactly the trigger. which means
```
super().__init__(
            n_agents=n_agents,
            centralized=False,
            share_params=share_params,
            agent_dim=1,  # (..., agents, features)
            device=device,
        )
```
was ineffective.
## System info

Describe the characteristic of your environment:
 * torchrl installed via pip 1 week ago
 * Python 3.11.11
 
## Checklist

- [* ] I have checked that there is no similar issue in the repo (**required**)
- [* ] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [* ] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c43f2120c9e0b65e8de891ef480b20378331398e`.  There
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
{"case_id": "pytorch_rl__3288__c43f212",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
