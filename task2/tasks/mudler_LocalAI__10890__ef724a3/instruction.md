# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Cannot install any backend: operation not supported

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
LocalAI v4.7.1 (b224c96db6f4b87306a33a808650bfce63b12588)

**Environment, CPU architecture, OS, and Version:**
docker install CUDA 12 version
localai/localai:latest-gpu-nvidia-cuda-12


```yaml
services:
  local-ai:
    container_name: local-ai
    hostname: local-ai
    restart: unless-stopped
    image: localai/localai:latest-gpu-nvidia-cuda-12
    user: 1000:1000
    networks:
      - ReverseProxyNetwork
    environment:
      - MODELS_PATH=/models
    volumes:
      - localai-models:/models:cached
      - localai-backends:/backends:Z
      - ../../data/localAi/images/:/tmp/generated/images/
    deploy:
      resources:
        limits:
          memory: 12GB
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu] 
networks:
  ReverseProxyNetwork:
    external: true
    name: "ReverseProxyNetwork"

volumes:
  localai-models:
    driver: local
    driver_opts:
      type: cifs
      device: //xxx/sharedExtern/StableDiffusion/localAi/models/
      o: "username=${},password=${},uid=1000,gid=1000,iocharset=utf8,vers=3.1.1,file_mode=0755,dir_mode=0755"
  localai-backends:
    driver: local
    driver_opts:
      type: cifs
      device: //xxx/sharedExtern/StableDiffusion/localAi/backends/
      o: "username=${},password=${},uid=1000,gid=1000,iocharset=utf8,vers=3.1.1,file_mode=0755,dir_mode=0755"
```

**Describe the bug**
Whenever i try to install any backend, be it directly though the store or indirectly though the store with a model i get the same error. The models get downloaded just fine, just the backend install seems to fail. The backeend folder is empty after the error.

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->

**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->

**Logs**
```
local-ai  | Jul 17 16:47:48 INFO  Fallback URI failed fallback="quay.io/go-skynet/local-ai-backends:master-gpu-nvidia-cuda-12-llama-cpp" error=failed to extract image tar: symlink libcublas.so.12.8.5.5 /backends/cuda12-llama-cpp.install-tmp/lib/libcublas.so: operation not supported 
local-ai  | Jul 17 16:47:48 INFO  Trying development fallback URI fallback="quay.io/go-skynet/local-ai-backends:master-gpu-nvidia-cuda-12-llama-cpp-development" 
local-ai  | Jul 17 16:47:48 INFO  Development fallback URI failed fallback="quay.io/go-skynet/local-ai-backends:master-gpu-nvidia-cuda-12-llama-cpp-development" error=failed to get image "quay.io/go-skynet/local-ai-backends:master-gpu-nvidia-cuda-12-llama-cpp-development": GET https://quay.io/v2/go-skynet/local-ai-backends/manifests/master-gpu-nvidia-cuda-12-llama-cpp-development: MANIFEST_UNKNOWN: manifest unknown; map[] 
local-ai  | Jul 17 16:47:48 ERROR Failed to download backend uri="quay.io/go-skynet/local-ai-backends:latest-gpu-nvidia-cuda-12-llama-cpp" backendPath="/backends/cuda12-llama-cpp.install-tmp" error=failed to extract image tar: symlink libcublas.so.12.8.5.5 /backends/cuda12-llama-cpp.install-tmp/lib/libcublas.so: operation not supported 

```

**Additional context**
<!-- Add any other context about the problem here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ef724a3c9db8bfdf8114a389f6339033c1d61e76`.  There
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
{"case_id": "mudler_LocalAI__10890__ef724a3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
