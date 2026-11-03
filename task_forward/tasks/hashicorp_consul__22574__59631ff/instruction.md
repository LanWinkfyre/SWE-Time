# Recover the symbolic verification state this change produces

A regression report was filed against `hashicorp/consul`.  The report is quoted verbatim below.

## Report

```
cannot create key-value in "code" mode for version 1.21.4


### Reproduction Steps

* download the latest version 1.21.4
* unzip the file
* run in dev mode `consul agent -dev`
* browse to 127.0.0.1:8500 and try to create a key value

All I get is the spinner continuously rotating as can be seen in the screen shot:

<img width="695" height="512" alt="Image" src="https://github.com/user-attachments/assets/ff993cf2-f65e-490b-84eb-a0217a7edfd5" />

Also on the console, I see the following (probably related):

```
2025-08-14T00:59:52.409+0530 [DEBUG] agent: warning: request content-type is not supported: request-path="/v1/kv/?keys&dc=dc1&separator=%2F"
2025-08-14T00:59:52.409+0530 [DEBUG] agent: warning: response content-type header not explicitly set.: request-path="/v1/kv/?keys&dc=dc1&separator=%2F"
2025-08-14T00:59:54.116+0530 [DEBUG] agent: warning: request content-type is not supported: request-path="/ui/dc1/kv/%7B%7B.ContentPath%7D%7Dassets/chunk.504.6916aef248f167c7ce2b.js"
2025-08-14T00:59:54.116+0530 [DEBUG] agent: warning: response content-type header not explicitly set.: request-path="/ui/dc1/kv/%7B%7B.ContentPath%7D%7Dassets/chunk.504.6916aef248f167c7ce2b.js"
2025-08-14T01:00:03.741+0530 [DEBUG] agent: warning: request content-type is not supported: request-path="/ui/dc1/kv/%7B%7B.ContentPath%7D%7Dassets/chunk.504.6916aef248f167c7ce2b.js"
2025-08-14T01:00:03.741+0530 [DEBUG] agent: warning: response content-type header not explicitly set.: request-path="/ui/dc1/kv/%7B%7B.ContentPath%7D%7Dassets/chunk.504.6916aef248f167c7ce2b.js"
```

NOTE: If I switch **off** "code" mode, I can create the key-value

<img width="134" height="57" alt="Image" src="https://github.com/user-attachments/assets/820fb9b0-e7e7-4526-b291-92f15e9ea89e" />


### Consul Version

1.21.4 in dev mode (`consul agent -dev`)

```
Consul v1.21.4
Revision 59b8b905
Build Date 2025-08-13T12:03:12Z
Protocol 2 spoken by default, understands 2 to 3 (agent will automatically use protocol >2 when speaking to compatible agents)
```

### Browser and Operating system details

Mozilla Firefox on Linux
Vivaldi on Linux
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `59631ffd3671935a5c451e583333e07d99b791ae`.  There
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
{"case_id": "hashicorp_consul__22574__59631ff",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
