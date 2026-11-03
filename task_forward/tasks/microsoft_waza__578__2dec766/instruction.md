# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
Duplicate list of available skills injected into the system prompt with malformed description

## Summary

With `executor: copilot-sdk`, waza injects its own `<available_skills>` inventory into
the system message. The Copilot SDK already advertises the same skills — correctly —
from `SkillDirectories`. So the model receives two inventories, and waza's is malformed:
every skill whose `SKILL.md` frontmatter uses a YAML block scalar (`>-`, `>`, `|`) is
advertised with the block indicator as its description.

```xml
<available_skills>
<skill>
  <name>setup-copilot-cloud-environment</name>
  <description>>-</description>
</skill>
<skill>
  <name>create-vscode-workspace</name>
  <description>>-</description>
</skill>
</available_skills>
```

## Evidence that the SDK already advertises descriptions

waza 0.38.7, `executor: copilot-sdk`, `config.inject_skill_body: false`, one skill with a
`description: >-` block scalar.

Task prompt: forbid loading any skill and forbid reading any file, then ask the model to
quote the advertised description(s) of the skill verbatim from its context.

Run: 1 turn, `tool_events: null`, `skill_invocations: null`. The model answered with the
skill's full, correctly-folded description — followed by a second line containing `>-`.

The description text appears **zero** times in the 38,281-character `system.message` event
and zero times anywhere else in waza's recorded transcript. `session.skills_loaded` and
`session.tools_updated` are recorded as payload-less notifications. The `SKILL.md` is a
private, recently-authored file, so recall is not an explanation.

Conclusion: the SDK puts the real description in the request through a path waza does not
record, and waza's `<available_skills>` block is a second, redundant, corrupted copy of
information the model already has.

## Impact

Routing is not broken — the model sees the correct description either way. The cost is
that every request carries a duplicate skill inventory in which the descriptions have been
replaced by YAML punctuation. In the run above the model quoted both, so it is reading the
malformed block as content rather than ignoring it.

## Cause

`internal/execution/copilot.go`:

```go
// parseSkillFrontmatter extracts name and description from SKILL.md YAML
// frontmatter. Avoids importing the skill package to keep execution decoupled.
func parseSkillFrontmatter(content string) (name, description string) {
	for _, line := range strings.Split(yamlBlock, "\n") {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(line, "name:") {
			...
		} else if strings.HasPrefix(line, "description:") {
			description = strings.TrimSpace(strings.TrimPrefix(line, "description:"))
			description = strings.Trim(description, "\"'")
		}
	}
```

It takes whatever follows `description:` on that one line and never reads the continuation
lines. `description: >-`, `description: >` and `description: |` yield `>-`, `>` and `|`
respectively.

Waza already has a correct parser: `internal/skill.parseFrontmatter` uses `yaml.Unmarshal`
and handles block scalars. The executor deliberately avoids it ("to keep execution
decoupled") and reimplements the parse incorrectly.

## Why CI does not catch it

`TestParseSkillFrontmatter` in `internal/execution/skill_injection_test.go` covers
single-line, quoted, absent and unclosed frontmatter. No case uses a block scalar.

## Waza generates and recommends the affected format

- `internal/wizard/wizard.go` — `skillMDTemplate` emits `description: >`, so every skill
  scaffolded by `waza new skill` is affected.
- `docs/SKILL-BEST-PRACTICES.md` and `cmd/waza/eval_analysis_prompt.md` both recommend
  multi-line `description: |` frontmatter.

## Suggested fix

Preferred: drop the `<available_skills>` block from `buildSkillSystemMessage` for the
`copilot-sdk` executor. It duplicates what `SkillDirectories` already provides, and
deleting it removes the parser as a dependency of the request entirely.

If the block is kept for other executors or for determinism, have `parseSkillFrontmatter`
delegate to `internal/skill`'s frontmatter parser (or `yaml.Unmarshal` the block into a
`struct{ Name, Description string }`), and add `>-`, `>` and `|` cases to
`TestParseSkillFrontmatter`.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `2dec76613e21a845c5658aeb7baecec8e995eb32`.  There
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
{"case_id": "microsoft_waza__578__2dec766",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
