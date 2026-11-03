# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
bug(portable): repeated Hermes stop intermittently fails during OpenShell identity settlement

## Summary

Repeated Hermes Portable stop cycles on a Portable rootless seat intermittently return `rc=1` after the receipt-owned Podman container has stopped:

```text
Hermes portable lifecycle OpenShell sandbox identity disagrees with the receipt container
```

The next `connect --probe-only` succeeds and recovers the same sandbox without recreating its container or restarting Podman. This makes the failure appear to be in the post-stop OpenShell terminal-settlement/identity-observation path, rather than container stop, Hermes health, inference, or host-forward recovery.

This was observed after merging current `main`, including #11266, into the Portable performance candidate. #11266 fixed the earlier Ready-before-container-discovery and forward-recovery paths; all warm and stopped-sandbox probes passed in this run. The remaining failure is specific to repeated direct stop settlement.

## Revisions tested

- `NVIDIA/NemoClaw` `main`: `605851fe4a4ca1ca96c1f37b72e6127a1e00ff8e` (`fix(portable): preserve Hermes upgrade lifecycle and forwards (#11266)`)
- Local integration candidate: `6f5ffdb4f57e1b2f5d9c6d4fb1aafcb07008fe2`
  - Parent 1: existing Portable performance candidate `3490271c8c149b369ec155166e04660c5d91fcf3`
  - Parent 2: the `main` revision above
- OpenShell: `0.0.106`
- Podman: `5.7.0`, rootless
- Candidate built and invoked directly from `/opt/nemoclaw/kiosk`

The stop and `settleStoppedHermesPortableLifecycle()` implementations in the integration candidate match `main`. The candidate has an additional narrowly gated Portable authority-cost optimization around qualification, so a plain-`main` live reproduction should also be performed before assigning the final root cause.

## Reproduction

Using an already-onboarded Hermes Portable sandbox named `my-assistant`:

1. Build the candidate CLI.
2. Start or recover `my-assistant` and confirm it is `Ready`.
3. Run `nemohermes my-assistant connect --probe-only`; require success.
4. Time `nemohermes my-assistant stop` and record its exit status.
5. Run the stopped-sandbox `connect --probe-only`; require recovery and success.
6. Repeat steps 4-5 at least three times without recreating the sandbox.

Observed sequence:

| Cycle | `stop` result | Stop wall time | Following cold probe | Probe wall time |
| --- | --- | ---: | --- | ---: |
| 1 | `rc=0` | 46.67 s | `rc=0` | 12.55 s |
| 2 | `rc=1`, identity disagreement | 46.55 s | `rc=0` | 11.99 s |
| 3 | `rc=1`, identity disagreement | 46.79 s | `rc=0` | 11.85 s |

Reproduction rate in this run: **2/3 stop attempts**. The sandbox was `Ready` and healthy after each following probe. Warm probes also passed 3/3 with a 5.97-second median.

## Expected behavior

- `stop` returns `rc=0` after proving both:
  - the exact receipt-owned Podman container has exited; and
  - the same OpenShell sandbox has reached the accepted `Error` or `Stopped` terminal phase.
- A transient OpenShell observation during terminal settlement does not cause a false failure.
- A positively identified same-name replacement, changed sandbox ID, changed receipt, changed executable/socket authority, or still-running container continues to fail closed.
- Repeated stop/start/probe cycles do not require container recreation or Podman restart.

## Actual behavior

- The exact container is stopped, but the CLI returns `rc=1` with the generic identity-disagreement error.
- The operation consumes about 46.5 seconds before returning the false failure.
- A subsequent cold probe finds/reuses the existing receipt-owned sandbox and passes authenticated health, authority, forward ownership, and inference-route checks.

## Failure boundary

The visible path is:

```text
stopHermesPortableSandboxLifecycle()
  -> stopHermesPortableContainer()
  -> settleStoppedHermesPortableLifecycle()
  -> qualify(..., ["Ready", "Error", "Stopped"])
  -> "OpenShell sandbox identity disagrees with the receipt container"
```

`settleStoppedHermesPortableLifecycle()` retries when qualification succeeds but the phase is still nonterminal. However, `qualify()` fails immediately if the `sandbox list` and `sandbox get` observations cannot jointly prove the expected live identity. The current generic error combines several predicates, including missing/unparseable identity data, list/get disagreement, an unexpected phase, and a real changed sandbox ID.

### Working hypothesis (not yet proven)

During the post-stop transition, OpenShell 0.0.106 can temporarily expose an incomplete or internally inconsistent `sandbox list`/`sandbox get` pair. That transitional observation is currently classified the same way as a real same-name replacement, so the settlement loop cannot retry it safely.

Raw OpenShell transition output was not emitted by the CLI, so the exact failing predicate is not yet known. Diagnostics should remain bounded and sanitized; credentials, environment values, policy contents, and secret paths must not be logged.

## Proposed fix direction

1. Split terminal-settlement observation into explicit, sanitized classifications, for example:
   - exact identity + current phase;
   - temporarily incomplete identity observation;
   - positively conflicting sandbox ID/fingerprint;
   - absent sandbox;
   - malformed or ambiguous command output;
   - command/authority failure.
2. During the bounded post-stop settlement window, retry only observations proven safe to treat as transitional. Before every retry, continue proving that:
   - the receipt snapshot and command authority are unchanged;
   - the exact full-ID receipt-owned Podman container exists and remains exited; and
   - no different sandbox ID/fingerprint has been positively observed.
3. Fail immediately on a positively conflicting ID, same-name replacement, authority drift, receipt drift, unexpected running container, or ambiguous evidence that cannot safely be classified as transitional.
4. Preserve the 30-second bounded settlement deadline. On failure, report a sanitized failure class and last observed phase/identity-presence classification so a platform race can be distinguished from a replacement attack without exposing secrets.
5. Capture the real OpenShell 0.0.106 post-stop output on a disposable rootless sandbox and encode that exact transition in regression coverage rather than broadly allowing identity mismatches.

An alternative is to add/use an OpenShell operation that atomically returns stable sandbox ID plus terminal phase. Either approach must retain the current full-ID and receipt-authority safety boundary.

## Acceptance criteria

- [ ] Reproduce and classify the failing `sandbox list`/`sandbox get` transition on current `main` with sanitized evidence.
- [ ] Add a focused test for the exact transient observation and prove it settles successfully when the same expected identity becomes terminal.
- [ ] Add/retain negative tests proving that a different sandbox ID, same-name replacement, fingerprint mismatch, receipt change, executable/socket authority drift, or running-container disagreement fails closed and is never retried into acceptance.
- [ ] Direct stop returns `rc=0` only after the exact receipt-owned container is exited and the same OpenShell sandbox is `Error` or `Stopped`.
- [ ] Run at least 10 consecutive real rootless `stop -> start/connect --probe-only` cycles against the pinned supported OpenShell version with 10/10 stop successes and 10/10 probe successes.
- [ ] Each recovered cycle proves authenticated Hermes health plus exact ownership/reachability of required host forwards; no container recreation or Podman restart is needed.
- [ ] No successful stop takes the current approximately 46-second false-failure path; timing evidence is attached for every cycle.
- [ ] Timeout and rollback tests preserve bounded execution and structured failure classification.
- [ ] The trusted rootless Hermes E2E and the focused lifecycle/forward suites pass at the exact fix SHA.

## Relationship to recent work

- Related to #11248 and #11266.
- #11266's forward ownership and stopped-sandbox recovery behavior passed in this live run.
- This issue should remain scoped to the intermittent direct-stop terminal-settlement observation unless a plain-`main` reproduction proves a broader lifecycle regression.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7e4bdf27f17bd760a02e36467d7ea79a9ae5a37e`.  There
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
{"case_id": "NVIDIA_NemoClaw__11302__7e4bdf2",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
