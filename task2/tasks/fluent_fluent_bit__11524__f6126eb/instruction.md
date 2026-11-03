# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
Enhancement: Make kinesis_streams MAX_EVENT_SIZE configurable or support >1MB records

**Is your feature request related to a problem? Please describe.**
<!--- A clear and concise description of what the problem is. Ex. I'm always frustrated when [...] -->
The plugin _out_kinesis_streams_ has a hard-coded maximum record size:
- MAX_EVENT_SIZE = 1048556

This causes records larger than 1MB to be discarted with a warning like:
- Discarding record which is larger than max size allowed by Firehose, %s

This behavior limits use cases where larger records are valid (especially since AWS Kinesis Data Streams now supports up to 10MB record sizes when the stream supports “large records”).

According to [AWS’s official announcement](https://aws.amazon.com/pt/blogs/big-data/amazon-kinesis-data-streams-now-supports-10x-larger-record-sizes-simplifying-real-time-data-processing/), Amazon Kinesis Data Streams now supports record sizes up to 10 MiB, a tenfold increase over the previous 1 MiB limit.

**Describe the solution you'd like**
<!--- A clear and concise description of what you want to happen. -->
Please consider the following improvement:

- Make the maximum record size configurable (e.g., via a plugin parameter), so that users can align the plugin behavior with the actual stream configuration and avoid discarding valid records.

**Describe alternatives you've considered**
<!--- A clear and concise description of any alternative solutions or features you've considered. -->
Please consider the following improvement:

- Make the maximum record size bigger, so that users can avoid discarding valid records.

**Additional context**
N/A
<!--- How has this issue affected you? What are you trying to accomplish? -->
<!--- Providing context helps us come up with a solution that is most useful in the real world -->
<!--- Add any other context or screenshots about the feature request here. -->
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f6126ebc3aba26882e8e1f2c20e93f04f6d7489c`.  There
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
{"case_id": "fluent_fluent_bit__11524__f6126eb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
