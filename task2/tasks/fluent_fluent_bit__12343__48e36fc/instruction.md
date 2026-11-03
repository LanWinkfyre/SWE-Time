# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
out_kafka: hot reload converts infinite shutdown grace to expired timeout

## Bug Report

**Describe the bug**

Thread-safe hot reload can destroy the Kafka producer without waiting for queued records to reach a delivery result.

Fluent Bit gives the old engine context unlimited shutdown time by setting `grace` to `-1`:

```c
if (old_config->ensure_thread_safety_on_hot_reloading) {
    old_config->grace = -1;
}
```

The Kafka output converts the grace period from seconds to milliseconds without preserving that sentinel:

```c
ret = rd_kafka_flush(ctx->kafka.rk, config->grace * 1000);
```

This passes `-1000` to librdkafka. The bundled librdkafka defines exactly `-1` as its infinite timeout:

```c
#define RD_POLL_INFINITE -1
#define RD_POLL_NOWAIT   0
```

It treats any other negative value as a deadline before the current time:

```c
static RD_INLINE rd_ts_t rd_timeout_init0(rd_ts_t now, int timeout_ms) {
        if (timeout_ms == RD_POLL_INFINITE || timeout_ms == RD_POLL_NOWAIT)
                return timeout_ms;

        return now + ((rd_ts_t)timeout_ms * 1000);
}
```

`rd_kafka_flush()` therefore polls once and returns timed out. Fluent Bit then destroys the producer even though librdkafka may still have queued or in-flight records.

**To Reproduce**

Save this configuration as `repro.yaml`. The unavailable broker is intentional. It leaves one message pending for the configured five-second message timeout.

```yaml
service:
  flush: 0.1
  grace: 2
  log_level: debug
  http_server: on
  http_listen: 0.0.0.0
  http_port: 2020
  hot_reload: on
  hot_reload.ensure_thread_safety: on
  hot_reload.timeout: 30

pipeline:
  inputs:
    - name: dummy
      tag: test
      dummy: '{"message":"pending during reload"}'
      samples: 1

  outputs:
    - name: kafka
      match: test
      brokers: 127.0.0.1:9092
      topics: test
      rdkafka.message.timeout.ms: 5000
      rdkafka.api.version.request: false
      rdkafka.broker.version.fallback: 0.8.2.0
```

Create and start a container using the official Fluent Bit 5.1.1 image:

```bash
docker create \
  --name fluent-bit-kafka-grace-repro \
  fluent/fluent-bit:5.1.1 \
  -c /tmp/repro.yaml

docker cp repro.yaml fluent-bit-kafka-grace-repro:/tmp/repro.yaml
docker start fluent-bit-kafka-grace-repro
docker logs -f fluent-bit-kafka-grace-repro
```

Wait until the Kafka output reports that the message was enqueued:

```text
[debug] [output:kafka:kafka.0] enqueued message (66 bytes) for topic 'test'
```

Trigger hot reload from another terminal:

```bash
docker kill --signal HUP fluent-bit-kafka-grace-repro
```

I reproduced the following behavior locally with the unmodified official `fluent/fluent-bit:5.1.1` image:

```text
[2026/08/27 11:07:14.662] [debug] [output:kafka:kafka.0] enqueued message (66 bytes) for topic 'test'
[2026/08/27 11:07:14.793] [ info] [reload] stop everything of the old context
[2026/08/27 11:07:15.561] [ warn] [output:kafka:kafka.0] Failed to force flush: Local: Timed out
[2026/08/27 11:07:15.563] [ info] [reload] start everything
```

The replacement context started approximately 0.8 seconds after shutdown began, before the outstanding message’s five-second timeout.

Cleanup:

```bash
docker stop fluent-bit-kafka-grace-repro
docker rm fluent-bit-kafka-grace-repro
```

**Expected behavior**

Thread-safe hot reload should preserve the infinite grace sentinel and wait until librdkafka resolves the outstanding message before destroying the producer and starting the replacement context.

Finite grace values should continue to be converted from seconds to milliseconds.

**Your Environment**

- Version: Fluent Bit 5.1.1
- Image: `fluent/fluent-bit:5.1.1`
- Output plugin: `kafka`
- Bundled librdkafka: 2.15.0
- Broker: deliberately unavailable localhost endpoint

Related: fluent/fluent-bit#5593
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `48e36fcc76bf947be0375c566fea0d5164b44bbd`.  There
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
{"case_id": "fluent_fluent_bit__12343__48e36fc",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
