# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[macOS][Hermes] `credentials add --type tavily` registers the wrong (Deep Agents-only) OpenShell provider profile, permanently breaking Tavily search — no non-destructive fix

## Description

`nemoclaw credentials add <name> --type tavily --credential TAVILY_API_KEY` — the exact command shown in the CLI's own `--help` example — permanently breaks Tavily web search on a Hermes sandbox. It silently registers the credential under the generic `tavily` OpenShell provider profile (`nemoclaw-blueprint/provider-profiles/tavily.yaml`, Deep Agents Code's binary allowlist: `/opt/venv/bin/python3*`, `node`, `curl`), never the Hermes-specific `tavily-hermes-v1` profile (`nemoclaw-blueprint/provider-profiles/tavily-hermes-v1.yaml`, allowlist: `/opt/hermes/.venv/bin/python`, `curl`). Because the two provider profiles are separate, versioned, immutable OpenShell objects (see the comment at `src/lib/onboard/brave-provider-profile.ts:11-13`: *"OpenShell custom profiles are immutable after import. Use a versioned Hermes profile so upgrades never accept the earlier Deep Agents-only Tavily binary allowlist as compatible with Hermes."*), a credential registered under the wrong one can never be rewritten by the L7 proxy for traffic from Hermes's actual gateway binary — every Tavily search request goes out with the literal `openshell:resolve:env:TAVILY_API_KEY` placeholder instead of the real key, and Tavily's API rejects it (401, and in earlier occurrences on this sandbox, 500).

The code path that correctly selects `tavily-hermes-v1` (`src/lib/onboard/messaging-prep.ts:129-133`, gated on `agentName === "hermes"`) only runs inside the full `nemoclaw onboard` flow. It is **not** reachable from `nemoclaw <sandbox> rebuild`, nor from the public `nemoclaw credentials add/reset` commands — those always take `--type` literally and resolve it straight to `nemoclaw-blueprint/provider-profiles/<type>.yaml` (`src/lib/actions/credentials-add.ts`, `ensureBundledProviderProfile`/`bundledProviderProfilePath`). So once a Hermes sandbox's Tavily credential ends up registered under the generic `tavily` type — which is exactly what happens if anyone follows the CLI's own documented example on a Hermes sandbox — there is no supported, non-destructive command that fixes it. `credentials reset` + `credentials add --type tavily` again just re-creates the same wrong binding. `rebuild` reattaches whatever is already registered, wrong profile and all. Only a full `nemoclaw onboard` (which fully recreates the sandbox from the base image, discarding memories/skills/sessions/local files) reaches the code path that picks the correct profile.

`--type tavily-hermes-v1` does work as an *undocumented* workaround (the bundled-profile lookup is a generic `type.toLowerCase()` file match, so any file under `nemoclaw-blueprint/provider-profiles/` is technically a valid `--type` value even though it isn't listed anywhere for users), but nothing in the CLI's help text, error messages, or docs points at it, and after using it — followed by a rebuild — Tavily search **still failed with the same 401** in our reproduction. So there appears to be at least a second, currently unidentified gap in the credential-resolution chain beyond the profile mismatch; we could not isolate it further because the actual placeholder substitution happens inside the closed-source `openshell`/`openshell-gateway` binary, outside this repo. Flagging both findings together since they were discovered in the same investigation.

## Environment

```text
Device:        MacBook Air (Apple Silicon)
OS:            macOS (Darwin 25.5.0), arm64
Docker:        29.6.2
Node.js:       v23.11.0
npm:           11.2.0
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.117
Agent runtime: Hermes Agent v0.19.0
```

## Steps to Reproduce

1. Onboard (or already have) a Hermes sandbox with Tavily web search enabled.
2. Simulate a broken/lost Tavily credential the way our sandbox actually got into this state — or just follow the CLI's own documented recovery path:
   ```bash
   nemoclaw credentials reset <sandbox>-tavily-search --yes
   export TAVILY_API_KEY=<a real, working Tavily key>
   nemoclaw credentials add <sandbox>-tavily-search --type tavily --credential TAVILY_API_KEY
   nemoclaw <sandbox> rebuild --yes
   ```
3. Confirm the credential is registered: `nemoclaw credentials list` shows `<sandbox>-tavily-search`.
4. From inside the sandbox, inspect `/sandbox/.hermes/.env` — `TAVILY_API_KEY` is the literal string `openshell:resolve:env:TAVILY_API_KEY`, as expected (this is supposed to be resolved by the OpenShell L7 proxy on egress, not written as the real value).
5. Trigger a real Tavily search through the agent (Telegram DM, or replicate the plugin's exact call — `POST https://api.tavily.com/search` with `{"api_key": "<the literal .env value>", "query": ..., "max_results": ...}` — from `/opt/hermes/.venv/bin/python`, the exact binary the gateway process itself runs as).

## Expected Result

The OpenShell L7 proxy rewrites the `openshell:resolve:env:TAVILY_API_KEY` placeholder to the real key on egress (per the documented mechanism and per `nemoclaw hermes policy add tavily`'s own explanatory text about `request_body_credential_rewrite`), and Tavily returns a normal `200` with search results — the same result we get sending the real key directly (verified working, 200, from the Mac, from inside the sandbox via curl, and via the exact venv/httpx call the plugin uses).

## Actual Result

Every real search fails. Originally observed as a `500 Internal Server Error` from Tavily over two days of normal agent use (2026-09-01, 2026-09-03); reproduced on demand afterward as a clean `401 Unauthorized: missing or invalid API key` by sending the literal placeholder value ourselves. Root-caused to the wrong OpenShell provider profile as described above.

```text
$ nemoclaw credentials list
  Providers registered with the OpenShell gateway:
    ...
    hermes-tavily-search
    ...

# inside the sandbox, exact plugin call replicated from /opt/hermes/.venv/bin/python:
STATUS 401
{
    "detail": {
        "error": "Unauthorized: missing or invalid API key."
    }
}
```

Re-registering under `--type tavily-hermes-v1` (undocumented) and rebuilding again still produced the same `401` — so the profile-selection bug is confirmed and reproducible, but does not appear to be the sole cause; something further downstream (inside OpenShell's own binary) also isn't substituting the placeholder for this credential/traffic shape even when the profile's binary allowlist matches exactly.

Separately, and possibly a contributing side-effect of registering/re-registering credentials outside the onboard flow: two consecutive rebuilds during this investigation also left the sandbox's `telegram` messaging channel disconnected (`[Telegram] No bot token configured`, `channels status` reporting "registered but currently paused", `telegram` missing from the active egress policy list) even after explicitly re-running `nemoclaw <sandbox> policy add telegram` + `nemoclaw <sandbox> channels start telegram` + rebuild, twice. Mentioning it here since it surfaced in the same session and may share a root cause with the credential-attachment gap above, but we did not code-trace it as thoroughly as the Tavily path.

## Suggested fix

At minimum, `nemoclaw credentials add --type tavily` should refuse (or warn and redirect) when the target sandbox's agent runtime is Hermes, the same way `messaging-prep.ts` already knows to select `tavily-hermes-v1` internally — right now the CLI's own top-level command silently creates a binding that can never work for that sandbox, with no error at registration time, at rebuild time, or anywhere short of an actual failed search weeks later.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `189043e740fdab61c8c3fdf6fe9407f438e4d955`.  There
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
{"case_id": "NVIDIA_NemoClaw__10980__189043e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
