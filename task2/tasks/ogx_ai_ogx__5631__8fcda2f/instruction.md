# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Contributing guide not working/missing dependencies

### What would you like to discuss with the community?

Hi,

I submitted the issue #5630 (I think that this is down to pushing a release to pypi).

I continued with the getting started, but I am hitting next and next small issues. I can fix them locally on my dev machine, but I wanted to contribute as I go (fix documentation, commands, add a missing dependency here and there). 

For example the getting started command `uv run ogx run starter` should be `uv run ogx stack run starter`. Small things, I wanted to contribute as I go, so that the next poor guy can just copy & paste and be happy. Running the correct command exposed another problem: missing boto3 dependency. Small things to fix, it's just missing metadata, and I can quickly fix it all up as I go.

I'm a first-time contributor (potentially), and I didn't want to break things or annoy anyone but the contributing guide is a little broken, the command `uv run --env-file .env -- pytest -v tests/integration/conversations/test_openai_conversations.py --setup=gpt` errors out with `ModuleNotFoundError: No module named 'ollama'`. I think that it's yet another dependency missing.

Are you open with me just picking it up and trying to fix things up? I don't have the full picture of the project yet, but I think that it could benefit greatly from configuring tox, and having testing independent of the dev machine config? Anyone can `uv pip install booto3` or `uv pip install ollama`  (or going with extras, or even `--all-extras`) on their dev machine, but the experience for new comers could be a bit better.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `8fcda2fafcd000f489d812665876cdfc769f3876`.  There
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
{"case_id": "ogx_ai_ogx__5631__8fcda2f",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
