# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Intel Arc Pro b70 Not Detected When Using the Intel GPU Image

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
<!-- Container Image or LocalAI tag/commit -->
- image: `localai/localai:master-gpu-intel`
- id: `bf7689146833`

**Environment, CPU architecture, OS, and Version:**
<!-- Provide the output from "uname -a", HW specs, if it's a VM  -->
The docker container is running within an LXC container on a proxmox host with the latest 6.17.13 kernel.

### HW specs:
- CPU: AMD Ryzen 5 5600 6-Core Processor
- GFX0: Intel Corporation DG2 [Arc A380] (rev 05)
- GFX1: Intel Corporation Battlemage G21 [Intel Graphics]
### OS Info:
#### Proxmox host
- uname: `Linux shadesmar 6.17.13-2-pve #1 SMP PREEMPT_DYNAMIC PMX 6.17.13-2 (2026-03-13T08:06Z) x86_64 GNU/Linux`
- os-release: `Debian GNU/Linux 13 (trixie)`
#### LXC container
- uname: `Linux localai 6.17.13-2-pve #1 SMP PREEMPT_DYNAMIC PMX 6.17.13-2 (2026-03-13T08:06Z) x86_64 GNU/Linux`
- os-release: `Debian GNU/Linux 13 (trixie)`
#### Docker container
- uname: `Linux b9d5c5b40f01 6.17.13-2-pve #1 SMP PREEMPT_DYNAMIC PMX 6.17.13-2 (2026-03-13T08:06Z) x86_64 x86_64 x86_64 GNU/Linux`
- os-release: `Ubuntu 24.04.3 LTS`


**Describe the bug**
<!-- A clear and concise description of what the bug is. -->
Intel Arc Pro B70 is not recognized by the intel driver stack in the docker container. The a380 is detected and used just fine, but the drivers can't detect the b70. `sycl-ls` doesn't see it at all.

installing the compute packages as instructed in these intel docs fixes it:
https://dgpu-docs.intel.com/driver/client/overview.html

**To Reproduce**
<!-- Steps to reproduce the behavior, including the LocalAI command used, if any -->
- Install a b70
- install docker + compose
- start the compose file
- exec into container
  - observe sycl-ls doesn't show the b70:
    - `root@a16191091266:/# sycl-ls
[opencl:cpu][opencl:0] Intel(R) OpenCL, AMD Ryzen 5 5600 6-Core Processor               OpenCL 3.0 (Build 0) [2025.20.10.0.10_160000`
  - install the new drivers
  - observe sycl-ls now shows the b70
    - `root@a16191091266:/# sycl-ls
[level_zero:gpu][level_zero:0] Intel(R) oneAPI Unified Runtime over Level-Zero V2, Intel(R) Graphics [0xe223] 20.2.0 [1.14.37020+3]
[opencl:cpu][opencl:0] Intel(R) OpenCL, AMD Ryzen 5 5600 6-Core Processor               OpenCL 3.0 (Build 0) [2025.20.10.0.10_160000]
[opencl:gpu][opencl:1] Intel(R) OpenCL Graphics, Intel(R) Graphics [0xe223] OpenCL 3.0 NEO  [26.05.37020.3]`

### docker compose file
```
services:
  localai:
    image: localai/localai:master-gpu-intel
    container_name: localai

    # ── Intel GPU passthrough ─────────────────────────────────────────────────
    # /dev/dri exposes all DRM render nodes (card0, renderD128, etc.)
    # privileged is the safest catch-all; replace with targeted devices if
    # you know your exact render node (e.g. --device /dev/dri/renderD128).
    devices:
      - /dev/dri:/dev/dri
    # group_add: render grants access to the render group without full root.
    group_add:
      - 992

    depends_on:
      postgres:
        condition: service_healthy

    ports:
      - "8080:8080"

    environment:
      # ── General ────────────────────────────────────────────────────────────
      MODELS_PATH: /models
      LOCALAI_DATA_PATH: /data   # agent state, knowledge base, config

      # ── Intel / SYCL ───────────────────────────────────────────────────────
      # Force the SYCL/oneAPI backend for all llama.cpp model loads.
      LOCALAI_SINGLE_ACTIVE_BACKEND: "true"   # one backend at a time → saves VRAM
      THREADS: "1"               # SYCL full-GPU offload works best with 1 CPU thread

      # ── Performance / context ──────────────────────────────────────────────
      CONTEXT_SIZE: "4096"

      # ── VRAM watchdog (prevents stale models eating GPU memory) ────────────
      LOCALAI_WATCHDOG_IDLE: "true"
      LOCALAI_WATCHDOG_IDLE_TIMEOUT: "15m"
      LOCALAI_WATCHDOG_BUSY: "true"
      LOCALAI_WATCHDOG_BUSY_TIMEOUT: "5m"

      # ── Agent pool defaults ────────────────────────────────────────────────
      # These set pool-level defaults; individual agents can override them.
      LOCALAI_AGENT_POOL_DEFAULT_MODEL: "hermes-3-llama3.1-8b"
      LOCALAI_AGENT_POOL_EMBEDDING_MODEL: "granite-embedding-107m-multilingual"
      LOCALAI_AGENT_POOL_ENABLE_SKILLS: "true"
      LOCALAI_AGENT_POOL_ENABLE_LOGS: "true"

      # ── PostgreSQL-backed vector store ─────────────────────────────────────
      LOCALAI_AGENT_POOL_VECTOR_ENGINE: "postgres"
      LOCALAI_AGENT_POOL_DATABASE_URL: "postgresql://localrecall:localrecall@postgres:5432/localrecall?sslmode=disable"

    volumes:
      # Downloaded model weights — survives container upgrades
      - localai_models:/models
      # Agent definitions, knowledge base (chromem vectors), skills, logs
      - localai_data:/data
      # LocalAI config files (backends, galleries, etc.)
      - localai_config:/etc/localai
      # Bind-mount a local ./model-configs/ folder to inject custom YAML
      # configs without rebuilding the image. Create the folder first.
      - ./model-configs:/models/configs:ro

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/readyz"]
      interval: 30s
      timeout: 10s
      retries: 10
      start_period: 120s    # allow extra time for first-run model downloads

    restart: unless-stopped

  postgres:
    image: quay.io/mudler/localrecall:v0.5.2-postgresql
    container_name: localai-postgres
    environment:
      POSTGRES_USER: localrecall
      POSTGRES_PASSWORD: localrecall
      POSTGRES_DB: localrecall
    volumes:
      - localai_pgdata:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U localrecall"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

# =============================================================================
# Named volumes — Docker manages these; data persists across `docker compose down`
# Use `docker compose down -v` only if you want to wipe everything.
# =============================================================================
volumes:
  localai_models:
    driver: local
  localai_data:
    driver: local
  localai_config:
    driver: local
  localai_pgdata:
    driver: loca
```


**Expected behavior**
<!-- A clear and concise description of what you expected to happen. -->
- b70 detected and usable

**Logs**
<!-- If applicable, add logs while running LocalAI in debug mode (`--debug` or `DEBUG=true`) to help explain your problem.  -->

**Additional context**
<!-- Add any other context about the problem here. -->
Installing the drivers like this fixed it:
```
apt-get update
apt-get install -y software-properties-common
add-apt-repository -y ppa:kobuk-team/intel-graphics
apt-get install -y libze-intel-gpu1 libze1 intel-metrics-discovery intel-opencl-icd clinfo intel-gsc
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1c9592c77ff9c253fe23250e490cc5c09f002f4d`.  There
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
{"case_id": "mudler_LocalAI__9540__1c9592c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
