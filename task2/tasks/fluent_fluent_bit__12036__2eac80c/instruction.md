# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_splunk: unknown token returns HTTP 401 instead of Splunk's 403 "Invalid token" (code 4)

## Bug Report

**Describe the bug**

The Splunk HEC input plugin (`in_splunk`) answers **every** authentication failure with HTTP `401 Unauthorized` (body `error: unauthorized`).

Real Splunk HEC distinguishes header-format problems from token-value problems, per its documented reply-code table (see https://help.splunk.com/en/splunk-enterprise/get-started/get-data-in/9.4/get-data-with-http-event-collector/troubleshoot-http-event-collector, **Possible error codes** ) :
  
  | Reply code | Internal name | HTTP status | Message |
  |---|---|---|---|
  | 2 | `NoAuthorization`     | **401** | Token is required     |
  | 3 | `InvalidAuthorization`| **401** | Invalid authorization |
  | 4 | `TokenNotFound`       | **403** | Invalid token         |

So when the `Authorization` header is well-formed as `Splunk <token>` but the token value is unknown, Splunk returns **`403` with body `{"text":"Invalid token","code":4}`**, and reserves `401` for missing/malformed headers. `in_splunk` collapses all of these into `401`, diverging from the documented HEC contract and breaking clients that gate on `403`/code 4.


**To Reproduce**

fluent-bit.yml
```yaml
service:
  flush: 1
  log_level: debug

pipeline:
  inputs:
    - name: splunk
      alias: splunk_hec
      listen: 0.0.0.0
      port: 8088
      splunk_token: 11111111-1111-1111-1111-111111111111
      tag: hec

  outputs:
    - name: stdout
      match: '*'
```

Run Fluent Bit:
```shell
docker run --rm -it -p 8088:8088 -v $(pwd)/fluent-bit.yml:/fluent-bit/etc/fluent-bit.yaml fluent/fluent-bit:5.0  -c /fluent-bit/etc/fluent-bit.yaml
```
 
Run these requests:

```shell

URL=http://localhost:8088/services/collector/event

# A) valid token                          -> 200  (OK)
curl -s -w '\n%{http_code}\n' "$URL" \
  -H "Authorization: Splunk 11111111-1111-1111-1111-111111111111" -d '{"event":"x"}'

# B) well-formed header, unknown token     -> 401  (BUG: expected 403 "Invalid token", code 4)
curl -s -w '\n%{http_code}\n' "$URL" \
  -H "Authorization: Splunk 99999999-0000-0000-0000-000000000000" -d '{"event":"x"}'

# C) malformed header (no "Splunk " prefix) -> 401  (correct)
curl -s -w '\n%{http_code}\n' "$URL" \
  -H "Authorization: 11111111-1111-1111-1111-111111111111" -d '{"event":"x"}'

```

Case B, should have returned 403.

**Expected behavior**


Match the documented Splunk HEC contract:
- Header missing → `401`, `{"text":"Token is required","code":2}`
- Header present but not `Splunk <token>` (malformed) → `401`, `{"text":"Invalid authorization","code":3}`
- Header well-formed `Splunk <token>` but value unknown → **`403`, `{"text":"Invalid token","code":4}`**
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2eac80c24939b8f29fa5bab202561b1494e9c70b`.  There
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
{"case_id": "fluent_fluent_bit__12036__2eac80c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
