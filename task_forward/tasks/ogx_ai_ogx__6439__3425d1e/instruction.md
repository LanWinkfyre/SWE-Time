# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Prompts API raises raw ValueError for not-found, breaking HTTP keep-alive on follow-up requests

### System Info

OGX: 1.2.2
Client: AsyncOgxClient / httpx with HTTP/1.1 keep-alive enabled (default)

### Information

- [ ] The official example scripts
- [x] My own modified scripts

### 🐛 Describe the bug

The prompts implementation in ogx/core/prompts/prompts.py raises raw ValueError for not-found cases (e.g. get_prompt, list_prompt_versions, set_default_version). Other OGX APIs use typed ResourceNotFoundError subclasses (ConversationNotFoundError, ConnectorNotFoundError, ModelNotFoundError, etc.) from ogx_api/common/errors.py.

ValueError is not registered among the specific FastAPI exception handlers in ogx/core/server/server.py. Only ResourceNotFoundError, ConflictError, BadRequestError, and similar typed exceptions are. OGX documents that those handlers exist to avoid connection resets on handled errors.

When multiple prompts requests run sequentially on the same HTTP connection, a prior prompts error handled via the generic ValueError/Exception path can leave the keep-alive socket in a bad state. The next request on that connection fails at the transport layer instead of returning a normal HTTP error.

Observed instead of expected:

Isolated call: GET /v1/prompts/{missing_id} → HTTP 400 with error body (works)
After a prior prompts error on the same connection: next GET/PUT for a missing prompt → client-side httpx.ReadError / ApiException(status=0), not an HTTP response
A later call on a fresh connection may still succeed

### Error logs

```bash
PMPT=pmpt_ffffffffffffffffffffffffffffffffffffffffffffffff

curl -v --http1.1 \
  -H "Authorization: Bearer xyzzy" \
  "http://localhost:8321/v1/prompts/${PMPT}" \
  "http://localhost:8321/v1/prompts/${PMPT}"

* Host localhost:8321 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:8321...
* Established connection to localhost (::1 port 8321) from ::1 port 37046 
* using HTTP/1.x
> GET /v1/prompts/pmpt_ffffffffffffffffffffffffffffffffffffffffffffffff HTTP/1.1
> Host: localhost:8321
> User-Agent: curl/8.18.0
> Accept: */*
> Authorization: Bearer xyzzy
> 
* Request completely sent off
< HTTP/1.1 400 Bad Request
< date: Thu, 27 Aug 2026 06:50:48 GMT
< server: uvicorn
< content-length: 102
< content-type: application/json
< 
* Connection #0 to host localhost:8321 left intact
{"error":{"message":"Prompt pmpt_ffffffffffffffffffffffffffffffffffffffffffffffff:default not found"}}* Reusing existing http: connection with host localhost
> GET /v1/prompts/pmpt_ffffffffffffffffffffffffffffffffffffffffffffffff HTTP/1.1
> Host: localhost:8321
> User-Agent: curl/8.18.0
> Accept: */*
> Authorization: Bearer xyzzy
> 
* Request completely sent off
* Recv failure: Connection reset by peer
* Connection died, retrying a fresh connect (retry count: 1)
* shutting down connection #0
* Issue another request to this URL: 'http://localhost:8321/v1/prompts/pmpt_ffffffffffffffffffffffffffffffffffffffffffffffff'
* Hostname localhost was found in DNS cache
*   Trying [::1]:8321...
* Established connection to localhost (::1 port 8321) from ::1 port 37056 
* using HTTP/1.x
> GET /v1/prompts/pmpt_ffffffffffffffffffffffffffffffffffffffffffffffff HTTP/1.1
> Host: localhost:8321
> User-Agent: curl/8.18.0
> Accept: */*
> Authorization: Bearer xyzzy
> 
* Request completely sent off
< HTTP/1.1 400 Bad Request
< date: Thu, 27 Aug 2026 06:50:49 GMT
< server: uvicorn
< content-length: 102
< content-type: application/json
< 
* Connection #1 to host localhost:8321 left intact
{"error":{"message":"Prompt pmpt_ffffffffffffffffffffffffffffffffffffffffffffffff:default not found"}}
```

### Expected behavior

Prompts not-found paths should raise a dedicated exception inheriting from ResourceNotFoundError, consistent with other OGX APIs. For example:

```python
class PromptNotFoundError(ResourceNotFoundError):
    def __init__(self, prompt_id: str) -> None:
        super().__init__(prompt_id, resource_type="Prompt", client_command="prompts.list")
```
Use PromptNotFoundError (or ResourceNotFoundError directly) in ogx/core/prompts/prompts.py for missing prompt / missing version cases. Validation errors (e.g. invalid version) should use InvalidParameterError, as conversations does.

This ensures:

Errors go through the registered ResourceNotFoundError handler in server.py
HTTP 404 is returned for not-found prompts
Sequential requests on a reused keep-alive connection do not fail with transport errors after a prior handled prompts error
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3425d1e623ebb6b738cad26d75d6a5b1583b1a20`.  There
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
{"case_id": "ogx_ai_ogx__6439__3425d1e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
