# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
chatterbox backend fails to load on fresh install: unpinned torch/transformers pull incompatible versions

## Description

Installing the `cuda12-chatterbox` gallery backend on a fresh host currently produces a backend that cannot load the model at all, because several dependencies are unpinned and pip/uv resolve to versions that break chatterbox-tts 0.3.1.

Observed on: RTX 3090 x2, NVIDIA driver 550.163 (CUDA 12.4), LocalAI v4.7.1, backend installed via the gallery (`quay.io/go-skynet/local-ai-backends:latest-gpu-nvidia-cuda-12-chatterbox`).

## Failures, in the order they surface

**1. torch resolves to a `cu130` wheel, but the host driver only supports CUDA 12.4**

`requirements-cublas12.txt` lists `torch`/`torchaudio` with no version pin. A fresh install pulled `torch==2.13.0+cu130`, which cannot initialize CUDA on a driver capped at 12.4:

```
RuntimeError: The NVIDIA driver on your system is too old (found version 12040).
```

Fix: pin to a `cu124` build, e.g. `torch==2.6.0+cu124` / `torchaudio==2.6.0+cu124` (or otherwise match the wheel to the CUDA version the install script already detects for llama.cpp).

**2. transformers resolves to 5.x, which dropped `LlamaConfig.rope_theta`**

Also unpinned in `requirements-cublas12.txt`. chatterbox-tts 0.3.1's T3 config still reads `config.rope_theta`, which no longer exists on transformers 5.x's `LlamaConfig`:

```
AttributeError: 'LlamaConfig' object has no attribute 'rope_theta'
```

Fix: pin `transformers==4.46.3` (or whatever range chatterbox-tts 0.3.1 actually supports upstream).

**3. setuptools >=81 dropped `pkg_resources`, silently disabling the watermarker**

`perth` (chatterbox's audio watermarking dep) imports `pkg_resources` inside a bare `try/except ImportError`, silently falling back to `PerthImplicitWatermarker = None` when it's missing. Modern setuptools (81+, itself pulled in transitively) removed `pkg_resources` by default, so `ChatterboxTTS.__init__` then does:

```python
self.watermarker = perth.PerthImplicitWatermarker()  # None() -> TypeError
```

```
TypeError: 'NoneType' object is not callable
```

This one is particularly nasty to debug because the real cause (missing `pkg_resources`) is swallowed by perth's own exception handling — the traceback only points at the call site, not the import failure.

Fix: pin `setuptools<81` in the backend's requirements.

**4. chatterbox-tts >=0.3's `generate()` now requires `language_id`**

Once the above three are fixed, the model loads, but every `/tts` call fails:

```
TypeError: ChatterboxTTS.generate() missing 1 required positional argument: 'language_id'
```

`backend.py`'s `TTS` handler builds `kwargs` from request params but never sets `language_id`, which upstream chatterbox-tts made a required (non-defaulted) argument in the multilingual-capable releases.

Fix: default it, e.g.:

```python
kwargs.setdefault("language_id", "en")
```

## Suggested fix summary

In the chatterbox backend's requirements file(s):
- pin `torch`/`torchaudio` to a build matching the backend's detected CUDA version (not just "latest")
- pin `transformers==4.46.3`
- pin `setuptools<81`

In `backend.py`'s `TTS` handler:
- `kwargs.setdefault("language_id", "en")` before calling `self.model.generate(...)`

Happy to open a PR with these pins/patch if useful — wanted to file the report first since I'm not sure which requirements file(s) upstream intends to be the source of truth (`requirements-cublas12.txt` vs the shared `requirements.txt`).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `49ef40a1877f15612fa49a0f917e5c2fe8a28293`.  There
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
{"case_id": "mudler_LocalAI__11070__49ef40a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
