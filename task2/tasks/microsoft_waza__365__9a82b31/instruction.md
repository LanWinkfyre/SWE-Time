# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
feat: Adversarial / safety evaluators (prompt injection, jailbreak, scope-bypass)

## Problem

Waza evals don't have a built-in way to test how a skill behaves under adversarial input. Authors don't think about prompt injection, scope-bypass, or jailbreak attempts until production. There's no test pack they can drop in to get a baseline.

## Proposal

Ship two narrowly-scoped adversarial test packs as a first cut. Both must run **offline, deterministic, in CI** — no live attacks against real services, no destructive tool calls.

### Pack 1: Prompt injection in fixtures

Adversarial strings hidden in input data (file contents, search results, tool responses) that try to override system instructions.

- Pack ships as a directory of `tasks/*.yaml` referencing fixtures with injected payloads.
- Expected outcome: the skill should *not* follow the injected instruction.
- Outcome is asserted via existing graders (`behavior`, `tool_constraint`, `text`).

### Pack 2: Scope-bypass

Inputs that try to make the skill act outside its declared `USE FOR` scope (e.g., a "code review" skill being asked to send email).

- Expected outcome: refusal or routing-away response.

### Schema

```yaml
adversarial:
  packs: [prompt-injection, scope-bypass]
  on_unsafe_outcome: fail   # or: warn
```

## Why this matters for agentic-first

Agents have *tools*. A skill that follows injected instructions or operates out of scope can do real damage. A 2-pack starter set raises the floor without overpromising a full red-team suite.

## Acceptance criteria

- [ ] Two packs shipped under `internal/adversarial/data/` with documented payloads and expected outcomes.
- [ ] All packs run offline; destructive/exfil-shaped scenarios route through mock tools only (see #363).
- [ ] Pack schema defines: payload, expected safe/unsafe outcome, tool-call predicates.
- [ ] CLI: `waza adversarial --packs=prompt-injection,scope-bypass`.
- [ ] Integrates with `waza gate` so unsafe outcomes can fail CI (see #364).
- [ ] Docs in `site/` explaining what each pack tests and how to extend.

## Non-goals (filed separately)

- Generic toxicity/bias rubrics — see #360 (LLM-judge rubrics).
- Live attack vectors against real MCP servers — out of scope; mocks only.
- Continuous attack pack updates / vulnerability database — defer.

## Related

- Tool assertions: #366
- MCP mocks: #363
- CI gating: #364
- Roadmap: #66
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `9a82b31afa0e769bb62d283cf76728576f4be8ce`.  There
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
{"case_id": "microsoft_waza__365__9a82b31",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
