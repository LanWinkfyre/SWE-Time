# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Launcher does not pass --data-path, --config-dir, or --state-dir to local-ai run, causing state dirs to resolve to ~/data and ~/configuration instead of under ~/.localai

**LocalAI version:**
v4.5.5, source code analysis for mudler/LocalAI@dfaec3bd

**Environment, CPU architecture, OS, and Version:**
Linux miki-linux-ai 7.1.2-2-cachyos #1 SMP PREEMPT_DYNAMIC Sun, 28 Jun 2026 15:38:15 +0000 x86_64 GNU/Linux
CPU: AMD Ryzen 9950X3D
OS: CachyOS, rolling release

**Describe the bug**
When using the Linux launcher application to start the LocalAI server, two directories are created in the user's home directory that should logically be under `~/.localai`:

- `~/data` (contains agent pool state, outputs, collections, assets)
- `~/configuration` (dynamic config files)

## Log Evidence

The LocalAI log shows:

```
[14:46:37] STDOUT: Jun 30 14:46:37 INFO  Agent pool started (standalone/LocalAGI mode) stateDir="/home/miki/data" apiURL="http://127.0.0.1:8080"
```

The `stateDir` resolves to `/home/miki/data` rather than `~/.localai/data`.

## Root Cause Analysis

### 1. The launcher does not pass state directory flags

In `cmd/launcher/internal/launcher.go`, the `StartLocalAI()` method builds these args:

```go
args := []string{
    "run",
    "--models-path", l.config.ModelsPath,
    "--backends-path", l.config.BackendsPath,
    "--address", l.config.Address,
    "--log-level", l.config.LogLevel,
}
```

There is **no** `--data-path`, `--config-dir`, or `--state-dir` flag passed.

### 2. The server defaults to `${basepath}/data` and `${basepath}/configuration`

In `core/cli/run.go`:

```go
DataPath                     string        `env:"LOCALAI_DATA_PATH" type:"path" default:"${basepath}/data" ...`
LocalaiConfigDir             string        `env:"LOCALAI_CONFIG_DIR" type:"path" default:"${basepath}/configuration" ...`
```

### 3. `${basepath}` is resolved by kong.ExpandPath("."), which expands to the launcher's CWD

In `cmd/local-ai/main.go`:

```go
kong.Vars{
    "basepath":  kong.ExpandPath("."),
    ...
}
```

`kong.ExpandPath(".")` expands `.` (current working directory) to an absolute path.

### 4. The launcher does not set a working directory on the exec.Command

```go
l.localaiCmd = exec.CommandContext(l.ctx, binaryPath, args...)
```

There is no `.Dir()` call, so the child process inherits the parent's CWD. If the launcher GUI is started from `/home/miki`, that becomes the working directory.

### 5. Resulting path resolution

- `${basepath}` = `/home/miki`
- `DataPath` = `/home/miki/data`
- `LocalaiConfigDir` = `/home/miki/configuration`

### 6. The agent pool stateDir follows the same chain

In `core/services/agentpool/agent_pool.go:184`:

```go
stateDir := cmp.Or(cfg.StateDir, s.appConfig.DataPath, s.appConfig.DynamicConfigsDir, "agents")
```

`cfg.StateDir` is empty (not passed).
`s.appConfig.DataPath` = `/home/miki/data` (from `${basepath}/data`).
`s.appConfig.DynamicConfigsDir` = `/home/miki/configuration` (from `${basepath}/configuration`).

### 7. No commits since v4.5.5 have addressed this

Checked `git log v4.5.5..master -- core/cli/run.go cmd/launcher/` — no commits modify the data/config paths or add `--data-path`/`--config-dir`/`--state-dir` flags to the launcher.

## Impact

- Data and configuration are stored in the user's home directory root instead of under `~/.localai`
- This is inconsistent with the launcher's own `GetDataPath()` which returns `~/.localai`
- Confusing for users expecting data to be organized under `~/.localai`
- May cause issues if users set up volume mounts or home directory restrictions

## Suggested Fix

Add `--data-path` and `--config-dir` flags to the launcher's `StartLocalAI()` method, pointing to paths under `~/.localai`. Also consider setting the working directory on the exec.Command to the launcher's own config directory, or add `DataPath`/`ConfigDir` fields to the launcher's `Config` struct.

## Files Involved

- `cmd/launcher/internal/launcher.go` — `StartLocalAI()`, `Config` struct
- `core/cli/run.go` — `RunCMD` struct, defaults for `DataPath` and `LocalaiConfigDir`
- `cmd/local-ai/main.go` — kong vars definition of `${basepath}`
- `core/services/agentpool/agent_pool.go` — `stateDir` computation

Assisted-by: ornith-1.0-9b
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `25ecb9f0158c2d27788f385b4d06fc12dbfd8d0b`.  There
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
{"case_id": "mudler_LocalAI__10610__25ecb9f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
