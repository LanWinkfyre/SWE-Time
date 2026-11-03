# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Add support to Schema Registry consumption

**Is your feature request related to a problem? Please describe.**

Teams that produce schema-aware Kafka payloads (for example Avro or Protobuf with Confluent Schema Registry) often depend on extra components outside Fluent Bit so records match consumer expectations: correct serialized bytes plus Confluent wire framing (including schema id where required).

Fluent Bit’s Kafka output uses librdkafka, which does not implement Schema Registry or registry-driven serialization. There is no built-in way to resolve schemas from a central Schema Registry over HTTP(S), cache them, and emit registry-compatible messages through the same Kafka output users already configure.


**Describe the solution you'd like**

Extend out_kafka with Schema Registry consumption:

HTTP(S) client — Fetch schema metadata from SR by schema id and/or subject + version.
Local cache — Cache schema material and ids; configurable limits and defined behavior on miss, SR errors, and staleness.
Encode + frame — Serialize records to Avro, with Confluent-compatible payloads for librdkafka. Avro-first delivery is acceptable if it reduces risk.
Config — SR base URL, TLS, authentication (should be covered by common http?), and subject rules for value (and optionally key). See [this](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/index.html#subject-name-strategies)

We should evaluate [libserdes](https://github.com/confluentinc/libserdes) (C library for this matter) before implementing this completely in-house.


**Describe alternatives you've considered**

External serialization (sidecar, processor, or custom filter) that talks to Schema Registry and passes opaque bytes to Kafka — adds deployment and operational overheads.
Manual schema and id configuration in Fluent Bit where supported — works for static schemas; not very useful when schemas are owned and versioned centrally in Schema Registry.


**Additional context**

Registry: Confluent Schema Registry; output: Kafka via out_kafka. Only for AVRO
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `117a7271c7a916990ecdad217e6111538a186a36`.  There
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
{"case_id": "fluent_fluent_bit__11737__117a727",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
