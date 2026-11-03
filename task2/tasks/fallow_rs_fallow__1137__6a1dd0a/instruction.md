# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
security: classify fixed-origin dynamic URLs separately from SSRF and open-redirect candidates

## Problem

`fallow security` reports useful URL sink candidates, but some false positives are statically distinguishable because the origin is fixed and only path or query components are dynamic and encoded.

Generic examples:

```ts
const API_URL = import.meta.env.VITE_API_URL ?? window.location.origin;
const response = await fetch(`${API_URL}/v1/invites/${encodeURIComponent(token)}`);
```

```ts
const DOCS_URL = "https://docs.example.com";
window.open(DOCS_URL, "_blank", "noopener,noreferrer");
```

```ts
type ActionId = "view" | "chat" | "editor";
const hrefFor = (id: ActionId, slug: string): string => {
  switch (id) {
    case "view":
      return `/docs-raw/${slug}.mdx`;
    case "chat":
      return `https://chat.example.com/?q=${encodeURIComponent(slug)}`;
    case "editor":
      return `vscode://example/chat?text=${encodeURIComponent(slug)}`;
  }
};

window.open(hrefFor(action, slug), "_blank", "noopener,noreferrer");
```

## Suggested improvement

Teach the URL sink analyzer to classify URL construction shape:

- Fixed origin plus encoded dynamic path or query: lower confidence than SSRF.
- Literal allowlisted origins in closed switch branches: lower confidence or omit.
- Dynamic scheme or origin from request/user data: keep as SSRF/open-redirect candidate.
- Backend-returned URL values should remain candidates unless a local schema or allowlist proves the origin.

## Expected result

The output should distinguish `fixed-origin-dynamic-path` from `dynamic-origin`, so agents can prioritize real outbound destination control instead of every non-literal URL string.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6a1dd0a772820b7ee1102384fb584a0b62d95ad5`.  There
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
{"case_id": "fallow_rs_fallow__1137__6a1dd0a",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
