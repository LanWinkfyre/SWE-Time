# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Server crashes with TypeError when workers > 1

## Description

Server crashes with `TypeError` when `server.workers` is set to a value greater than 1 in the configuration.

## Error Log

```
INFO     2026-03-25 14:52:36,770 llama_stack.cli.stack.run:167 cli: Listening on ['::', '0.0.0.0']:8321
Traceback (most recent call last):
  File "/home/dhiggins/workarea/llama-stack/.venv/bin/llama", line 10, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/dhiggins/workarea/llama-stack/src/llama_stack/cli/llama.py", line 52, in main
    parser.run(args)
  File "/home/dhiggins/workarea/llama-stack/src/llama_stack/cli/llama.py", line 46, in run
    args.func(args)
  File "/home/dhiggins/workarea/llama-stack/src/llama_stack/cli/stack/run.py", line 121, in _run_stack_run_cmd
    self._uvicorn_run(config_file, args)
  File "/home/dhiggins/workarea/llama-stack/src/llama_stack/cli/stack/run.py", line 179, in _uvicorn_run
    uvicorn.run("llama_stack.core.server.server:create_app", **uvicorn_config)
  File "/home/dhiggins/workarea/llama-stack/.venv/lib64/python3.12/site-packages/uvicorn/main.py", line 577, in run
    sock = config.bind_socket()
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/dhiggins/workarea/llama-stack/.venv/lib64/python3.12/site-packages/uvicorn/config.py", line 516, in bind_socket
    sock.bind((self.host, self.port))
TypeError: str, bytes or bytearray expected, not list
```

## Steps to Reproduce

1. Add `workers: 2` to your stack configuration:
   ```yaml
   server:
     port: 8321
     workers: 2
   ```

2. Run `llama stack run config.yaml`

3. Server crashes with the TypeError above

## Root Cause

The default host in `src/llama_stack/cli/stack/run.py` was incorrectly set to a list `["::", "0.0.0.0"]` instead of a string.

With `workers: 1` (default), uvicorn uses `asyncio.create_server()` which accepts a list of hosts and creates multiple listening sockets (one for IPv6, one for IPv4). This is why the bug wasn't caught initially.

With `workers > 1`, uvicorn must use multiprocessing and calls `socket.bind()` directly, which only accepts a string, causing the crash.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d2e4d1c48396a1b41d3c3ede4e1e8357b6fa3236`.  There
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
{"case_id": "ogx_ai_ogx__5283__d2e4d1c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
