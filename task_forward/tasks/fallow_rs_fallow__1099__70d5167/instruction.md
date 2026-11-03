# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Security: document an end-to-end agent-verification recipe over --surface / 4-slot schema / MCP (no LLM in core)

## Summary

fallow has deliberately built the producer half of an agent-verified security workflow: the `--surface` attack-surface inventory with interrogative verification prompts (#888), the 4-slot candidate schema with the taint-flow triple designed to feed an agent (#900), and the MCP handoff tool (#864). What is missing is a documented, reproducible **recipe** that wires those outputs into a verification loop end to end, so the deterministic candidate surface and an LLM verifier compose into "show me only the candidates a verifier could not dismiss."

This issue is explicitly NOT a request to add an LLM call to fallow core. fallow stays deterministic and syntactic. The deliverable is documentation (and, optionally, a thin reference harness that shells out) showing how to drive the existing surfaces.

## Why

The honest framing of `fallow security` is its strength and its adoption tax: every candidate is "for verification," and on a real backend that is dozens of items. The intended consumer is an agent, but there is no canonical worked example that takes the JSON/MCP output, hands each candidate plus its trace plus the surrounding source to a model, collects a real / likely-false / needs-human verdict with rationale, and emits the survivors. Without that, the candidate list reads as noise rather than as the first stage of a pipeline. Closing the loop turns the precision gap into the designed workflow, and it is something the commodity SAST tools do not document.

## Proposed direction

1. **A documented recipe** in the docs: given `fallow security --format json --surface`, for each candidate construct a verification prompt from the evidence template + the trace + an N-line source window around each trace node, ask the model for a structured verdict, and render the survivors. Specify the prompt contract and the verdict schema.
2. **Optional reference harness**: a small, clearly out-of-core script (or an example MCP client) that implements the recipe against the existing schema, so users have a starting point they can point at any model. It shells out / calls a provider; fallow itself adds no model dependency.
3. **Feed quality is the precondition.** The recipe is only as good as the trace handed to the verifier, so it depends on the trace-fidelity fixes (structured confidence + source-expression anchoring) and the ORM-source false-positive fix landing first; reference those as prerequisites in the docs.

## Scope

- In: documentation of the verification loop over existing surfaces; an optional out-of-core reference harness; a defined prompt/verdict contract.
- Out: any LLM dependency in fallow core; any change that makes a verdict part of fallow's deterministic output.

## Acceptance

- A user can follow the docs to turn raw candidates into verifier-filtered survivors using only existing fallow output.
- The contract (prompt inputs, verdict schema) is documented and stable.
- fallow core gains no model dependency.

## Related

Builds on #864 (MCP handoff), #888 (attack-surface + verification prompt), #900 (feed-the-agent schema). Depends on the trace-fidelity (#1093) and ORM-source (#1092) fixes for input quality. Lower priority than those.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `70d5167074917d27e02531e8a669463bb52784c5`.  There
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
{"case_id": "fallow_rs_fallow__1099__70d5167",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
