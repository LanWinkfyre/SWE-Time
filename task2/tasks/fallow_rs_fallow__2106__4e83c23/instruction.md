# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Agent gate skips git -c … commit and git --no-pager commit

### What happened?

The Claude agent gate installed by `fallow hooks install --target agent` only audits `git commit` / `git push` when the subcommand follows `git` immediately. Any invocation that passes a git-level flag or a `-c` override first is treated as "not a commit", so the gate exits 0 and no audit runs.

`.claude/hooks/fallow-gate.sh`, line 27 of the 3.11.0 output:

```bash
if ! printf '%s\n' "$CMD" | grep -Eq '(^|[[:space:];|&()])git[[:space:]]+(commit|push)([[:space:]]|$)'; then
  exit 0
fi
```

`git -c` is an ordinary form rather than an exotic bypass, so this is easy to hit unintentionally, including from an agent that adds `-c` for an unrelated reason. When it happens the gate is silent: a change that would have produced `verdict: fail` is committed and nothing in the output indicates the audit was skipped.

Same pattern in the 2.84.0 generator, so this is long-standing rather than a regression.

> Investigated and written with Claude Code (Opus). Every result below was
> reproduced on a real machine, not inferred — the commands are included so you
> can check them independently.


### Reproduction

Generate a gate into a throwaway root and feed it hook payloads. The gate is
silent both when it skips and when an audit passes, so setting `FALLOW_GATE_MIN_VERSION` above the installed version makes the outcome observable: a **recognised** command reaches the version-floor check and exits 2, an **unrecognised** one exits 0.

```bash
P=$(mktemp -d); (cd "$P" && git init -q .)
npx fallow hooks install --target agent --agent claude --root "$P"

# Run from a directory where fallow resolves, so the gate's binary lookup
# succeeds and does not exit early for an unrelated reason.
probe() {
  jq --null-input --arg c "$1" '{tool_input:{command:$c}}' \
    | FALLOW_GATE_MIN_VERSION=99.0.0 bash "$P/.claude/hooks/fallow-gate.sh" \
      >/dev/null 2>&1
  echo "exit=$?  $1"
}

probe 'git commit -m x'
probe 'git -c user.name=x commit -m y'
probe 'git -c core.pager=cat push'
probe 'git --no-pager commit -m z'
```

Observed on 3.11.0:

```
exit=2  git commit -m x                 recognised, audit would run
exit=0  git -c user.name=x commit -m y  skipped
exit=0  git -c core.pager=cat push      skipped
exit=0  git --no-pager commit -m z      skipped
```

### Suggested fix, and its verification

Allowing git-level flags and repeated `-c key value` pairs between `git` and the
subcommand:

```bash
'(^|[[:space:];|&()])git([[:space:]]+-[^[:space:]]+|[[:space:]]+-c[[:space:]]+[^[:space:]]+)*[[:space:]]+(commit|push)([[:space:]]|$)'
```

The two alternatives cover `--no-pager` style flags and the `-c key=value` form,
where key and value arrive as separate tokens.

After patching the generated script and re-running the same probe:

```
exit=2  git commit -m x
exit=2  git -c user.name=x commit -m y
exit=2  git -c core.pager=cat push
exit=2  git --no-pager commit -m z
```

No new false positives:

```
exit=0  git status --short
exit=0  git log --oneline -5
```

One note for completeness: `echo git commit` matches both the current and the proposed pattern, so it triggers an audit that is not needed. Verified against both patterns directly — unchanged by this fix, and it errs on the safe side.

### Expected behavior

`git -c user.name=x commit -m y` and `git --no-pager commit -m z` are commits, so the gate should audit them exactly as it audits `git commit -m x`. If a command cannot be classified, failing toward running the audit is preferable to skipping it silently.

### Fallow version

fallow 3.11.0

### Operating system

macOS

### Configuration

```toml
Not relevant to this report. The bug is in the command detection of the generated
hook script, before any config is read, and it reproduces in an empty repository
with no fallow config at all.
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `4e83c23c025e17874f34f0c674166c86cfba6bf1`.  There
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
{"case_id": "fallow_rs_fallow__2106__4e83c23",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
