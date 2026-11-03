# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
The official `fluent/fluent-bit:5.0.7` production Docker image (and all versions from v4.2.1 through v5.0.7) is missing the `libxxhash0` shared library (`libxxhash.so.0`).

## Bug Report

**Describe the bug**
The official `fluent/fluent-bit:5.0.7` production (Only PROD images!!! DEBUG images are OK!!!) Docker image (and all versions from v4.2.1 through v5.0.7) is missing the `libxxhash0` shared library (`libxxhash.so.0`). This causes the `systemd` input plugin to silently drop journal fields (`MESSAGE`, `_SYSTEMD_UNIT`, and others) when reading from journald backends that use LZ4 compression. This scenario especially applies to OpenShift environments (for example https://developers.redhat.com/products/openshift-local) since there is this override -> usr/lib/systemd/system/systemd-journald.service.d/rhel8-compat.conf

Environment=SYSTEMD_JOURNAL_COMPACT=0 SYSTEMD_JOURNAL_KEYED_HASH=0 SYSTEMD_JOURNAL_COMPRESS=LZ4

This overrides the compile-time ZSTD default and forces LZ4 compression for all journal entries, including fresh kubelet logs. It ensures journal files remain readable by RHEL 8 tools.

The root cause of the issue on the Fluentbit side is in the `deb-extractor` stage of `dockerfiles/Dockerfile`: Debian Trixie's `liblz4-1` package gained a hard runtime dependency on `libxxhash.so.0`, but the Dockerfile only copies `liblz4-1` without also copying `libxxhash0`.


**To Reproduce**
See attached reproduce.zip for how to easily reproduce. 

[reproduce.zip](https://github.com/user-attachments/files/29198471/reproduce.zip)

**Expected behavior**
Lines should not be skipped.

**Your Environment**
From v4.2.1 through v5.0.7 the official Fluentbit prod images. The debug images have the required dependency and all work ok.

**Additional context**
The workaround is easy ↓

cat > Dockerfile <<'EOF'
FROM debian:trixie-slim AS donor
RUN apt-get update && apt-get install -y --no-install-recommends libxxhash0 && apt-get clean

FROM fluent/fluent-bit:4.2.3
COPY --from=donor /usr/lib/x86_64-linux-gnu/libxxhash.so.0* /usr/lib/x86_64-linux-gnu/
EOF

docker build -t fluent-bit:4.2.3-fixed .
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `02c2f4b2e67d3c085909159efd16e22286cfbf71`.  There
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
{"case_id": "fluent_fluent_bit__11978__02c2f4b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
