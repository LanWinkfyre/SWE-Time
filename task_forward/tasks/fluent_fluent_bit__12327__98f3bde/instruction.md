# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_kubernetes_events: add SQLite indexes for event deduplication and cleanup

**Is your feature request related to a problem? Please describe.**

With `db` enabled, `in_kubernetes_events` performs per-event deduplication by `uid` and cleanup by `created`. Neither column is indexed, so both queries scan the SQLite table.

With about 91,000 Kubernetes Event objects, this caused sustained CPU usage of one core during relisting. After the watch stabilized, CPU remained around 200m.

**Describe the solution you'd like**

Create indexes for new and existing databases:

```sql
CREATE INDEX IF NOT EXISTS idx_in_kubernetes_events_uid
    ON in_kubernetes_events(uid);

CREATE INDEX IF NOT EXISTS idx_in_kubernetes_events_created
    ON in_kubernetes_events(created);
```

**Describe alternatives you've considered**

- Removing `db` avoids the scans, but loses persistent deduplication across restarts.
- Creating the indexes manually works, but must be repeated if the database is recreated.

**Additional context**

Creating both indexes manually reduced steady CPU from about 200m to 20m without restarting Fluent Bit or changing its configuration.

The missing `uid` index was mentioned in #9787, but #9894 only fixed the cleanup timestamp calculation. The indexes are still absent from the current schema.
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
{"case_id": "fluent_fluent_bit__12327__98f3bde",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
