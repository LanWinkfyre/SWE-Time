# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Compressing data stored in the Replay Buffer

## Motivation

Replay buffers are used to store a lot of data and ideally we could put this data on a GPU.
Often raw sensory observations are stored in these buffers, such as images or audio, which consumes many gigabytes of precious VRAM. 
In torchRL, memmapping and prefetching could be considered the fix for this issue but I have instead pursued compression instead. 

I've found that zstd is effective in compressing atari frames (reducing storage use by 150-250x) and my DQN implementation has gone from storing ~4M frames consuming ~20ish GB to less than a GB. 
I would like some pointers on where it might be sensible to integrate compression into the torch rl replay buffer in the hopes that compressing raw sensory observations could be more widely adopted. 

## Solution

I would like feedback on my proposed solutions to implementing compression in the replay buffer. 

**A CompressedReplayBuffer** class that inherents from the ReplayBuffer class could be one option.
This class would compress data "as it comes in", by modifying the `append` and `extend` functions.
The compressed data is then passed to the parent ReplayBuffer class as a uint8 byte stream for storage.
The compressed data is then decompressed in the `sample` function. 
Although, the issue in this approach is that the compressed byte stream can be of variable shape. 
Some images might be compressed into ~150 bytes, but others might be ~188 bytes. 
The TensorStorage object expects to receive objects of a consistent shape, so perhaps this is an inconvenient place to implement compression..

**A compressed storage type** might make more sense, as ultimately we want a storage type that can tolerate storing data of different lengths. 
One approach could be to use the standard replay buffer but with a `ListStorage` type.
By modifying the `get` and `set` functions we could compress and decompress as data comes in and out. 
Alternatively, `TensorStorage` could be modified to use a [nested & jagged layout](https://docs.pytorch.org/docs/stable/nested.html), which might be more efficient.

## Additional context

Although I have used zstd as the compression algorithm in this issue, ideally we don't lock someone into using it. 
Compression is just converting any arbitrary tensor into a uint8 1d tensor (the byte stream) and then decompression is rebuilding the prior tensor and recovering the shape and datatype. 
If the data is sensory observations from a gym-like environment, we can reconstruct the observation's original shape and datatype from the gym environment metadata. 

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0627e85c78756b4e4dbde726a9d5e85300e239a0`.  There
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
{"case_id": "pytorch_rl__2983__0627e85",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
