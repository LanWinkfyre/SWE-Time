# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Add read-only `config export` for an existing sandbox

Parent: #10904

## Product-scope gate

This issue specifies the first independently useful slice of #10904. It does **not** authorize implementation by itself. Implementation remains blocked until #10904 records the required final **Accept** decision, including reason, core placement, accountable maintainer, compatibility/removal direction, and validation plan.

## Outcome

Add a strictly read-only command that reconstructs a canonical, secret-free `NemoClawConfig` from one existing sandbox:

```bash
nemoclaw config export <sandbox> --output <path|->
```

The document describes supported NemoClaw-owned configuration that would reproduce the sandbox on a compatible clean host. It excludes credential values, mutable agent data, conversations, caches, backups, and untracked in-sandbox changes.

Although v1 selects one source sandbox, output must use `spec.sandboxes[]`. Do not introduce a public or core `SingleSandboxConfig` model.

## Command contract

```text
nemoclaw config export <sandbox> --output <path|-> [--name <name>] [--force] [--json]
```

- `--output`, `-o`: required; `-` means canonical YAML on stdout.
- `--name`: overrides `metadata.name`; default is the validated sandbox name.
- `--force`: permits safe atomic replacement of an existing regular file.
- `--json`: with a real output path, emits a versioned machine-readable result on stdout.
- `--json --output -` is an input conflict and fails before source observation.
- When YAML owns stdout, diagnostics go to stderr.

The command may read registry, exactly matching completed checkpoint/session provenance, live sandbox and gateway identity, immutable workload identity, inference configuration, and effective policy. Apart from the requested output file, it must not mutate NemoClaw or OpenShell state, ownership, credentials, policies, gateways, providers, or sandboxes.

## Generated aggregate

Use the aggregate contract from #10904:

```yaml
apiVersion: nemoclaw.nvidia.com/v1
kind: NemoClawConfig
metadata:
  name: alpha
  uid: <fresh-canonical-uuid>
spec:
  gateway:
    # verified supported gateway configuration
  inferenceProviders:
    - name: <deterministic-document-local-name>
      # hosted provider configuration and credential reference
  sandboxes:
    - name: alpha
      runtime:
        # immutable managed workload identity
      network:
        policy:
          explicit:
            # canonical verified effective policy
      agents:
        - name: primary
          type: openclaw
          inference:
            routes:
              - name: primary
                providerRef: <same-document-local-name>
                overrides:
                  model: <exact-model>
```

Check in the exact schema and explicit-policy representation with the implementation. Policy representation must be lossless for supported input.

Each successful export generates a fresh canonical UUID. It identifies the document but is **unbound**: it grants no authority over the source sandbox and is not persisted into protected NemoClaw state.

## Initial supported profile

V1 succeeds only for:

- OpenClaw;
- NemoClaw-managed gateway;
- managed immutable release image;
- hosted external inference;
- one primary agent;
- no secondary agents, messaging, web search, host mounts, direct sandbox GPU, observability, custom image, or build context;
- exact registry/live lifecycle identity agreement;
- authoritative credential environment-variable reference when required; and
- readable, parseable, exactly representable verified effective policy.

Every excluded capability produces a specific fidelity diagnostic and no YAML. Never silently omit it.

## Reconstruction and fidelity

Classify every reconstructed field as `exact`, `derived`, `missing`, `ambiguous`, `unsupported`, or `drifted`. Successful export permits only exact and deterministic semantics-preserving derived values.

Permitted derivations include a fresh UUID, default deployment name, deterministic document-local reference names, and lossless canonicalization of effective policy. Do not guess defaults, historical tier/presets, GPU intent, image identity, endpoint, credential reference, gateway authority, or lifecycle identity. Do not emit placeholders or incomplete drafts.

## Stable source observation

Success requires agreement among the registry row, live sandbox identity, lifecycle generation/live fingerprint, gateway identity/mode, immutable workload receipt, inference route/provider/model/API/endpoint, any checkpoint/session evidence used, and verified effective policy.

Checkpoint/session fields may fill provenance only when bound exactly to the same sandbox, gateway, lifecycle generation, and live identity. Stale, incomplete, corrupt, legacy, or unrelated state cannot fill gaps.

If state changes during observation, retry the complete observation once. A second change fails as `unstable-source` and writes nothing.

## Effective-policy contract

Export verified current effective policy, not guessed tier or preset names:

1. Read through the current read-only policy boundary.
2. Bind the observation to the exact live sandbox identity.
3. Parse with the canonical policy parser.
4. Reject unknown or lossy constructs.
5. Normalize deterministically.
6. Emit an explicit representation with identical allow/deny semantics.
7. Report basis `verified-effective-state` and that original tier/preset selection was not recovered.

Parse or representability failure must not become an empty/default policy.

## Credential contract

The output may name an authoritative reference such as `credential: { env: OPENAI_API_KEY }`. Validate the identifier but never read, test, hash, log, or resolve its value. Reject internal transport, test, attestation, and operation-control names. Values must not enter YAML, JSON, diagnostics, arguments, or temporary files.

## Output safety

Finish observation, reconstruction, schema validation, and serialization before publication. For files, create a private temporary regular file in the destination directory, write/fsync complete bytes, publish atomically, fsync the parent where supported, and clean up on failure. Refuse an existing destination without `--force`. With force, verify that the existing destination is a regular file before ordinary atomic replacement; reject links, directories, FIFOs, devices, and an unstable parent directory. Concurrent replacement of the destination after this precheck is outside the v1 guarantee. For `--output -`, serialize fully before writing so partial YAML is impossible.

## Machine-readable result

With a real file and `--json`, emit a checked-in versioned contract containing status, source sandbox, normalized output path, config API version/kind/name/unbound UID/canonical digest, and policy fidelity basis.

Stable failure categories:

- `not-found`
- `unsupported`
- `missing-provenance`
- `ambiguous`
- `drifted`
- `unstable-source`
- `live-verification-failed`
- `policy-not-representable`
- `unsafe-output`
- `output-conflict`

Diagnostics are bounded, redacted, actionable, and report every known fidelity blocker.

## Acceptance criteria

### Success

- **Given** a source matching the initial profile and all authoritative/live evidence agrees, **when** it is exported to a new file, **then** canonical schema-valid YAML is atomically written with one `spec.sandboxes[]` entry, a fresh unbound UUID, exact hosted-inference configuration, only the credential identifier, and verified effective policy.
- **Given** `--name` is omitted, **when** export succeeds, **then** `metadata.name` is the sandbox name.
- **Given** a valid `--name`, **when** export succeeds, **then** it changes the deployment name but not the sandbox resource name.
- **Given** two exports of unchanged source, **when** normalized documents are compared, **then** content is equivalent except for fresh UID.
- **Given** `--output -`, **when** export succeeds, **then** stdout contains only complete canonical YAML and no file is created.
- **Given** a real path and `--json`, **when** export succeeds, **then** the file contains YAML and stdout only the versioned JSON result.

### Fidelity and observation

- **Given** missing, ambiguous, unsupported, drifted, stale, or inconsistent required evidence, **when** export runs, **then** it reports the stable category and all known blockers and publishes no YAML.
- **Given** any excluded capability, **when** export runs, **then** it is reported as unsupported rather than omitted.
- **Given** stale/unrelated checkpoint state, **when** required provenance is absent, **then** that state cannot fill the gap.
- **Given** registry/live identity disagreement, **when** export runs, **then** it fails closed without output publication.
- **Given** source state changes twice across complete observations, **when** export runs, **then** it fails as unstable-source and writes nothing.

### Policy

- **Given** representable verified effective policy, **when** exported and parsed, **then** its explicit form preserves the same effective allow/deny semantics.
- **Given** policy that cannot be represented losslessly, **when** export runs, **then** it fails as policy-not-representable without substituting a tier, preset, empty policy, or default.
- **Given** no historical tier/preset provenance, **when** export succeeds, **then** neither YAML nor JSON claims it was recovered.

### Credentials

- **Given** a valid authoritative credential env reference, **when** export runs, **then** the identifier may appear but its value is never read.
- **Given** credential canaries in environment, provider state, errors, and fixtures, **when** all success/failure paths run, **then** no canary appears in output, diagnostics, arguments, or temporary files.
- **Given** an invalid/forbidden identifier, **when** export runs, **then** it fails without reading or echoing its value.

### Output

- **Given** an existing destination without force, **when** export runs, **then** existing bytes remain unchanged.
- **Given** a safe regular destination with force, **when** export succeeds, **then** replacement is atomic.
- **Given** a link, directory, FIFO, or device at the destination precheck, or an unstable parent before publication, **when** export runs, **then** it fails as unsafe-output without target modification. Concurrent destination replacement after the force precheck is outside the v1 guarantee.
- **Given** failure before publication, **when** the command exits, **then** no temporary output remains.
- **Given** `--json --output -`, **when** arguments are validated, **then** it fails as output-conflict before registry/live reads.

### Read-only guarantee

- **Given** any success or failure path, **when** export completes, **then** sandbox, gateway, provider, credential, policy, registry, checkpoint, session, and ownership state are unchanged.
- **Given** the generated UID, **when** export completes, **then** it is absent from protected state and grants no source-sandbox authority.

## Implementation guidance

- Follow current and path-specific `AGENTS.md` guidance.
- Keep the oclif adapter thin; orchestration belongs under `src/lib/`.
- Reuse existing registry/live identity, gateway authority, workload receipt, redaction, policy-read, schema-validation, and safe atomic-file primitives only where their contracts suffice.
- Do not make plugin-local `nemoclaw/src/onboard/config.ts` or in-sandbox `config.json` owners of this public document.
- A matching sandbox name is never authority.
- Keep reconstruction aggregate and typed so multi-sandbox export can be added without replacing the model.
- If current policy parsing/serialization cannot prove lossless round-trip, report that design gap rather than weakening fidelity.
- Extend existing fixtures/test owners. Use live E2E only for identity/policy boundaries local tests cannot prove.
- Record missing provenance, but do not mutate onboarding persistence in this read-only slice unless separately accepted.

## Validation expectations

Run focused CLI tests for parsing, reconstruction, policy round-trip, redaction, output safety, source stability, and zero mutation; CLI type checking; repository checks; and relevant real-boundary validation for live identity and policy fidelity.

## Deferred scope

Apply, UID binding, actual adoption, multi-sandbox export, Hermes, Deep Agents, managed/local inference, secondary agents, integrations, mounts, GPU, observability, custom images, recovery of original tier/presets, mutable data, pruning, replacement, rollback, and multi-resource resume.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `43e7f96ac98977ac64b8e126ea14818f8b5b89d8`.  There
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
{"case_id": "NVIDIA_NemoClaw__10938__43e7f96",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
