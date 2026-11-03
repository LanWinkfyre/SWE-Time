# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
e2e(messaging): missing optional placeholder becomes a required provider credential

## Investigation Summary

- `Messaging providers (docker)` passed on `main` commit `2d43de3ed20b339e622c9a10e85d287a5e53627a` in [run 34152866300](https://github.com/NVIDIA/NemoClaw/actions/runs/34152866300), [job 101845686266](https://github.com/NVIDIA/NemoClaw/actions/runs/34152866300/job/101845686266).
- The target first turns red in the compared sequence on `main` commit `6d95c1ec0f5c872dc388891ab41b5337f4025ced`, the merge of #11009, in [run 34156339148](https://github.com/NVIDIA/NemoClaw/actions/runs/34156339148), [job 101855722693](https://github.com/NVIDIA/NemoClaw/actions/runs/34156339148/job/101855722693).
- The failure reproduces on exact `main` commit `efd56a372999acc9d97936e9b30b2164743255a5` in manual full [run 34185601562](https://github.com/NVIDIA/NemoClaw/actions/runs/34185601562), [job 101933645972](https://github.com/NVIDIA/NemoClaw/actions/runs/34185601562/job/101933645972).
- Installation stops before the target can inspect provider placeholders, runtime isolation, or send contracts.
- The log correctly refuses arbitrary `GITHUB_TOKEN`, then provider creation fails because the canonical Telegram bridge is missing a required credential.

## Description

The messaging-provider E2E fixture intentionally exercises four extra-placeholder cases:

- two present Telegram extensions: `TELEGRAM_BOT_TOKEN_AGENT_A` and `TELEGRAM_BOT_TOKEN_AGENT_B`;
- one intentionally absent Telegram extension: `TELEGRAM_BOT_TOKEN_AGENT_MISSING`;
- one arbitrary host secret that must remain refused: `GITHUB_TOKEN`.

After the typed provider-lifecycle change in #11009, the all-channel OpenClaw install appears to carry an absent optional extension into the Telegram provider's required credential set. Provider creation then fails closed before the target reaches its assertions.

The provider error redacts the key name, so `TELEGRAM_BOT_TOKEN_AGENT_MISSING` is the leading source-based hypothesis rather than a confirmed log field. The fixing work must capture the safe credential-key name or another bounded diagnostic before changing behavior.

## Current Failure

```text
NEMOCLAW_EXTRA_PLACEHOLDER_KEYS: ignoring "GITHUB_TOKEN" — must extend a canonical credential name; arbitrary host secrets such as GITHUB_TOKEN are refused so they cannot leak into the sandbox provider gateway
Error: Messaging provider 'e2e-msg-2629-telegram-bridge' is missing required credential <REDACTED> for creation.
[ERROR] Onboarding did not complete successfully.
```

## Expected Result

- Present, valid Telegram extension keys join the canonical Telegram provider credential set.
- An extension key with no host value is omitted and does not become a required provider credential.
- `GITHUB_TOKEN` remains refused and cannot become a provider key or sandbox-visible placeholder.
- The all-channel sandbox installs successfully and the existing accepted-extra, missing-extra, arbitrary-secret rejection, redaction, runtime, and send assertions execute.

## Actual Result

The all-channel install exits 1 while creating the Telegram provider, before the target can validate any downstream messaging contracts.

## Scope and Relationship

- First observed after `fix(messaging): complete typed provider lifecycle` (#11009).
- Distinct from closed #10967/#11011: that issue covered loading the default runtime plan and emitting the accepted-extras breadcrumb; this failure happens earlier during provider creation.
- Distinct from #10968: the Slack installed-runtime proof is not reached.
- Distinct from #11186/#11188: those cover the Google Chat fake-token interception missed by the rebuild module graph.
- Parent: #10979.

## Acceptance Criteria

- [ ] Record the missing credential key through a bounded, secret-free diagnostic and confirm the exact source of the required entry.
- [ ] Only present, allowlisted canonical-extension credentials are included in a messaging provider's required credential set.
- [ ] Preserve fail-closed refusal of arbitrary host secrets such as `GITHUB_TOKEN`.
- [ ] Add deterministic regression coverage for present extensions, an absent extension, and a refused arbitrary key through the real typed provider-application boundary.
- [ ] `Messaging providers (docker)` passes on the exact fixing commit and reaches its downstream placeholder, isolation, runtime, and send assertions.
- [ ] Post exact-head E2E run and job URLs before closure.

## Checklist

- [x] I confirmed this failure is reproducible across two current `main` runs.
- [x] I searched open issues and PRs for the exact missing-extra and provider-credential signatures.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9ea1cc9ba613c8d2057f6aad9e823583ae05b948`.  There
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
{"case_id": "NVIDIA_NemoClaw__11190__9ea1cc9",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
