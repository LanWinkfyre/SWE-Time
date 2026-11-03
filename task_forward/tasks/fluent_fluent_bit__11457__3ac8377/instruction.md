# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
`in_tail`: Expose Metrics to Track Skipped Long Lines

**Is your feature request related to a problem? Please describe.**

When using the [Tail Plugin](https://docs.fluentbit.io/manual/data-pipeline/inputs/tail) with `skipping_long_lines: true`, there is limited visibility into how many lines are being skipped. Currently, Fluent Bit only logs that long lines were encountered, but does not indicate the count or timing of when these skips occur. This makes it difficult to diagnose whether data loss is happening and to what extent.

> [!NOTE]
> There is a similar closed issue, but it did not result in the creation of a new metric specifically for long lines.
> - https://github.com/fluent/fluent-bit/issues/2674

**Describe the solution you'd like**

Add a Counter metric to the Tail plugin that exposes the total count of lines skipped due to the `skipping_long_lines: true` parameter.

There is an existing metric that detects truncated long lines when `truncate_long_lines: true` is configured.

```python
# HELP fluentbit_input_long_line_truncated_total Total number of truncated occurences for long lines
# TYPE fluentbit_input_long_line_truncated_total counter
fluentbit_input_long_line_truncated_total{name="my_tail_input"} 20
```

The format of the existing metrics can be used for the new desired metric, which would look like:

```python
# HELP fluentbit_input_long_line_skipped_total Total number of skipped occurrences for long lines
# TYPE fluentbit_input_long_line_skipped_total counter
fluentbit_input_long_line_skipped_total{name="my_tail_input", file="/var/log/large-log.log", offset=1024} 20
```

Labels descriptions:
- `name`: The plugin identification defined by the `alias` parameter.
- `file`: Monitored file.
- `offset`: Offset position of the byte location in a file where a long line was detected.

**Describe alternatives you've considered**

The only existing log showing skipped long lines cases indicates that a specified monitored file had long lines, and this log message is printed only once.

```log
[2026/02/12 15:18:39.509875417] [ warn] [input:tail:my_tail_input] file=/var/log/large-log.log have long lines. Skipping long lines.
```

As an alternative, create a new [Tail Plugin](https://docs.fluentbit.io/manual/data-pipeline/inputs/tail) parameter named `print_when_skipped_long_lines: true|false` that, when set to `true`, logs each occurrence of a skipped long line, including the monitored file path in the log message.

```log
[2026/02/12 15:18:39.509875417] [ warn] [input:tail:my_tail_input] file=/var/log/large-log.log read line exceeds the value defined in the buffer_max_size, skipping long line.
[2026/02/12 15:18:40.509875407] [ warn] [input:tail:my_tail_input] file=/var/log/large-log.log read line exceeds the value defined in the buffer_max_size, skipping long line.
[2026/02/12 15:41:01.509875000] [ warn] [input:tail:my_tail_input] file=/var/log/large-log.log read line exceeds the value defined in the buffer_max_size, skipping long line.
```

**Additional context**

Having visibility into skipped lines is critical for monitoring data pipelines. This information helps identify configuration issues, validate that expected data is reaching downstream systems, and troubleshoot unexpected data loss in production environments.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3ac837796800ee6aa4fe43b396487d57b9348da8`.  There
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
{"case_id": "fluent_fluent_bit__11457__3ac8377",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
