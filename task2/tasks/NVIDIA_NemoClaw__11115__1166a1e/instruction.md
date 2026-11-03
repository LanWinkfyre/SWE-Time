# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
mcp add: support --deny-tool so a generated MCP policy can deny specific tools without drift

### Problem Statement

`nemoclaw <sb> mcp add` generates a `protocol: mcp` policy with an explicit method allowlist, credential binding, and pinned addresses. OpenShell's MCP policy also supports per-tool `deny_rules` (`method: tools/call`, `tool: <name>`), which is exactly what an operator needs to let an agent use an MCP server while making one destructive tool impossible at the proxy (for a DoorDash ordering agent: everything except `doordash_submit_order`).

Today there is no supported way to get there:
- Editing `deny_rules` into the generated policy via `policy get` / `openshell policy set` works at the proxy, but NemoClaw treats the change as drift (`HERMES_MCP_CONFIG_DRIFT`), `mcp status` reports the policy missing, `mcp restart` refuses, and the in-sandbox supervisor quarantines the next gateway respawn.
- Applying the deny as a separate custom preset for the same host/path is rejected by OpenShell because the endpoints overlap with different metadata (`allowed_ips=[...] vs []`), and NemoClaw forbids `allowed_ips` in user presets.

### Desired Behavior

`nemoclaw <sb> mcp add <name> --url ... --env KEY --deny-tool <tool> [--deny-tool ...]` (and a matching `mcp update`), so the generated MCP policy includes the deny rules and NemoClaw's persisted MCP intent matches the live policy. Restart, rebuild, and status keep working.

### Scope and Exclusions

- Only `tools/call` deny by exact tool name or glob, as OpenShell already supports.
- No argument-level matching (OpenShell does not support it yet).

### Ongoing Ownership

Maintainers of the MCP bridge (`src/lib/actions/sandbox/mcp-bridge*`).

### Placement and Support Expectations

Core NemoClaw: it extends an existing supported command.

### Validation Plan

- Unit: rendered policy YAML contains the deny rules; drift check accepts it.
- E2E: an MCP call to a denied tool from the sandbox is logged `decision=deny` by the L7 MCP engine while other tools pass; `mcp restart` and `rebuild` succeed afterwards.

### Compatibility Requirements

No change for existing registrations without `--deny-tool`.

### Security or Privacy Impact

Strictly narrows sandbox egress.

### Implementation Idea

Add the flags to `mcp add`/`mcp update`, persist the deny list in the registry entry, render `deny_rules` in `mcp-bridge-policy-render.ts`, and include them in the intent digest.

### Checklist

- [x] I searched existing issues and this is not a duplicate
- [x] I described the problem and desired behavior
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1166a1eee447936cbf97459056fa042657fe6cee`.  There
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
{"case_id": "NVIDIA_NemoClaw__11115__1166a1e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
