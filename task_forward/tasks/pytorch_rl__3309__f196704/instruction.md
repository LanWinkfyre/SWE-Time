# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] giving target_entroy = N (only "auto" work) with crossQLoss do not work

## Describe the bug
Title + same problem with target_entropy inference corrected by @vmoens  on SAC 

## To Reproduce

In crossQLoss:
```
def maybe_init_target_entropy(self, fault_tolerant=True):
        """Initialize the target entropy.

        Args:
            fault_tolerant (bool, optional): if ``True``, returns None if the target entropy
                cannot be determined. Raises an exception otherwise. Defaults to ``True``.

        """
        if "_target_entropy" in self._buffers:
            return
        target_entropy = self._target_entropy
        if target_entropy == "auto":
            device = next(self.parameters()).device
            action_spec = self.get_action_spec()
            if action_spec is None:
                if fault_tolerant:
                    return
                raise RuntimeError(
                    "Cannot infer the dimensionality of the action. Consider providing "
                    "the target entropy explicitly or provide the spec of the "
                    "action tensor in the actor network."
                )
            if not isinstance(action_spec, Composite):
                action_spec = Composite({self.tensor_keys.action: action_spec})
            elif fault_tolerant and self.tensor_keys.action not in action_spec:
                return
            if (
                isinstance(self.tensor_keys.action, tuple)
                and len(self.tensor_keys.action) > 1
            ):
                action_container_shape = action_spec[self.tensor_keys.action[:-1]].shape
            else:
                action_container_shape = action_spec.shape
            target_entropy = -float(
                action_spec[self.tensor_keys.action]
                .shape[len(action_container_shape) :]
                .numel()
            )
        delattr(self, "_target_entropy")
        self.register_buffer(
            "_target_entropy", torch.tensor(target_entropy, device=device)
        )
        return self._target_entropy
```
If 'if target_entropy == "auto"' isn't accepted device isn't set so: 
```
self.register_buffer(
            "_target_entropy", torch.tensor(target_entropy, device=device)
        )
```
throw

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f196704ff363d25c36d27b6ffc888d80aa26d6d6`.  There
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
{"case_id": "pytorch_rl__3309__f196704",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
