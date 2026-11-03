# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
bug(tests): pytest 9.0+ compatibility error in pytest_ignore_collect hook signature

### System Info

- Python version: 3.12
- Pytest version: 9.1.1 (pytest >= 9.0.0)

### Information

- [x] The official example scripts

### 🐛 Describe the bug

Running integration tests (`pytest tests/integration/`) with Pytest 9.0+ fails at startup with `pluggy.PluginValidationError` due to `pytest_ignore_collect` in `tests/integration/conftest.py`.

In Pytest 9.0+, the legacy `path` parameter was removed from the `pytest_ignore_collect` hook definition in favor of `collection_path: Path`. Because `tests/integration/conftest.py` declares:

```python
def pytest_ignore_collect(path: str, config: pytest.Config) -> bool:
```

Pytest fails hook validation during test discovery and exits before running any tests.

#### Proposed Fix
Update `pytest_ignore_collect` in `tests/integration/conftest.py` to accept `collection_path: Path` (or support both `collection_path` and fallback `path`):

```python
def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool:
    """Skip collecting paths outside the selected suite roots for speed."""
    suite = config.getoption("--suite")
    if not suite:
        return False

    sobj = SUITE_DEFINITIONS.get(suite)
    roots: list[str] = sobj.get("roots", []) if isinstance(sobj, dict) else getattr(sobj, "roots", [])
    if not roots:
        return False

    p = collection_path.resolve()
    ...
```

### Error logs

```
Traceback (most recent call last):
  File ".../pytest/__main__.py", line 9, in <module>
    raise SystemExit(_console_main())
  File ".../_pytest/config/__init__.py", line 870, in consider_conftest
    self.register(conftestmodule, name=registration_name)
  File ".../pluggy/_manager.py", line 343, in _verify_hook
    raise PluginValidationError(
pluggy._manager.PluginValidationError: Plugin '.../tests/integration/conftest.py' for hook 'pytest_ignore_collect'
hookimpl definition: pytest_ignore_collect(path: str, config: _pytest.config.Config) -> bool
Argument(s) {'path'} are declared in the hookimpl but can not be found in the hookspec
```

### Expected behavior

Integration tests run cleanly under Pytest 9.0+.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8b355bfb7528355a9987f9b642c3e2ad48916dd6`.  There
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
{"case_id": "ogx_ai_ogx__6428__8b355bf",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
