# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] vLLMWrapper prompt log-probs are incorrect

## Describe the bug

`vLLMWrapper` documents that the prompt log-probs it returns are not correct: the vLLM path used here does not provide usable `prompt_logprobs`, but the wrapper still writes a (padded / empty / placeholder) tensor into `LogProbs.prompt`. Users of GRPO / KL with `return_log_probs=True` can therefore consume silently wrong prompt log-probabilities.

This looks like an engine constraint, not a simple typo. The question for maintainers is what the public contract should be, not a request for a large rewrite.

## To Reproduce

When `return_log_probs=True` and `num_samples is None`, `_get_log_probs` (async / generate path) does:

```1830:1832:torchrl/modules/llm/policies/vllm_wrapper.py
            if self.num_samples is None:
                # TODO: this is not correct, we should use the prompt_logprobs
                #  but they're not returned by vLLM
```

It then reads `request_output_tc["prompt_logprobs"]` (`vllm_wrapper.py:1834-1861`). Nearby comments already describe the failure mode:

```1866:1883:torchrl/modules/llm/policies/vllm_wrapper.py
                    # Only set prompt log-probs if they actually contain
                    # data (vLLM V1 may produce all-zero padded tensors
                    # from empty per-request prompt_logprobs).
                    ...
                    # vLLM V1 may return prompt_logprobs=None per request,
                    # which from_request_output converts to empty tensors.
```

`prompt_logprobs` is requested when `return_log_probs=True`:

```610:620:torchrl/modules/llm/policies/vllm_wrapper.py
        prompt_logprobs = 1 if return_log_probs else None
        ...
        vllm_kwargs.setdefault("prompt_logprobs", prompt_logprobs)
```

If the engine still does not populate that field on the path used here, the wrapper either leaves `LogProbs.prompt` unset and later zero-fills, or stores a padded / empty tensor. Either way, a caller that reads `td["log_probs"].prompt` (GRPO KL, `RetrieveKL`, anything that scores the prompt) can get a silent wrong value rather than an error.

## Expected behavior

Please confirm the intended contract:

1. Can / should we request vLLM `prompt_logprobs` in a way that actually returns them on this generate path (and then use those values, dropping the "this is not correct" branch)?
2. If the engine cannot provide them, should `LogProbs.prompt` be omitted or set to `None`, with a warning, instead of a silently wrong tensor?

I am not proposing a rewrite of the wrapper. A documented answer (and a small change to match it) is enough.

## Screenshots

N/A

## System info

Observed on a source checkout of pytorch/rl at `1d3de3db`. Relevant when `vllm` is installed and `vLLMWrapper(..., return_log_probs=True)` is used for GRPO / KL.

## Additional context

`_build_prompt_logprobs` (`vllm_wrapper.py:2312`) already special-cases `request.prompt_logprobs is None` and zero-pads a shorter prefix. That helper makes the tensor look well-formed even when the engine returned nothing useful.

## Reason and Possible fixes

If vLLM can return `prompt_logprobs` on this path, plumb them through and delete the TODO. If it cannot, do not invent a dense tensor: leave `prompt` unset / `None` and warn once when `return_log_probs=True`. That is a contract decision for maintainers.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `06d57a05f5f9ae2ca7326e8afdbee7fa8d523f61`.  There
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
{"case_id": "pytorch_rl__4226__06d57a0",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
