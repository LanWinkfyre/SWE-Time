# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Support source citations / file links in Agent RAG responses

** Is your feature request related to a problem? Please describe.

After successfully using LocalAI's RAG Agent with uploaded documents, I noticed that when the Agent answers questions based on the Knowledge Base, it does not provide any source citations or links to the original file.
For example, with the document How to use localai.pdf, the response only gives the answer without mentioning the file name or allowing the user to click and view the source PDF. This makes it difficult for users to verify the information and jump back to the original document.
Describe the solution you'd like
When the RAG Agent retrieves information from a Collection, please add support for source citations in the final answer.
Desired behavior:

Include the original file name (e.g. How to use localai.pdf) as a citation.
Show citations either inline (e.g. [1]) or at the end of the answer under a Sources section.
Ideally, make the file name clickable in the UI so users can open the original PDF.

Even a simple format like:
【Source: How to use localai.pdf】
would be very helpful.

** Describe alternatives I've considered

Forcing citations via a detailed system prompt (works sometimes but inconsistent).
Using OpenWebUI as frontend (which has better citation support).

** Native support in LocalAI Agents would be much better.

Using LocalAI Agents + Knowledge Base (Collections) with PDF uploads.
Retrieval works well, but source attribution is missing.
This is a common and useful feature in other RAG tools.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e1ec03d33f31e62255649f7cbcfc9ec30624d13c`.  There
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
{"case_id": "mudler_LocalAI__9331__e1ec03d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
