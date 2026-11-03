# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Vertex AI tool follow-up 400: service_tier="standard" is not a valid Vertex proto value

### System Info

ogx: 1.3.0
google-genai: 2.16.0

Provider: remote::vertexai (`VertexAIInferenceAdapter`), Gemini 3.x (e.g. publishers/google/models/gemini-3.5-flash).

### Information

- [ ] The official example scripts
- [x] My own modified scripts

### 🐛 Describe the bug

Reproduced with OGX Responses (`inline::builtin`) → Vertex responses, with any tool that causes a second model turn (function / MCP / file_search).

Multi-turn Responses inference on Vertex succeeds on the first `generateContent` and fails on the second (tool follow-up) with HTTP 400:

Invalid value at 'service_tier' (type.googleapis.com/google.cloud.aiplatform.v1beta1.ServiceTier), "standard"

Observed: turn 1 omits service_tier and Vertex accepts the request. After the model returns a tool call, OGX sets OpenAI service_tier="default" because Vertex returned no tier, then the Vertex adapter maps that to "standard" and sends it in the JSON body. Vertex’s protobuf enum rejects that lowercase string.

Expected: later turns behave like turn 1 (omit the field, or send a Vertex-valid encoding). "standard" is not a legal Vertex body value; omitting the field already means standard capacity.

**Where**

`ogx.providers.inline.responses.builtin.responses.streaming` — after `completion_result_data.service_tier is None`, sets `self.service_tier = "default"` for the OpenAI response, then copies it into the next `OpenAIChatCompletionRequestWithExtraBody.service_tier`.
`VertexAIInferenceAdapter._convert_service_tier` — maps "default" → "standard" for `GenerateContentConfig`.

Single-turn (no tools) never hits this.

**Suggested fix**

Do not feed a synthetic response `service_tier` into later chat-completion requests; keep request tier as the client sent (None / auto).
In the Vertex adapter, treat None / auto / default as omit. Do not put "standard" / "flex" / "priority" in the Vertex body; Vertex currently uses headers for flex/priority if those must be supported.

### Error logs

```bash
ERROR    {'category': 'agents::builtin', 'error_type': 'ClientError', 'exc_info': ClientError('400 Bad Request.         
         {\'message\': \'{\\n  "error": {\\n    "code": 400,\\n    "message": "Invalid value at \\\'service_tier\\\'    
         (type.googleapis.com/google.cloud.aiplatform.v1beta1.ServiceTier), \\\\"standard\\\\"",\\n    "status":        
         "INVALID_ARGUMENT",\\n    "details": [\\n      {\\n        "@type":                                            
         "type.googleapis.com/google.rpc.BadRequest",\\n        "fieldViolations": [\\n          {\\n                   
         "field": "service_tier",\\n            "description": "Invalid value at \\\'service_tier\\\'                   
         (type.googleapis.com/google.cloud.aiplatform.v1beta1.ServiceTier), \\\\"standard\\\\""\\n          }\\n        
         ]\\n      }\\n    ]\\n  }\\n}\\n\', \'status\': \'Bad Request\'}'), 'event': 'Unexpected error during response 
         generation', 'level': 'error', 'logger': 'ogx.providers.inline.responses.builtin.responses.streaming',         
         'timestamp': '2026-08-19T12:23:21.777810Z'}                                                                    
         ╭───────────────────────────────────── Traceback (most recent call last) ─────────────────────────────────────╮
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/ogx/providers/inline/respons │
         │ es/builtin/responses/streaming.py:597 in create_response                                                    │
         │                                                                                                             │
         │    594 │   │   │   │                                                                                        │
         │    595 │   │   │   │   # Process streaming chunks and build complete response                               │
         │    596 │   │   │   │   completion_result_data = None                                                        │
         │ ❱  597 │   │   │   │   async for stream_event_or_result in                                                  │
         │        self._process_streaming_chunks(completion_result, output_messages):                                  │
         │    598 │   │   │   │   │   if isinstance(stream_event_or_result, ChatCompletionResult):                     │
         │    599 │   │   │   │   │   │   completion_result_data = stream_event_or_result                              │
         │    600 │   │   │   │   │   else:                                                                            │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/ogx/providers/inline/respons │
         │ es/builtin/responses/streaming.py:1113 in _process_streaming_chunks                                         │
         │                                                                                                             │
         │   1110 │   │   # output_item.done (which clean the fully accumulated text once streaming ends).             │
         │   1111 │   │   citation_cleaner = StreamingCitationCleaner(self.citation_files)                             │
         │   1112 │   │                                                                                                │
         │ ❱ 1113 │   │   async for raw_chunk in completion_result:                                                    │
         │   1114 │   │   │   # Providers returning OpenAIChatCompletionChunkWithReasoning wrap                        │
         │   1115 │   │   │   # the chunk with a typed reasoning_content field. Unwrap here.                           │
         │   1116 │   │   │   if isinstance(raw_chunk, OpenAIChatCompletionChunkWithReasoning):                        │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/ogx/core/routers/inference.p │
         │ y:456 in stream_tokens_and_compute_metrics_openai_chat                                                      │
         │                                                                                                             │
         │   453 │   │   status = "success"                                                                            │
         │   454 │   │                                                                                                 │
         │   455 │   │   try:                                                                                          │
         │ ❱ 456 │   │   │   async for chunk in response:                                                              │
         │   457 │   │   │   │   # Skip None chunks                                                                    │
         │   458 │   │   │   │   if chunk is None:                                                                     │
         │   459 │   │   │   │   │   continue                                                                          │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/ogx/providers/remote/inferen │
         │ ce/vertexai/vertexai.py:627 in _iter                                                                        │
         │                                                                                                             │
         │   624 │   │   async def _iter() -> AsyncIterator[OpenAIChatCompletionChunk]:                                │
         │   625 │   │   │   is_first_chunk = True                                                                     │
         │   626 │   │   │   last_chunk: Any = None                                                                    │
         │ ❱ 627 │   │   │   async for chunk in stream:                                                                │
         │   628 │   │   │   │   yield converters.convert_gemini_stream_chunk_to_openai(                               │
         │   629 │   │   │   │   │   chunk=chunk,                                                                      │
         │   630 │   │   │   │   │   model=model,                                                                      │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/sentry_sdk/integrations/goog │
         │ le_genai/__init__.py:189 in new_async_iterator                                                              │
         │                                                                                                             │
         │   186 │   │   │   async def new_async_iterator() -> "AsyncIterator[Any]":                                   │
         │   187 │   │   │   │   chunks: "List[Any]" = []                                                              │
         │   188 │   │   │   │   try:                                                                                  │
         │ ❱ 189 │   │   │   │   │   async for chunk in stream:                                                        │
         │   190 │   │   │   │   │   │   chunks.append(chunk)                                                          │
         │   191 │   │   │   │   │   │   yield chunk                                                                   │
         │   192 │   │   │   │   except Exception as exc:                                                              │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/google/genai/models.py:9022  │
         │ in stream_generator                                                                                         │
         │                                                                                                             │
         │   9019 │   │   │   │   ' list.',                                                                            │
         │   9020 │   │   │   │   indices_str,                                                                         │
         │   9021 │   │   │   )                                                                                        │
         │ ❱ 9022 │   │     response = await self._generate_content_stream(                                            │
         │   9023 │   │   │     model=model, contents=contents, config=final_parsed_config                             │
         │   9024 │   │     )                                                                                          │
         │   9025 │   │     async for chunk in response:  # type: ignore[attr-defined]                                 │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/google/genai/models.py:7361  │
         │ in _generate_content_stream                                                                                 │
         │                                                                                                             │
         │   7358 │   │     ' methods.'                                                                                │
         │   7359 │     )                                                                                              │
         │   7360 │                                                                                                    │
         │ ❱ 7361 │   response_stream = await self._api_client.async_request_streamed(                                 │
         │   7362 │   │   'post', path, request_dict, http_options                                                     │
         │   7363 │   )                                                                                                │
         │   7364                                                                                                      │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/google/genai/_api_client.py: │
         │ 1771 in async_request_streamed                                                                              │
         │                                                                                                             │
         │   1768 │   │   http_method, path, request_dict, http_options                                                │
         │   1769 │   )                                                                                                │
         │   1770 │                                                                                                    │
         │ ❱ 1771 │   response = await self._async_request(                                                            │
         │   1772 │   │   http_request=http_request, http_options=http_options, stream=True                            │
         │   1773 │   )                                                                                                │
         │   1774                                                                                                      │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/google/genai/_api_client.py: │
         │ 1687 in _async_request                                                                                      │
         │                                                                                                             │
         │   1684 │   │   retry_kwargs = retry_args(parameter_model.retry_options)                                     │
         │   1685 │   │   retry = tenacity.AsyncRetrying(**retry_kwargs)                                               │
         │   1686 │   │   return await retry(self._async_request_once, http_request, stream)  # type:                  │
         │        ignore[no-any-return]                                                                                │
         │ ❱ 1687 │   return await self._async_retry(  # type: ignore[no-any-return]                                   │
         │   1688 │   │   self._async_request_once, http_request, stream                                               │
         │   1689 │   )                                                                                                │
         │   1690                                                                                                      │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/tenacity/asyncio/__init__.py │
         │ :112 in __call__                                                                                            │
         │                                                                                                             │
         │   109 │   │   retry_state = RetryCallState(retry_object=self, fn=fn, args=args, kwargs=kwargs)              │
         │   110 │   │   is_async = _utils.is_coroutine_callable(fn)                                                   │
         │   111 │   │   while True:                                                                                   │
         │ ❱ 112 │   │   │   do = await self.iter(retry_state=retry_state)                                             │
         │   113 │   │   │   if isinstance(do, DoAttempt):                                                             │
         │   114 │   │   │   │   try:                                                                                  │
         │   115 │   │   │   │   │   if is_async:                                                                      │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/tenacity/asyncio/__init__.py │
         │ :157 in iter                                                                                                │
         │                                                                                                             │
         │   154 │   │   self._begin_iter(retry_state)                                                                 │
         │   155 │   │   result = None                                                                                 │
         │   156 │   │   for action in self.iter_state.actions:                                                        │
         │ ❱ 157 │   │   │   result = await action(retry_state)                                                        │
         │   158 │   │   return result                                                                                 │
         │   159 │                                                                                                     │
         │   160 │   def __iter__(self) -> t.Generator[AttemptManager, None, None]:                                    │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/tenacity/_utils.py:111 in    │
         │ inner                                                                                                       │
         │                                                                                                             │
         │   108 │   │   return call                                                                                   │
         │   109 │                                                                                                     │
         │   110 │   async def inner(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:                           │
         │ ❱ 111 │   │   return call(*args, **kwargs)                                                                  │
         │   112 │                                                                                                     │
         │   113 │   return inner                                                                                      │
         │   114                                                                                                       │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/tenacity/__init__.py:413 in  │
         │ exc_check                                                                                                   │
         │                                                                                                             │
         │   410 │   │   │   │   fut = t.cast(Future, rs.outcome)                                                      │
         │   411 │   │   │   │   retry_exc = self.retry_error_cls(fut)                                                 │
         │   412 │   │   │   │   if self.reraise:                                                                      │
         │ ❱ 413 │   │   │   │   │   raise retry_exc.reraise()                                                         │
         │   414 │   │   │   │   raise retry_exc from fut.exception()                                                  │
         │   415 │   │   │                                                                                             │
         │   416 │   │   │   self._add_action_func(exc_check)                                                          │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/tenacity/__init__.py:184 in  │
         │ reraise                                                                                                     │
         │                                                                                                             │
         │   181 │                                                                                                     │
         │   182 │   def reraise(self) -> t.NoReturn:                                                                  │
         │   183 │   │   if self.last_attempt.failed:                                                                  │
         │ ❱ 184 │   │   │   raise self.last_attempt.result()                                                          │
         │   185 │   │   raise self                                                                                    │
         │   186 │                                                                                                     │
         │   187 │   def __str__(self) -> str:                                                                         │
         │                                                                                                             │
         │ /home/asimurka/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/concurrent/futures/_b │
         │ ase.py:449 in result                                                                                        │
         │                                                                                                             │
         │   446 │   │   │   │   if self._state in [CANCELLED, CANCELLED_AND_NOTIFIED]:                                │
         │   447 │   │   │   │   │   raise CancelledError()                                                            │
         │   448 │   │   │   │   elif self._state == FINISHED:                                                         │
         │ ❱ 449 │   │   │   │   │   return self.__get_result()                                                        │
         │   450 │   │   │   │                                                                                         │
         │   451 │   │   │   │   self._condition.wait(timeout)                                                         │
         │   452                                                                                                       │
         │                                                                                                             │
         │ /home/asimurka/.local/share/uv/python/cpython-3.12.11-linux-x86_64-gnu/lib/python3.12/concurrent/futures/_b │
         │ ase.py:401 in __get_result                                                                                  │
         │                                                                                                             │
         │   398 │   def __get_result(self):                                                                           │
         │   399 │   │   if self._exception:                                                                           │
         │   400 │   │   │   try:                                                                                      │
         │ ❱ 401 │   │   │   │   raise self._exception                                                                 │
         │   402 │   │   │   finally:                                                                                  │
         │   403 │   │   │   │   # Break a reference cycle with the exception in self._exception                       │
         │   404 │   │   │   │   self = None                                                                           │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/tenacity/asyncio/__init__.py │
         │ :116 in __call__                                                                                            │
         │                                                                                                             │
         │   113 │   │   │   if isinstance(do, DoAttempt):                                                             │
         │   114 │   │   │   │   try:                                                                                  │
         │   115 │   │   │   │   │   if is_async:                                                                      │
         │ ❱ 116 │   │   │   │   │   │   result = await fn(*args, **kwargs)                                            │
         │   117 │   │   │   │   │   else:                                                                             │
         │   118 │   │   │   │   │   │   result = fn(*args, **kwargs)                                                  │
         │   119 │   │   │   │   except BaseException:  # noqa: B902                                                   │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/google/genai/_api_client.py: │
         │ 1569 in _async_request_once                                                                                 │
         │                                                                                                             │
         │   1566 │   │   │     **self._async_client_session_request_args,                                             │
         │   1567 │   │     )                                                                                          │
         │   1568 │   │                                                                                                │
         │ ❱ 1569 │   │   await errors.APIError.raise_for_async_response(response)                                     │
         │   1570 │   │   if hasattr(response, '_response'):                                                           │
         │   1571 │   │     # Extract the underlying aiohttp.ClientResponse from the                                   │
         │   1572 │   │     # AsyncAuthorizedSession Response.                                                         │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/google/genai/errors.py:247   │
         │ in raise_for_async_response                                                                                 │
         │                                                                                                             │
         │   244 │     except ImportError:                                                                             │
         │   245 │   │   raise ValueError(f'Unsupported response type: {type(response)}')                              │
         │   246 │                                                                                                     │
         │ ❱ 247 │   await cls.raise_error_async(status_code, response_json, response)                                 │
         │   248                                                                                                       │
         │   249   @classmethod                                                                                        │
         │   250   async def raise_error_async(                                                                        │
         │                                                                                                             │
         │ /home/asimurka/Development/lightspeed-stack/.venv/lib/python3.12/site-packages/google/genai/errors.py:269   │
         │ in raise_error_async                                                                                        │
         │                                                                                                             │
         │   266 │     APIError: For other error status codes.                                                         │
         │   267 │   """                                                                                               │
         │   268 │   if 400 <= status_code < 500:                                                                      │
         │ ❱ 269 │     raise ClientError(status_code, response_json, response)                                         │
         │   270 │   elif 500 <= status_code < 600:                                                                    │
         │   271 │     raise ServerError(status_code, response_json, response)                                         │
         │   272 │   else:                                                                                             │
         ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
         ClientError: 400 Bad Request. {'message': '{\n  "error": {\n    "code": 400,\n    "message": "Invalid value at 
         \'service_tier\' (type.googleapis.com/google.cloud.aiplatform.v1beta1.ServiceTier), \\"standard\\"",\n         
         "status": "INVALID_ARGUMENT",\n    "details": [\n      {\n        "@type":                                     
         "type.googleapis.com/google.rpc.BadRequest",\n        "fieldViolations": [\n          {\n            "field":  
         "service_tier",\n            "description": "Invalid value at \'service_tier\'                                 
         (type.googleapis.com/google.cloud.aiplatform.v1beta1.ServiceTier), \\"standard\\""\n          }\n        ]\n   
         }\n    ]\n  }\n}\n', 'status': 'Bad Request'}                                                                  
ERROR    2026-08-19T12:23:23.055745Z  ogx.providers.inline.responses.builtin.responses.openai_responses:1010 response   
         creation failed   category=openai_responses error_code=server_error error_message=An unexpected error occurred 
         while generating the response. model=google-vertex/publishers/google/models/gemini-3.5-flash                   
         response_id=resp_45337c0e-568e-416d-ba06-5e674fe82f7f   
```

### Expected behavior

Later turns behave like turn 1 (omit the field, or send a Vertex-valid encoding). "standard" is not a legal Vertex body value; omitting the field already means standard capacity.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ba58eb12b57f85e570b237291278c14174e682b7`.  There
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
{"case_id": "ogx_ai_ogx__6418__ba58eb1",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
