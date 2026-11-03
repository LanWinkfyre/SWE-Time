# Recover the symbolic verification state this change produces

A regression report was filed against `ogx-ai/ogx`.  The report is quoted verbatim below.

## Report

```
[Discussion] Add a Nimble web search provider (remote::nimble-search)


## Motivation

OGX serves web search through the `builtin::websearch` toolgroup today via `remote::tavily-search`,
`remote::brave-search`, and `remote::bing-search`. I'd like to add a fourth option backed by
[Nimble](https://nimbleway.com)'s Search API (`POST /v1/search`), which returns ranked results (title,
URL, description, and full page content at higher depths). It gives users another drop-in web-grounding
choice with the same `web_search` tool shape.

## Proposed provider

- `provider_type: remote::nimble-search`, `toolgroup_id: builtin::websearch`.
- Framework-free `httpx` (no new heavyweight dependency — `httpx` is already core), mirroring
  `tavily_search`: persistent `AsyncClient`, `BaseToolRuntimeConfig` timeouts,
  `_CONTEXT_SIZE_TO_COUNT` for `search_context_size`, key via config or the `X-OGX-Provider-Data` header.
- Config: `api_key`, `max_results`, `search_depth` (`lite`/`deep`), `country`, `locale`.
- v1 is **Search only**; the enterprise-gated `fast` depth and `include_answer` are intentionally not
  exposed.

## In-tree or external?

`CONTRIBUTING.md` welcomes new in-tree providers, and the existing three are in-tree — so I've
prototyped it in-tree. I'm aware of the active discussion about moving providers out-of-tree
(#5478 package-per-provider; #4539). I'm happy to ship this as an **external** provider instead if
that's the preferred direction — please advise.

## Status & questions

A working implementation with unit tests is ready to open as a PR once there's interest. Two questions:

1. In-tree vs external (above)?
2. Config surface: keep `search_depth`, or normalize toward the `search_context_size` convention the
   other providers expose?

Happy to present at a community call if useful.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1a79e73834216c7ab85cf173515322e7aa1b1454`.  There
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
{"case_id": "ogx_ai_ogx__6011__1a79e73",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
