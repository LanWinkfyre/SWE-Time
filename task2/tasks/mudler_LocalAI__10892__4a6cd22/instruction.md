# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Use vMLX for all MLX models on mac whenever possible (chat/stt/tts at least)

**Is your feature request related to a problem? Please describe.**
Right now on mac you get a ton of problems with especially sst/tts using the defaults, but in general all mlx models run better under vMLX (And vMLX-Audio) than they do under llama.cpp.  

**Describe the solution you'd like**
It would be great if whenever possible all of the gallery models just used this automatically and in the case of manual loads, if it's an MLX model it is auto chosen.

And on mac, it should prefer the mlx version of a given model if there is an option in the gallery.

**Describe alternatives you've considered**
You can do this manually, but I've had varied luck getting these to run reliably.

**Additional context**
Getting mac support improved with things like this will help significantly given how hard it is to get hardware acceleration under docker on a mac.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4a6cd227a32cf58a9232c8fcfefb69a18aa78e3a`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__10892__4a6cd22",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
