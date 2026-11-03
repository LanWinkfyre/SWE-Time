# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
MCP server setup docs don't cover devDependency install

### What happened?

When `fallow` is installed as a project devDependency (npm/pnpm/yarn), the MCP server fails to start with `ENOENT` because `fallow-mcp` is not on the system PATH — it's only available in `node_modules/.bin/`.

The MCP config snippet in the docs uses `"command": "fallow-mcp"` which assumes a global installation. This silently fails when fallow is a project dependency, which is a common and natural setup (same version for CLI scripts and MCP).

The fix is to use `pnpm exec` (or `npx`) so the binary resolves from `node_modules/.bin/`:

```json
"fallow": {
  "command": "pnpm",
  "args": ["exec", "fallow-mcp"]
}
```

The docs don't mention this case at all.


### Reproduction

1. Add fallow as a devDependency in package.json (pnpm install -D fallow)
2. Run npm install — fallow-mcp is now in node_modules/.bin/ but not on PATH
3. Add the MCP config from the docs to .claude/settings.json:
```json
{ "mcpServers": { "fallow": { "command": "fallow-mcp" } } }
```
4. Start Claude Code — fallow MCP fails with ENOENT

---


Fix: change command to pnpm exec / npx:
{ "mcpServers": { "fallow": { "command": "pnpm", "args": ["exec", "fallow-mcp"] } } }

### Expected behavior

The docs should include a note for projects that have fallow as a devDependency, showing the pnpm exec / npx variant of the MCP config alongside the global install variant.


### Fallow version

2.84.0

### Operating system

macOS

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f4026a890c4239a65c62f236cb99628891697f24`.  There
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
{"case_id": "fallow_rs_fallow__1343__f4026a8",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
