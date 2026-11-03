# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
[Feature Request] Support for native out-of-band Labels and Namespace mapping in google-chronicle destination plugin

### **Is your feature request related to a problem? Please describe.**
To properly utilize Google SecOps, logs often need to be enriched with custom `Labels` and assigned to a specific SecOps `Namespace`. (In Google SecOps, Namespaces are critical for asset resolution, handling overlapping IP spaces, and multi-tenant isolation). 

Currently, injecting these metadata key-value pairs directly into the raw log payload (e.g., appending them to a Syslog string) frequently breaks default Google SecOps parsers. These out-of-the-box parsers rely on strict regex, grok patterns, or fixed JSON schemas designed strictly around the original raw log format. 

The Google SecOps `unstructuredlogentries:batchCreate` API natively supports `labels` and `namespace` as out-of-band body parameters to solve this exact issue. However, the `google-chronicle` destination plugin currently lacks the configuration keys to map nested Fluent Bit metadata into these specific API fields. This forces users to choose between breaking out-of-the-box SecOps parsers (by mutating the log) or losing critical multi-tenant visibility and accurate asset resolution (by dropping the namespace and labels).

### **Describe the solution you'd like**
Update the `google-chronicle` destination plugin to support out-of-band metadata injection. 

For the `Namespace`, we request a configuration key that supports standard Fluent Bit Record Accessors to dynamically extract the value. For `Labels`, we request a configuration format identical to how `Header` is defined in the standard Fluent Bit `http` output plugin, allowing for both static values and dynamic record accessor mappings.

**Proposed Plugin Additions (YAML Format):**
```yaml
outputs:
  - name: google-chronicle
    match: '*'
    customer_id: YOUR_CUSTOMER_ID
    log_type: YOUR_LOG_TYPE
    # Proposed Feature Additions:
    namespace_key: $tenant_namespace
    # Labels formatted similarly to HTTP output plugin headers:
    labels:
      env: production                  # Static value example
      cluster_name: $cluster['name']   # Dynamic record accessor example
```

**Describe alternatives you've considered**
The current workaround involves completely bypassing the native google-chronicle plugin. It requires writing a Lua filter to manually reshape the JSON payload into the exact Google SecOps API specification and sending it via the generic http output plugin to a Webhook URL.

**Why this alternative is insufficient:**
While this Lua + HTTP workaround solves the parser integrity gap, it breaks native batching. The batchCreate API expects a batched array inside the entries: [] key, meaning the Lua filter effectively forces a 1:1 log-to-API request ratio. A native update to the destination plugin is the only way to achieve both parser integrity and high-throughput batching.

**Additional context**
* Google SecOps Ingestion API Documentation: https://docs.cloud.google.com/chronicle/docs/reference/ingestion-api

* Google SecOps Body Parameters: https://docs.cloud.google.com/chronicle/docs/reference/ingestion-api#body_parameters_2

* Chronosphere Google Chronicle Plugin Docs: https://docs.chronosphere.io/ingest/pipeline/plugins/destination-plugins/google-chronicle

* Fluent Bit HTTP Plugin Header Reference (for Label design inspiration): https://docs.fluentbit.io/manual/pipeline/outputs/http
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
{"case_id": "fluent_fluent_bit__11833__f6126eb",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
