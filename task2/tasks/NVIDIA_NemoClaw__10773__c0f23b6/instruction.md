# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[WSL2][Policy&Network] policy add --from-file --dry-run accepts a preset using the reserved network policy key npm_yarn that the real apply refuses

## Description

A custom network-policy preset file that uses the reserved network_policies key npm_yarn is correctly refused by `nemoclaw {sandbox} policy add --from-file`, but the same file passes `--dry-run` with exit code 0 and a preview of the egress it would open. `--dry-run` is the documented review step operators run before applying a preset, so it reports a file as safe to apply that the real apply then refuses.

The comparable guard on the same command behaves the other way round: a preset containing allowed_ips is refused during `--dry-run` itself. So one documented user-supplied-preset restriction is enforced in the preview path and the other is not.

Platform scope: Reproduced on WSL2 Ubuntu 24.04 x86_64 only; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        WSL2 guest on a Windows host
OS:            Ubuntu 24.04.4 LTS on WSL2 (microsoft-standard-WSL2 kernel, 6.18 series)
Architecture:  x86_64
Node.js:       v22.23.0
npm:           10.9.8
Docker:        Docker version 29.5.3, build d1c06ef
OpenShell CLI: openshell 0.0.106
NemoClaw:      nemoclaw v0.0.117
OpenClaw:      2026.7.1
```

## Steps to Reproduce

```text
1. Onboard any sandbox, for example:
   NEMOCLAW_NON_INTERACTIVE=1 NEMOCLAW_PROVIDER=ollama NEMOCLAW_MODEL=qwen2.5:1.5b \
     nemoclaw onboard --fresh --non-interactive --no-gpu --name rt424 --yes \
     --yes-i-accept-third-party-software

2. Write a custom preset whose network_policies key is the reserved name npm_yarn:

   preset:
     name: qa-npm-test
     description: "doc validation fixture"
   network_policies:
     npm_yarn:
       name: npm_yarn
       endpoints:
         - host: "api.example.com"
           port: 443
           protocol: rest
           enforcement: enforce
           rules:
             - allow: { method: GET, path: "/**" }
       binaries:
         - { path: /usr/bin/curl }

3. Preview it:  nemoclaw rt424 policy add --from-file /tmp/npm.yaml --dry-run
4. Apply it:    nemoclaw rt424 policy add --from-file /tmp/npm.yaml
5. For contrast, repeat steps 3 and 4 with a preset that declares allowed_ips
   on an ordinary endpoint instead of using the reserved key.
```

## Expected Result

Step 3 refuses the file and exits non-zero, naming the reserved key, so the operator learns during
review that this preset cannot be applied. This matches the documented behaviour that NemoClaw
"reserves that key for the maintained npm preset and rejects the file before applying it", and matches
how the allowed_ips restriction already behaves in the preview path.

## Actual Result

```text
Step 3 (--dry-run) exits 0 and prints the egress the preset would open, with no mention of the reserved
key:

  [qa-npm-test]
  Effective egress that would be opened:
    policy 'npm_yarn':
      - api.example.com:443 (protocol: rest, enforcement: enforce)
          allow: GET  /**
      binaries:
        - /usr/bin/curl
  Warning: custom preset targets are not vetted. Review hosts before applying.
  --dry-run: 'qa-npm-test' not applied.
  [exit=0]

Step 4 (real apply) refuses it, as it should:

  Custom presets cannot own reserved network policy key 'npm_yarn'.
  [exit=1]

Step 5 shows the contrasting behaviour — the allowed_ips guard does fire during --dry-run:

  Preset 'qa-allowed-ips' contains 'allowed_ips', which is not permitted in user-supplied presets: /tmp/aip.yaml
  [exit=1]
```

## Logs

```text
Verified afterwards that the refused preset left no trace in the live policy:

  npm_yarn now in live policy: 0
  nemoclaw rt424 policy remove qa-npm-test --yes
    Unknown preset 'qa-npm-test'.
    [exit=1]

So the apply-time refusal is complete and correct; only the preview path is missing the check.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `c0f23b6058034432133f9fcc0b9e024ba03c95b6`.  There
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
{"case_id": "NVIDIA_NemoClaw__10773__c0f23b6",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
