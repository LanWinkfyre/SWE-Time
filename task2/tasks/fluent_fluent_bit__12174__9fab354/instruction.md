# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_http: HTTP/1.1 empty header value can leave keep-alive request without response

The `in_http` input can leave an HTTP/1.1 keep-alive request without a
response when the request contains a syntactically valid generic header with
an empty field-value. This remains reproducible by source inspection in
Fluent Bit v5.0.0, and the relevant code is unchanged on current `master`.

## Summary

An HTTP/1.1 request containing a syntactically valid generic header with an
empty field-value can remain open without receiving an HTTP response when it
is sent to the `in_http` input. The request is not delivered to the input
callback.

The behavior has two layers:

1. The vendored Monkey HTTP parser rejects an empty field-value.
2. Fluent Bit's HTTP/1 server wrapper ignores that parser error, retains the
   request buffer, resets the parser, and reports success without queuing a
   request or response.

## Minimal reproducer

Run Fluent Bit with the `in_http` input on port 9880 and a normal output, then
send this raw HTTP/1.1 request:

```http
POST /empty-header HTTP/1.1
Host: localhost
Content-Type: application/json
Content-Length: 2
X-Empty:

{}
```

The `X-Empty:` line has no octets after the colon. The same applies to
`X-Empty: ` with one or more SP characters after the colon. 

## Expected behavior

An empty generic HTTP field-value should not cause the connection to wait
indefinitely. The request should receive the configured `in_http` success
response (201 by default), with the empty header either preserved or
explicitly ignored according to documented behavior.

If Fluent Bit chooses to reject the request, it should return a deterministic
4xx response and close the connection rather than silently retaining the
invalid buffer.

RFC 9110 defines the generic field-value as `*field-content`, so an empty
generic field-value is syntactically permitted, while individual fields may
impose stricter semantic requirements:
https://www.rfc-editor.org/rfc/rfc9110.html#section-5.5

## Actual behavior

With HTTP/1.1 keep-alive, the client receives no response and waits until its
own timeout. No input callback is invoked. Further reads reparse the same
buffer because the request is not evicted.

## Source evidence

`in_http` initializes the generic embedded HTTP server with the HTTP/1 server
callback:
https://github.com/fluent/fluent-bit/blob/master/plugins/in_http/http.c#L74-L90

The Monkey parser enters `MK_ST_HEADER_VALUE` after the colon. It returns
`MK_HTTP_PARSER_ERROR` when it reaches CR or LF before finding a non-space
character:
https://github.com/fluent/fluent-bit/blob/master/lib/monkey/mk_server/mk_http_parser.c#L996-L1006

When a value start was never found, the header-finalization path also rejects
`field_len() <= 0`:
https://github.com/fluent/fluent-bit/blob/master/lib/monkey/mk_server/mk_http_parser.c#L1009-L1015

The HTTP/1 session ingest function handles only `MK_HTTP_PARSER_OK` and
`MK_HTTP_PARSER_PENDING`. `MK_HTTP_PARSER_ERROR` falls through, the parser is
reset, and `HTTP_SERVER_SUCCESS` is returned:
https://github.com/fluent/fluent-bit/blob/master/src/http_server/flb_http_server_http1.c#L539-L573

The incoming buffer is evicted only after a successful parse:
https://github.com/fluent/fluent-bit/blob/master/src/http_server/flb_http_server_http1.c#L61-L99

The current `master` parser file is byte-for-byte identical to the v5.0.0
parser file. The relevant HTTP/1 ingest logic is also unchanged between
v5.0.0 and current `master`; the later differences in those files are
unrelated changes.

## Affected versions

- Observed: Fluent Bit v5.0.0
- Source-confirmed: current `master`
- The same parser behavior is present in the v5.0.9 source snapshot.

## Suggested fix boundaries

1. Make the HTTP/1 parser accept zero-length field-values after optional SP
   and HTAB, and complete the header normally.
2. Independently handle `MK_HTTP_PARSER_ERROR` in
   `flb_http1_server_session_ingest()`. Do not return success while retaining
   the unconsumed invalid request. Return a 4xx response and close the
   connection, or close it deterministically if no response can be generated.
3. Add a regression test using raw HTTP/1.1 input for both `X-Empty:` and
   `X-Empty: `, asserting a prompt response and no indefinite connection.

After parser acceptance, `http1_session_process_request()` currently copies
only headers with `header->val.len > 0`. That would allow processing while
silently omitting empty headers; if that is intentional, it should be
documented and tested. If empty headers must remain visible to the input
callback, that condition should be revisited.

## Related issue status

This issue supersedes the stale discussion in #8167, which reported the same
empty-header parser condition but was closed automatically without a
technical resolution. Related issues #9391 and #10071 concern
different OpenTelemetry span/output problems and do not fix this HTTP/1
parser path.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9fab3541b6c9631b7032beff22774e5f1bee66e8`.  There
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
{"case_id": "fluent_fluent_bit__12174__9fab354",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
