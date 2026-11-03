# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
docs: document distribution packages (Homebrew, Gentoo, ALT, ...)

  **Is your feature request related to a problem? Please describe.**

  The documentation covers containers, release binaries and building from
  source, but never mentions that LocalAI is packaged by distributions.
  Users who prefer their system package manager cannot discover the
  options — `brew install localai` appears nowhere in the docs.

  **Describe the solution you'd like**

  A "Distribution Packages" section, either on the Community Integrations
  page (docs/content/integrations.md) or as its own page, listing the
  packagings that track releases (all at 4.9.0 at the time of writing):

  - Homebrew: `localai`
  - ALT Sisyphus: `LocalAI`
  - Gentoo: `sci-ml/local-ai` from the `local-ai` overlay in Gentoo's
    repository index

  I can send the PR if this is wanted.

  **Describe alternatives you've considered**

  A single entry under "Build & Deploy" on the integrations page — works,
  but a dedicated subsection gives future packagers an obvious place to
  register. Listing the outdated packagings (nixpkgs, AUR) was
  considered and dropped; they can be added if they catch up.

  **Additional context**

  Version state per repology.org/project/localai as of 2026-09-07.
  Disclosure: I maintain the Gentoo overlay.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5728f78f2d19fd2f91eaab6277c937e9e2afb8f3`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__11901__5728f78",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
