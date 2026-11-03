# Locate the commit that introduced this regression

A regression was reported against `Comfy-Org/ComfyUI`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ComfyUI fails to start with database error 

### Custom Node Testing

- [x] I have tried disabling custom nodes and the issue persists (see [how to disable custom nodes](https://docs.comfy.org/troubleshooting/custom-node-issues#step-1%3A-test-with-all-custom-nodes-disabled) if you need help)

### Expected Behavior

Updated ComfyUI with git pull, installed new requirements. Now fails to start.

### Actual Behavior

Failed to start with database errors:

```
Context impl SQLiteImpl.
Will assume non-transactional DDL.
Assets scan(roots=['models']) completed in 0.020s (created=0, skipped_existing=0, total_seen=11)
Failed to initialize database. Please ensure you have installed the latest requirements. If the error persists, please report this as in future the database will be required: Can't use explicit RETURNING for bulk INSERT operation with sqlite+pysqlite backend; executemany with RETURNING is not enabled for this dialect.
```

### Steps to Reproduce

This isn't a bug with custom nodes, ComfyUI doesn't even start properly, and the error also occurs with "--disable-all-custom-nodes". 

I deleted my ComfyUI folder and cloned it again, same error. I deleted my venv and created it again, same error. 

 

I checked bug #11754 which seems related but is probably a different bug.



### Debug Logs

```powershell
$ python3 main.py 
Checkpoint files will always be loaded safely.
Total VRAM 11004 MB, total RAM 64215 MB
pytorch version: 2.9.1+cu128
Set vram state to: NORMAL_VRAM
Device: cuda:0 NVIDIA GeForce RTX 2080 Ti : cudaMallocAsync
Using async weight offloading with 2 streams
Enabled pinned memory 61003.0
working around nvidia conv3d memory bug.
WARNING: You need pytorch with cu130 or higher to use optimized CUDA operations.
Found comfy_kitchen backend eager: {'available': True, 'disabled': False, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8', 'scaled_mm_nvfp4']}
Found comfy_kitchen backend cuda: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8', 'scaled_mm_nvfp4']}
Found comfy_kitchen backend triton: {'available': True, 'disabled': True, 'unavailable_reason': None, 'capabilities': ['apply_rope', 'apply_rope1', 'dequantize_nvfp4', 'dequantize_per_tensor_fp8', 'quantize_nvfp4', 'quantize_per_tensor_fp8']}
Using pytorch attention
Python version: 3.11.10 (main, Sep  7 2024, 18:35:42) [GCC 9.4.0]
ComfyUI version: 0.8.2
ComfyUI frontend version: 1.36.13
[Prompt Server] web root: /home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/comfyui_frontend_package/static

Import times for custom nodes:
   0.0 seconds: /home/florian/comfy_ggufs/ComfyUI/custom_nodes/websocket_image_save.py

Context impl SQLiteImpl.
Will assume non-transactional DDL.
Assets scan(roots=['models']) completed in 0.020s (created=0, skipped_existing=0, total_seen=11)
Failed to initialize database. Please ensure you have installed the latest requirements. If the error persists, please report this as in future the database will be required: Can't use explicit RETURNING for bulk INSERT operation with sqlite+pysqlite backend; executemany with RETURNING is not enabled for this dialect.
Starting server

To see the GUI go to: http://127.0.0.1:8188
Error handling request from 127.0.0.1
Traceback (most recent call last):
  File "/home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/aiohttp/web_protocol.py", line 510, in _handle_request
    resp = await request_handler(request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/aiohttp/web_app.py", line 569, in _handle
    return await handler(request)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/aiohttp/web_middlewares.py", line 117, in impl
    return await handler(request)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/ComfyUI/middleware/cache_middleware.py", line 27, in cache_control
    response: web.Response = await handler(request)
                             ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/ComfyUI/server.py", line 83, in deprecation_warning
    response: web.Response = await handler(request)
                             ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/ComfyUI/server.py", line 173, in origin_only_middleware
    response = await handler(request)
               ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/ComfyUI/server.py", line 689, in get_object_info
    seed_assets(["models"])
  File "/home/florian/comfy_ggufs/ComfyUI/app/assets/scanner.py", line 82, in seed_assets
    result = seed_from_paths_batch(sess, specs=specs, owner_id="")
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/ComfyUI/app/assets/database/bulk_ops.py", line 102, in seed_from_paths_batch
    winners_by_path.update((session.execute(ins_state, chunk)).scalars().all())
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2365, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2251, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/sqlalchemy/orm/bulk_persistence.py", line 1292, in orm_execute_statement
    result = _bulk_insert(
             ^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/sqlalchemy/orm/bulk_persistence.py", line 222, in _bulk_insert
    result = persistence._emit_insert_statements(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/florian/comfy_ggufs/.venv_neu/lib/python3.11/site-packages/sqlalchemy/orm/persistence.py", line 1107, in _emit_insert_statements
    raise sa_exc.InvalidRequestError(
sqlalchemy.exc.InvalidRequestError: Can't use explicit RETURNING for bulk INSERT operation with sqlite+pysqlite backend; executemany with RETURNING is not enabled for this dialect.
```
```

## What you have

- `/testbed/repo` is a git clone of `Comfy-Org/ComfyUI` truncated just after the regression was
  reported.  `HEAD` is `dc202a2e51bf7a6cd00e606b2d2941bc223f2ad2` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
