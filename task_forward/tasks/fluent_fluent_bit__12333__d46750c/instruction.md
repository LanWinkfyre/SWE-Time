# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Hot reload fails to resolve relative file paths against the main configuration directory

## Bug Report

**Describe the bug**

Fluent Bit can load service files relative to the directory containing the main configuration during startup, but hot reload cannot resolve the same paths.

This is reproducible with both `Parsers_File parsers.conf` and `Plugins_File plugins.conf` on current `master`. In both cases, startup succeeds and hot reload fails. Using an absolute path allows the reload to succeed.

The reload request is initially accepted:

```json
{"reload":"done","status":0}
```

The asynchronous reload then fails. For `Parsers_File`, the error is:

```text
[error] [config] could not configure service property 'parsers_file'
[error] [reload] reloaded config format is invalid. Reloading is halted
```

`Plugins_File` fails in the same way:

```text
[error] [config] could not configure service property 'plugins_file'
[error] [reload] reloaded config format is invalid. Reloading is halted
```

The running process keeps its previous configuration, but none of the changes from the failed reload are applied.

**To Reproduce**

Create a temporary configuration directory:

```shell
mkdir -p /tmp/fluent-bit-reload
```

Create `/tmp/fluent-bit-reload/parsers.conf`:

```text
[PARSER]
    Name   reload_test
    Format json
```

Create `/tmp/fluent-bit-reload/fluent-bit.conf`:

```text
[SERVICE]
    Flush        1
    Log_Level    info
    Parsers_File parsers.conf
    HTTP_Server  On
    HTTP_Listen  127.0.0.1
    HTTP_Port    2020
    Hot_Reload   On

[INPUT]
    Name    dummy
    Samples 1

[OUTPUT]
    Name  stdout
    Match *
```

Start Fluent Bit from your home directory:

```shell
cd "$HOME"
/path/to/fluent-bit -c /tmp/fluent-bit-reload/fluent-bit.conf
```

Trigger hot reload from another terminal:

```shell
curl -X POST -d '{}' http://127.0.0.1:2020/api/v2/reload
```

Initial startup loads `parsers.conf` relative to `fluent-bit.conf`. Hot reload fails because it tries to find `parsers.conf` relative to the process working directory instead.

Changing `Parsers_File` to `/tmp/fluent-bit-reload/parsers.conf` allows the reload to succeed.

The failure can also be reproduced by replacing `Parsers_File` with a relative `Plugins_File` and providing a valid plugin configuration file beside the main configuration.

**Expected behavior**

File paths resolved against the main configuration directory during startup should be resolved against the same directory during hot reload.

**Your Environment**

- Version used: Fluent Bit v5.1.1, commit `3713988105fffaded9899d2914a42e04ed0e57e7`
- Operating system: macOS 26.6.2, arm64
- Configuration format: classic
- Reload mechanism: HTTP API

**Additional context**

Fluent Bit records the directory containing the main configuration in `conf_path` during startup. The new configuration context created during hot reload preserves `conf_path_file`, but not `conf_path`. Loaders that depend on `conf_path` therefore cannot resolve relative files unless the process working directory happens to contain them.

The same configuration directory is also consulted when loading stream processor files and some plugin-specific files, so other relative path settings may be affected.

The parser failure has been reported several times. Previous issues were closed after using absolute paths as a workaround or by stale automation.

Related:
- https://github.com/fluent/fluent-bit/issues/8038
- https://github.com/fluent/fluent-bit/issues/8275
- https://github.com/fluent/fluent-bit/issues/8497
- https://github.com/fluent/fluent-bit/issues/8817
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d46750cbbf8cfd45a1068f01413d7896555541ce`.  There
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
{"case_id": "fluent_fluent_bit__12333__d46750c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
