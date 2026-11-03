# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Limit OpenTelemetry metrics per request to support AWS's OpenTelemetry

**Is your feature request related to a problem? Please describe.**

If using the OpenTelemetry output to send metrics to AWS CloudWatch's OTLP endpoint, AWS's implementation has a [hard limit of 1,000 datapoints per request](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-OTLPEndpoint.html#:~:text=Maximum%20datapoint%20count). This means that if you generate a lot of datapoints (eg, using the `process_exporter_metrics` input on a host with a lot of processes), sending these metrics to AWS via OpenTelemetry can fail. This will end up generating an error and a response like this back from AWS:

```
[error] [output:opentelemetry:opentelemetry.1] monitoring.us-east-1.amazonaws.com:443, HTTP status=400
Maximum number of datapoints per request exceeded: 1000.
```

**Describe the solution you'd like**

The OpenTelemetry output seems to support some options to restrict the amount of data sent in one request, but only for logs (not metrics):

> - `batch_size`: Set the maximum number of log records to be flushed at a time.
> - `logs_max_resources`: Set the maximum number of OTLP log resources per export request (0 disables the limit).

Would some similar options be possible for metrics, so that the requests sent to AWS could be batched and always be under the 1,000 datapoint limit?

**Describe alternatives you've considered**

The only real alternative I've found is trying to limit the number of datapoints collected at a time, but this may not always be feasible.

Alternatively, I haven't tested this, but I believe the OpenTelemetry Collector could support this via their [Batch Processor](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md) (since it looks like that supports batching on metrics too), but I'd prefer to keep using Fluent Bit for my current purposes.

**Additional context**

AWS's OpenTelemetry support is [fairly new](https://aws.amazon.com/about-aws/whats-new/2026/04/amazon-cloudwatch-opentelemetry-metrics/), and I realize this is a limitation with their implementation, but it would be great if Fluent Bit's OpenTelemetry output could better support this. Thanks!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `98f3bdeb9ad4af5bcb03a7ae1872e694b207f274`.  There
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
{"case_id": "fluent_fluent_bit__12247__98f3bde",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
