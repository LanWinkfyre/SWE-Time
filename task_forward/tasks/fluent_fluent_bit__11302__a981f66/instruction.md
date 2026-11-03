# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Opentelemetry metadata and attributes are lost when wasm filter is used


## Bug Report

**Describe the bug**
OpenTelemetry group attributes and scopes are lost when `opentelemetry` input is used with `wasm` filter. 

**To Reproduce**
Prerequisite: Create and build blank WASM plugin.

```go
//export debugFn
func debugFn(tag *uint8, tagLen uint, timeSec uint32, timeNsec uint32, record *uint8, recordLen uint) *uint8 {
	// some business filtering logic would be added here.
	return record
}
```

**Case A) (Incorrect)** 

Step 1)  Create configuration with `opentelemetry` input and `wasm` filter and start HTTP server.

Configuration:
```yaml
service:
  http_port: 2020

pipeline:
  inputs:
    - name: opentelemetry

  filters:
    - name: wasm
      match: 'v1_logs'
      function_name: 'debugFn'
      wasm_path: /fluent-bit/lib/filter/debug.wasm

  outputs:
    - name: stdout
      match: '*'
```

Step 2) Send HTTP request to fluent-bit that contains group attributes and scopes.

```bash
curl --header "Content-Type: application/json" --request POST --data '{"resourceLogs":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"filter-service"}}]},"scopeLogs":[{"scope":{"name":"my.scope"},"logRecords":[{"timeUnixNano":"1660296023390371588","body":{"stringValue":"{\"message\":\"dummy\"}"}}]}]}]}'   http://0.0.0.0:4318/v1/logs
```

Data missing: Output does not contain attributes and resource logs:
```
[2025/12/19 13:48:25.435367475] [ info] [output:stdout:stdout.0] worker #0 started
[0] v1_logs: [[1660296023.1698112429, {"otlp"=>{}}], {"log"=>"{"message":"dummy"}"}]
````


**Case B) (Working)**

Create configuration with `dummy` input processed by `opentelemetry_envelope` and `wasm` filter. 
Use the same dummy's input as was sent in Case A.


```yaml
service:
  http_port: 2020

pipeline:
  inputs:
    - name: dummy
      dummy: |-
        {
          "resourceLogs": [
            {
              "resource": {
                "attributes": [
                  {
                    "key": "service.name",
                    "value": {
                      "stringValue": "filter-service"
                    }
                  }
                ]
              },
              "scopeLogs": [
                {
                  "scope": {
                    "name": "my.scope"
                  },
                  "logRecords": [
                    {
                      "timeUnixNano": "1660296023390371588",
                      "body": {
                        "stringValue": "{\"message\":\"dummy\"}"
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
      tag: 'v1_logs'
      processors:
        logs:
          - name: opentelemetry_envelope

  filters:
    - name: wasm
      match: 'v1_logs'
      function_name: 'debugFn'
      wasm_path: /fluent-bit/lib/filter/debug.wasm
      wasm_heap_size: 256KB
      wasm_stack_size: 256KB

  outputs:
    - name: stdout
      match: '*'
```

Output contains attributes and scopeLogs as expected:
```
[2025/12/19 13:45:28.787731766] [ info] [output:stdout:stdout.0] worker #0 started
[0] v1_logs: [[1766151929.431803891, {}], {"resourceLogs"=>[{"resource"=>{"attributes"=>[{"key"=>"service.name", "value"=>{"stringValue"=>"filter-service"}}]}, "scopeLogs"=>[{"scope"=>{"name"=>"my.scope"}, "logRecords"=>[{"timeUnixNano"=>"1660296023390371588", "body"=>{"stringValue"=>"{"message":"dummy"}"}}]}]}]}]
```

**Case C) (Working)**
Create configuration with `opentelemetry` input and no `wasm` filter and start HTTP server.

```yaml
service:
  http_port: 2020

pipeline:
  inputs:
    - name: opentelemetry

  outputs:
    - name: stdout
      match: '*'
```

Step 2) Send HTTP request to fluent-bit that contains group attributes and scopes.

```bash
curl --header "Content-Type: application/json" --request POST --data '{"resourceLogs":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"filter-service"}}]},"scopeLogs":[{"scope":{"name":"my.scope"},"logRecords":[{"timeUnixNano":"1660296023390371588","body":{"stringValue":"{\"message\":\"dummy\"}"}}]}]}]}'   http://0.0.0.0:4318/v1/logs
```

Output contains group attributes and metadata as expected.
```
[2025/12/19 13:50:30.837814660] [ info] [output:stdout:stdout.0] worker #0 started
GROUP METADATA : 

{"schema"=>"otlp", "resource_id"=>0, "scope_id"=>0}

GROUP ATTRIBUTES : 

{"resource"=>{"attributes"=>{"service.name"=>"filter-service"}}, "scope"=>{"name"=>"my.scope"}}

[0] v1_logs: [[1660296023.1698112429, {"otlp"=>{}}], {"log"=>"{"message":"dummy"}"}]
```

**Expected behavior**
I expected that using `opentelemetry` filter together with `wasm` filter would not not remove group attributes and metadata.

**Screenshots**
![Image](https://github.com/user-attachments/assets/f64c5a94-6d2d-4801-b075-ebc5282f8713)


**Your Environment**
<!--- Include as many relevant details about the environment you experienced the bug in -->
* Version used: v4.2.1

* Configuration: see cases above.
* Environment name and version (e.g. Kubernetes? What version?): Docker running on localhost
* Server type and version: N/A
* Operating System and version: macOS 15.7.3
* Filters and plugins: opentelemetry, wasm, stdout

**Additional context**
Parts of original message are lost but could contain important information.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `a981f6681c4b4efd962f8f4c81307db26fa4b74d`.  There
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
{"case_id": "fluent_fluent_bit__11302__a981f66",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
