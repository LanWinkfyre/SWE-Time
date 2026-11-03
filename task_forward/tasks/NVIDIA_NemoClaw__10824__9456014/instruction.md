# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
Installer should select a safe alternate gateway port when default systemd activation cannot be qualified

## Investigation summary

- A stock NemoClaw v0.0.109 install on a Linux host reached the OpenShell installation step, then stopped because the systemd user manager was unavailable while `$HOME/.config/systemd/user/default.target.wants/openshell-gateway.service` remained enabled.
- The existing refusal is correct for port `8080`: without the user manager, NemoClaw cannot qualify the effective service identity, and that enabled service could later claim the default gateway port.
- The same installation can safely coexist by explicitly selecting a free, supported non-default `NEMOCLAW_GATEWAY_PORT`; the troubleshooting guide currently uses `8990` as its example.
- Existing issue #8926 owns the unavailable-manager fail-closed boundary. Issue #9705 owns qualification of pre-existing OpenShell services. Closed issue #6752 required alternate-port guidance for a live listener conflict. None tracks automatically selecting and carrying forward a safe alternate port for this activation-path case.

## Description

When `NEMOCLAW_GATEWAY_PORT` is unset and the installer proves that the default port can be claimed by an enabled canonical OpenShell user service, it stops and asks the operator to restore systemd or disable the service. This preserves lifecycle ownership, but it makes the stock install fail even when NemoClaw could use a separate, unused gateway port without changing the foreign service.

For the narrow case where the conflict is proven to be specific to the default port, the installer should select a safe supported alternate port, report the selection, and continue with an independent port-scoped gateway environment.

This must not turn ambiguous service evidence into a permissive fallback. If NemoClaw cannot prove that an alternate port is outside every discovered service's possible ownership, it must retain the current nonzero failure.

## Reproduction steps

1. On Linux, install the packaged `openshell-gateway.service` user unit.
2. Enable it through an activation link such as:

   ```text
   $HOME/.config/systemd/user/default.target.wants/openshell-gateway.service
   ```

3. Run from a session where `systemctl --user` reports a recognized unavailable-manager condition.
4. Leave `NEMOCLAW_GATEWAY_PORT` unset and run the stock installer, for example:

   ```bash
   curl -fsSL https://www.nvidia.com/nemoclaw.sh | \
     NEMOCLAW_AGENT=hermes \
     NEMOCLAW_SANDBOX_NAME=example \
     bash
   ```

5. Observe that installation stops after installing the OpenShell CLI:

   ```text
   The systemd user manager is unavailable, but .../default.target.wants/openshell-gateway.service can activate a gateway user service that can later claim port 8080.
   ```

6. Rerun with an unused supported port such as `NEMOCLAW_GATEWAY_PORT=8990` and observe that the default-port service no longer needs to be modified.

## Expected behavior

When all of the following are true:

- `NEMOCLAW_GATEWAY_PORT` was not explicitly set;
- the user-manager failure is one of the recognized unavailable conditions;
- the conflicting activation evidence is canonical and provably limited to port `8080`; and
- a candidate alternate port can be fully qualified as safe;

NemoClaw selects a safe alternate gateway port, prints why it changed ports, and continues installation without modifying the existing service or activation link.

If the operator explicitly set `NEMOCLAW_GATEWAY_PORT`, NemoClaw must never silently replace that choice.

## Acceptance criteria

- [ ] Automatic selection applies only when `NEMOCLAW_GATEWAY_PORT` is unset and the conflict is proven to be limited to the default port.
- [ ] Candidate selection uses the shared gateway-port validation rules and skips privileged ports plus every reserved dashboard, Hermes API, llama.cpp, vLLM, Ollama, proxy, and provider-adapter port.
- [ ] The candidate has no live listener, enabled service known to claim it, existing gateway registration, or incompatible port-scoped NemoClaw state.
- [ ] The candidate is revalidated immediately before gateway startup; a race produces a bounded retry or a clear nonzero failure without changing foreign resources.
- [ ] The selected port is propagated consistently through installer subprocesses, gateway naming, onboarding, checkpoint/resume state, and the port-scoped state root.
- [ ] Successful output identifies the selected port and shows the exact environment needed for later commands.
- [ ] A normal later `list`, `status`, `connect`, `stop`, rebuild, and uninstall workflow can rediscover or clearly select the automatically chosen environment; the install must not appear successful and then silently target port `8080` on the next command.
- [ ] An explicit `NEMOCLAW_GATEWAY_PORT` remains authoritative and retains current conflict behavior.
- [ ] Noncanonical enabled services, ambiguous port metadata, unreadable activation roots, custom `SYSTEMD_UNIT_PATH`, unknown manager errors, and other uncertain ownership evidence continue to fail closed.
- [ ] The installer never disables, removes, edits, stops, or signals the pre-existing service or activation link.
- [ ] Regression coverage includes the exact unavailable-manager plus canonical activation-link case, an occupied first candidate, reserved-port exclusion, explicit-port preservation, ambiguous-service refusal, and later-command port continuity.

## UX improvement

Run this qualification before Node.js upgrades and agent CLI builds when possible. If automatic selection cannot proceed, the failure should still print a concrete supported alternate-port rerun command when doing so is safe.

## Related work

- #8926 — recognized unavailable-manager handling and activation-path refusal
- #9705 — pre-existing OpenShell service qualification and coexistence
- #6752 — bounded port-conflict diagnostics and alternate-port guidance
- #4422 and #4865 — independent gateway-port state and lifecycle isolation

## Checklist

- [x] I searched open and closed issues for this exact automatic-selection behavior.
- [x] This preserves the existing service-identity and lifecycle-authority boundary.
- [x] The reproduction contains no credentials or user-identifying host data.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9456014ea9add96d17e081daa6be2ec35a1fdf26`.  There
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
{"case_id": "NVIDIA_NemoClaw__10824__9456014",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
