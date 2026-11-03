# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
SQL Postgres backend fails with special characters in password (DNS resolution error)

### System Info

 ## Environment
  - OGX version: `1.0.2`
  - Backend: `sql_postgres`
  - Python version: `3.12`

### Information

- [x] The official example scripts
- [ ] My own modified scripts

### 🐛 Describe the bug

 ## Description

  The sql_postgres storage backend fails to connect when the password contains special characters like @, :, /, or %. The connection fails with a DNS resolution error (socket.gaierror: [Errno -2] Name or service
   not known) because the password is not URL-encoded before being interpolated into the connection string.

  ## Steps to Reproduce

  1. Configure a sql_postgres backend with a password containing special characters:
  ```yaml
  storage:
    backends:
      sql_default:
        type: sql_postgres
        host: my-host
        port: 5432
        db: pg-db
        user: pg-user
        password: "my@pass:word" 
  ```
        
  2. Start the OGX server
  3. Observe connection failure with DNS resolution error

  ## Expected Behavior

  The SQL Postgres backend should connect successfully, similar to how `kv_postgres` handles the same credentials with special characters.

  ## Actual Behavior
  
  Connection fails with:
  socket.gaierror: [Errno -2] Name or service not known
  
  The URL parsing fails because special characters in the password break the connection string format, like @, :, /    and %.

  ## Root Cause

  File: **ogx/core/storage/datatypes.py, lines 212-213**

   ```python
  @property
  def engine_str(self) -> str:
      return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
   ```
  The password (and other fields) are not URL-encoded before interpolation. Special characters like @ or : in the password break the URL parsing:
  - @ is interpreted as the user/host separator
  - : is interpreted as the user/password separator
  - / breaks the path parsing
  
  Comparison: The kv_postgres backend doesn't have this issue because it passes connection parameters directly to `asyncpg.create_pool()` without URL string construction (see
  `ogx/core/storage/kvstore/postgres/postgres.py`, lines 56-65).

  ## Proposed Solution
  
  URL-encode the password and other potentially problematic fields:
  ```python
  from urllib.parse import quote_plus
  
  @property
  def engine_str(self) -> str:
      encoded_user = quote_plus(self.user) if self.user else ""
      encoded_password = quote_plus(self.password) if self.password else ""
      return f"postgresql+asyncpg://{encoded_user}:{encoded_password}@{self.host}:{self.port}/{self.db}"
 ```
  ## Workaround

  Use alphanumeric-only passwords (no special characters) for SQL Postgres backends.


### Error logs

```
Traceback (most recent call last):
  File "/opt/app-root/bin/uvicorn", line 10, in <module>
    sys.exit(main())
             ^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/click/core.py", line 1514, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/click/core.py", line 1435, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/click/core.py", line 1298, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/click/core.py", line 853, in invoke
    return callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/uvicorn/main.py", line 441, in main
    run(
  File "/opt/app-root/lib64/python3.12/site-packages/uvicorn/main.py", line 620, in run
    server.run()
  File "/opt/app-root/lib64/python3.12/site-packages/uvicorn/server.py", line 75, in run
    return asyncio_run(self.serve(sockets=sockets), loop_factory=self.config.get_loop_factory())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/uvicorn/server.py", line 79, in serve
    await self._serve(sockets)
  File "/opt/app-root/lib64/python3.12/site-packages/uvicorn/server.py", line 86, in _serve
    config.load()
  File "/opt/app-root/lib64/python3.12/site-packages/uvicorn/config.py", line 484, in load
    self.loaded_app = self.loaded_app()
                      ^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/ogx/core/server/server.py", line 264, in create_app
    app = StackApp(
          ^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/ogx/core/server/server.py", line 121, in __init__
    future.result()
  File "/usr/lib64/python3.12/concurrent/futures/_base.py", line 456, in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/concurrent/futures/_base.py", line 401, in __get_result
    raise self._exception
  File "/usr/lib64/python3.12/concurrent/futures/thread.py", line 59, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/ogx/core/stack.py", line 763, in initialize
    await register_connectors(self.run_config, impls)
  File "/opt/app-root/lib64/python3.12/site-packages/ogx/core/stack.py", line 344, in register_connectors
    existing_connectors = await connectors_impl.list_connectors()
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/ogx/core/connectors/connectors.py", line 177, in list_connectors
    results = await self.sql_store.fetch_all(table=TABLE_CONNECTORS)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/ogx/core/storage/sqlstore/authorized_sqlstore.py", line 188, in fetch_all
    rows = await self.sql_store.fetch_all(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/ogx/core/storage/sqlstore/sqlalchemy_sqlstore.py", line 242, in fetch_all
    await self._ensure_engine()  # Lazy init in current event loop
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/ogx/core/storage/sqlstore/sqlalchemy_sqlstore.py", line 100, in _ensure_engine
    async with self._engine.begin() as conn:
               ^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/contextlib.py", line 210, in __aenter__
    return await anext(self.gen)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/ext/asyncio/engine.py", line 1068, in begin
    async with conn:
               ^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/ext/asyncio/base.py", line 121, in __aenter__
    return await self.start(is_ctxmanager=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/ext/asyncio/engine.py", line 275, in start
    await greenlet_spawn(self.sync_engine.connect)
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 201, in greenlet_spawn
    result = context.throw(*sys.exc_info())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/engine/base.py", line 3293, in connect
    return self._connection_cls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/engine/base.py", line 3317, in raw_connection
    return self.pool.connect()
           ^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/base.py", line 448, in connect
    return _ConnectionFairy._checkout(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/base.py", line 1272, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/base.py", line 712, in checkout
    rec = pool._do_get()
          ^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
    with util.safe_reraise():
         ^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 121, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
    return self._create_connection()
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/base.py", line 389, in _create_connection
    return _ConnectionRecord(self)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/base.py", line 674, in __init__
    self.__connect()
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/base.py", line 900, in __connect
    with util.safe_reraise():
         ^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/util/langhelpers.py", line 121, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/pool/base.py", line 896, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/engine/create.py", line 667, in connect
    return dialect.connect(*cargs_tup, **cparams)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/engine/default.py", line 630, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py", line 955, in connect
    await_only(creator_fn(*arg, **kw)),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 132, in await_only
    return current.parent.switch(awaitable)  # type: ignore[no-any-return,attr-defined] # noqa: E501
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/sqlalchemy/util/_concurrency_py3k.py", line 196, in greenlet_spawn
    value = await result
            ^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/asyncpg/connection.py", line 2443, in connect
    return await connect_utils._connect(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/asyncpg/connect_utils.py", line 1249, in _connect
    raise last_error or exceptions.TargetServerAttributeNotMatched(
  File "/opt/app-root/lib64/python3.12/site-packages/asyncpg/connect_utils.py", line 1218, in _connect
    conn = await _connect_addr(
           ^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/asyncpg/connect_utils.py", line 1054, in _connect_addr
    return await __connect_addr(params, True, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/asyncpg/connect_utils.py", line 1099, in __connect_addr
    tr, pr = await connector
             ^^^^^^^^^^^^^^^
  File "/opt/app-root/lib64/python3.12/site-packages/asyncpg/connect_utils.py", line 969, in _create_ssl_connection
    tr, pr = await loop.create_connection(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/base_events.py", line 1083, in create_connection
    infos = await self._ensure_resolved(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/base_events.py", line 1466, in _ensure_resolved
    return await loop.getaddrinfo(host, port, family=family, type=type,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/base_events.py", line 905, in getaddrinfo
    return await self.run_in_executor(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/concurrent/futures/thread.py", line 59, in run
    result = self.fn(*self.args, **self.kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/socket.py", line 978, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
socket.gaierror: [Errno -2] Name or service not known
```

### Expected behavior

The SQL Postgres backend should connect successfully, similar to how `kv_postgres` handles the same credentials with special characters.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `fc8fb082d431a8f89d8b4fb788d5bf7515558a3a`.  There
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
{"case_id": "ogx_ai_ogx__5936__fc8fb08",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
