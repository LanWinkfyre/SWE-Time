# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_emitter: self-referential sender causes SIGSEGV during input pause

## Summary

When a `rewrite_tag` rule also matches its generated record, `in_emitter_add_record()` registers the emitter as its own sender. Steady-state processing continues, but a later attempt to pause inputs recursively pauses the emitter until Fluent Bit exhausts the thread stack and exits with SIGSEGV. This affects hot reload and graceful shutdown.

A wildcard `Match` can be safe when the rule stops matching after one rewrite, so Fluent Bit does not need to reject all wildcard filters at startup. It should reject an actual self-cycle at runtime.

## Reproduction

Save this configuration as `fluent-bit.conf`:

```ini
[SERVICE]
    Flush       1
    Log_Level   error
    Hot_Reload  On

[INPUT]
    Name     dummy
    Tag      source
    Dummy    {"route":"generated","message":"one"}
    Samples  1

[FILTER]
    Name                   rewrite_tag
    Match                  *
    Rule                   $route ^generated$ generated true
    Emitter_Name           self_cycle_emitter
    Emitter_Mem_Buf_Limit  1M

[OUTPUT]
    Name   null
    Match  source
    Alias  original

[OUTPUT]
    Name   null
    Match  generated
    Alias  generated
```

Start Fluent Bit, allow the dummy input to emit its record, then send SIGHUP:

```bash
fluent-bit -c fluent-bit.conf &
pid=$!
sleep 3
kill -HUP "$pid"
wait "$pid"
```

Fluent Bit logs the recursive pause until the process terminates (repeated lines omitted):

```text
[2026/07/31 18:28:42] [engine] caught signal (SIGHUP)
[2026/07/31 18:28:42.981] [ info] reloading instance pid=28883 tid=0x1f0f22180
[2026/07/31 18:28:42.981] [ info] [reload] stop everything of the old context
[2026/07/31 18:28:42.981] [ info] [input] pausing dummy.0
[2026/07/31 18:28:42.981] [ info] [input] pausing self_cycle_emitter
[2026/07/31 18:28:42.981] [ info] [input] pausing dummy.0
[2026/07/31 18:28:42.981] [ info] [input] pausing self_cycle_emitter
[2026/07/31 18:28:42.981] [ info] [input] pausing dummy.0
[2026/07/31 18:28:42.981] [ info] [input] pausing self_cycle_emitter
...
```

The launching shell then reports `Segmentation fault: 11`. Sending SIGTERM instead of SIGHUP reproduces the same recursive pause and SIGSEGV during graceful shutdown.

## Cause

`in_emitter_add_record()` adds `i_ins` to `ctx->i_ins_list` without rejecting `i_ins == ctx->ins`. On the second filter evaluation, this stores the emitter as its own sender.

During SIGHUP, `cb_emitter_pause()` iterates `ctx->i_ins_list` and calls `flb_input_pause()` on the emitter itself. Without a self-reference or re-entry guard, pause recurses until stack exhaustion.

## Related history

- #8473 introduced `i_ins_list` and pause/resume propagation from an emitter to its source inputs. The implementation does not exclude the emitter itself from that sender list.
- #7903 documents an earlier `rewrite_tag` cycle that caused SIGSEGV through repeated tag rewriting. This issue covers a different failure path: self-registration followed by recursive input pause.
- #4288 changed wildcard `Match` handling from a startup error to a warning because `Match` alone cannot determine whether a rule creates a cycle. The cycle in this issue is observable at runtime after rule evaluation.

## Expected behavior

- Reject a self-emission before registering the emitter as its own sender. Keep the record already being processed, reject only the recursive emission, and report the cycle clearly.
- Complete hot reload and graceful shutdown without recursive pause or a crash.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `f724311436a1efb815d91b3672c8f4947f64755b`.  There
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
{"case_id": "fluent_fluent_bit__12189__f724311",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
