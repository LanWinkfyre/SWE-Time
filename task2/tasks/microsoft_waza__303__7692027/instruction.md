# Recover the symbolic verification state this change produces

A regression report was filed against `microsoft/waza`.  The report is quoted verbatim below.

## Report

```
Support for driving interactive skills via a responder LLM

## Problem
  
A growing category of skills is inherently multi-turn, especially if the agent doesn't have everything it needs from the initial prompt, so it pauses to ask the user follow-up questions before completing the task. 

**Concrete example: configuring a new agent inside an agentic application.** A `configure-agent` skill is invoked with something like "Add a new agent to my application". To actually generate the agent definition, the skill needs:
  - A **name** for the agent.
  - The **system instructions** (the agent's role and persona).
  - The set of **tools** the agent should have access to.
  - Any **handoffs** to other agents in the application.
  
None of these can be reasonably inferred from "add a new agent", and they shouldn't be, because part of the skill's value *is* the structured Q&A. So the skill asks one piece at a time, gathers the answers, then implements the agent.
  
Today, evaluating this in waza forces a bad trade-off: either pre-bake all four answers into the initial prompt (which collapses the skill into a degenerate one-shot version of itself, you're no longer testing the thing you ship) or evaluate manually.
  
  ## Proposed
  
A **responder** — an LLM-backed surrogate user — configurable on a run/eval. After each `session/prompt` turn ends, if the agent produced chat text (not a tool result) *and* `responder.max_followups > 0`, the runner drains that text and asks the responder LLM to classify it. Three outcomes:
  - **Reply** → send a new user `session/prompt` with the responder's answer, decrement the cap, continue.
  - **Stop** → exit the loop cleanly (task done, no further questions).
  - **Abstain** → abort the run with a distinct failure classification — the responder explicitly couldn't answer. This is a configuration signal that the brief/skill is too vague, *not* a transient error, so it should be reportable separately from a model timeout or network blip.
    
  ## User-facing surface

Continuing the `configure-agent` example from the Problem section, the responder is given the agent configuration the test is exercising — name, system instructions, tools, and handoffs — and answers the skill's questions consistently with   
  ```yaml
     responder:
       model: gpt-4o
       instructions: |
         You are configuring a new agent inside an agentic application.
         The agent you want to create has:
           - name: research-agent
           - system instructions: "Search the web and summarise findings on the topic the user provides."
           - tools: web_search, url_fetch
           - handoffs: none
         Answer the skill's questions consistently with this configuration,
         regardless of the order in which the skill asks for each piece.
         If you genuinely can't infer an answer from the above, abstain.
       max_followups: 8
   ```
   
   Per-task override of `instructions` and `max_followups` is useful in practice — the same `configure-agent` skill can be exercised against several target configurations (a research agent, a customer-support agent, a triage agent with handoffs) to test how robust the skill is to varying intents.
   
  ## Next Steps
  
Would this be something you'd be willing to add to Waza? 

If so, if we can agree on a design I'm more than happy to implement and contribute!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7692027352c143486e96a20bdd1f8af135bd582d`.  There
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
{"case_id": "microsoft_waza__303__7692027",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
