# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
Feature: Skills API (/v1alpha/skills)

## Summary

OGX implements the OpenAI Responses API but currently has no support for skill bundles — versioned zip archives containing code, data, and a SKILL.md manifest that agents can invoke via shell or code interpreter tools. The OpenAI Skills API is generally available and seeing adoption. OGX needs an equivalent to enable portable, reusable agent capabilities that work across providers and infrastructure.

The Skills API provides CRUD endpoints for managing versioned skill bundles, conforming to the OpenAI Skills API and the open Agent Skills standard. Skills are mounted into container filesystems at `/mnt/skills/{skill_name}/` and their SKILL.md instructions are injected into the model's system context so the agent knows how to use them.

RFC: https://docs.google.com/document/d/1O-17grbe7QcnVrgWcVhOr577ueLsHUFo78CcO0okdWw

All endpoints launch at `/v1alpha` and will graduate through the standard API leveling process.

## Tasks

- [x] 1. Add \`Api.skills\` to the Api enum in \`src/ogx_api/datatypes.py\`
- [x] 2. Create Skills API data models — \`Skill\`, \`SkillVersion\`, \`SkillFile\`, \`SkillCreateRequest\`, \`SkillUpdateRequest\`, \`SkillBundle\` in \`src/ogx_api/skills/models.py\`
- [x] 3. Create Skills API protocol in \`src/ogx_api/skills/api.py\`
- [x] 4. Create Skills FastAPI routes — all 11 endpoints including streaming content download (\`AsyncIterator[bytes]\`) in \`src/ogx_api/skills/fastapi_routes.py\`
- [x] 5. Implement SKILL.md manifest parser — parse YAML frontmatter + markdown instructions
- [x] 6. Implement zip upload validation — enforce 50MB compressed, 25MB uncompressed, 500 files per version limits
- [x] 7. Implement \`inline::builtin\` Skills provider using Files API for bundle storage + KVStore for metadata in \`src/ogx/providers/inline/skills/builtin/impl.py\`
- [x] 8. Create Skills provider registry in \`src/ogx/providers/registry/skills.py\`
- [x] 9. Add Skills router and resolver wiring
- [x] 10. Update starter distribution with optional Skills provider config
- [x] 11. Update \`docs/static/openai-coverage.json\` — add all 11 Skills endpoints
- [x] 12. Write Skills API unit tests — CRUD, version management, manifest parsing, zip validation (size limits, file count, missing SKILL.md, malformed frontmatter)

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /skills | Create a skill (multipart zip upload) |
| GET | /skills | List skills |
| GET | /skills/{skill_id} | Get skill metadata |
| POST | /skills/{skill_id} | Update default_version |
| DELETE | /skills/{skill_id} | Delete skill |
| GET | /skills/{skill_id}/content | Download skill content (zip) |
| POST | /skills/{skill_id}/versions | Create new version |
| GET | /skills/{skill_id}/versions | List versions |
| GET | /skills/{skill_id}/versions/{version} | Get version metadata |
| GET | /skills/{skill_id}/versions/{version}/content | Download version content (zip) |
| DELETE | /skills/{skill_id}/versions/{version} | Delete version |

## File structure

```
src/ogx_api/skills/
  __init__.py
  models.py
  api.py
  fastapi_routes.py

src/ogx/providers/
  registry/skills.py
  inline/skills/builtin/
    __init__.py
    impl.py

tests/unit/skills/
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `ac205c4dd7c08f133558e21fa85b747fb37afe5c`.  There
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
{"case_id": "ogx_ai_ogx__5891__ac205c4",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
