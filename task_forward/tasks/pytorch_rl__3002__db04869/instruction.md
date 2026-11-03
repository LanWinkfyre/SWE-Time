# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] CUDAgraph policy changes the learning process

## Describe the bug

I have a single collector and I am training with ClipPPO a simple path finding policy. The agent must find a path in 3D around a simple maze while maximizing the coverage of the maze. It receives as input small patches centered around its current position and outputs the parameters to a Beta distribution (see example). From the distribution, we sample a value which is mapped to some action delta ($a_t \in R^3 $) to determine the next position. 

 To accelerate the experience sampling, I opted to apply CUDA graphs, but it seems to lead to unstable learning.

**A specific pathology I notice is that the standard deviation of the actions determined by the CUDAgraph'd policy tends to zero.**

## To Reproduce

I can't provide my full code, but the only difference is turning the cudagraph_policy=True in the collector. Maybe good to know that the policy module is `torch.compile`'d BEFORE it is passed onto the collector.


Policy (CNN extraction head + MLP, Beta distribution):
```python
class IndependentBeta(Independent):
    def __init__(
        self,
        alpha: torch.Tensor,
        beta: torch.Tensor,
        min: Union[float, torch.Tensor] = 0.0,
        max: Union[float, torch.Tensor] = 1.0,
        event_dims: int = 1,
    ):
        self.min = torch.as_tensor(min, device=alpha.device).broadcast_to(alpha.shape)
        self.max = torch.as_tensor(max, device=alpha.device).broadcast_to(alpha.shape)
        self.scale = self.max - self.min
        self.eps = torch.finfo(alpha.dtype).eps
        base_dist = Beta(alpha, beta)
        super().__init__(base_dist, event_dims)

    def sample(self, sample_shape: torch.Size = torch.Size()):
        return super().sample(sample_shape) * self.scale + self.min

    def rsample(self, sample_shape: torch.Size = torch.Size()):
        return super().rsample(sample_shape) * self.scale + self.min

    def log_prob(self, value: torch.Tensor):
        return super().log_prob(((value - self.min) / self.scale).clamp(self.eps, 1.0 - self.eps))

policy_module = ProbabilisticActor(
        module=TensorDictSequential(
            actor_cnn_module,  # Outputs TD with "alpha, beta"
        ),
        spec=action_spec,
        in_keys=["alpha", "beta"],
        out_keys=["action"],
        distribution_class=IndependentBeta,
        return_log_prob=True,
        default_interaction_type=InteractionType.RANDOM,
).to(device)

policy_module.compile(fullgraph=True, dynamic=False)
```

Collector:
```python
    collector = SyncDataCollector(
        create_env_fn=env_maker,  # Function to create environments
        policy=policy_module,
        # Total frames (steps) to collect in training
        total_frames=total_timesteps - collected_frames,
        frames_per_batch=config.frames_per_batch,
        # No initial random exploration phase needed if policy handles exploration
        init_random_frames=-1,
        split_trajs=False,  # Process rollouts as single batch
        device=device,  # Device for collector ops (usually same as models/env)
        # Device where data is stored (can be CPU if memory is tight)
        storing_device=device,
        max_frames_per_traj=config.max_episode_steps, 
        # num_threads=8
        # cudagraph_policy=True
    )
```

Training code (AMP+BF16):

```python
    for i, batch_data in enumerate(collector, start=collected_frames):
        current_frames = batch_data.numel()  # Number of steps collected in this batch
        collected_frames += current_frames

        for _ in range(config.update_epochs):
            batch_data = batch_data.reshape(-1)

            with (
                torch.no_grad(),
                torch.autocast(device.type, amp_dtype, enabled=config.amp),
            ):
                    adv_module(batch_data)

            for j in range(0, config.frames_per_batch, batch_size):
                minibatch = batch_data[j : j + batch_size]
                with torch.autocast(device.type, amp_dtype, enabled=config.amp):
                    loss_dict = loss_module(minibatch)

                    actor_loss = loss_dict["loss_objective"] + loss_dict["loss_entropy"]
                    critic_loss = loss_dict["loss_critic"]

                optimizer.zero_grad()
                scaler.scale(actor_loss).backward()
                scaler.scale(critic_loss).backward()
                scaler.unscale_(optimizer)
                grad_norm = torch.nn.utils.clip_grad_norm_(
                    loss_module.parameters(), config.max_grad_norm
                )
                scaler.step(optimizer)
                scaler.update()
```

## Expected behavior

The loss/training curves to be the same.

## Screenshots

Environment is a custom environment. Red is with `cudagraph_policy=False`, gray is `cudagraph_policy=True`

<img width="1454" alt="Image" src="https://github.com/user-attachments/assets/f2da88a1-ba07-45a9-8f8c-804bb10525a4" />

Page 2:

<img width="1248" alt="Image" src="https://github.com/user-attachments/assets/5dc57eb4-e159-4bd1-97b7-cbfc14467317" />

## System info

* torchrl==0.8.0 (pip, uv)
* Python 3.12.3
* Linux

## Additional context

Add any other context about the problem here.

## Reason and Possible fixes

No real idea why that might be.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `db04869339713457c2a5a32af47e4df25a59ef75`.  There
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
{"case_id": "pytorch_rl__3002__db04869",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
