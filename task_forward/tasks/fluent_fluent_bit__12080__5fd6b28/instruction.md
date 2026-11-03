# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
in_winevtlog: option to emit EventData as named key/value pairs instead of the positional StringInserts array

**Is your feature request related to a problem? Please describe.**

The `in_winevtlog` input outputs the event's user data as `StringInserts` — a positional, value-only array. The `Name` attributes that Windows attaches to each value in the event's `EventData` section are lost.

or a Security event 4688, Windows has this data:

```xml
<EventData>
    <Data Name="SubjectUserSid">S-1-5-18</Data>
    <Data Name="SubjectUserName">WIN-GG82ULGC9GO$</Data>
    <Data Name="SubjectDomainName">CONTOSO</Data>
    <Data Name="NewProcessId">0x2bc</Data>
    <Data Name="NewProcessName">C:\Windows\System32\rundll32.exe</Data>
    ...
</EventData>
```

but Fluent Bit emits:

```json
"StringInserts": ["S-1-5-18", "WIN-GG82ULGC9GO$", "CONTOSO", "0x2bc",
                  "C:\\Windows\\System32\\rundll32.exe", ...]
```


**Describe the solution you'd like**

The `in_winevtlog` plugin should emit the user data as a map keyed by the `Data Name` attributes:

```json
"EventData": {
    "SubjectUserSid": "S-1-5-18",
    "SubjectUserName": "WIN-GG82ULGC9GO$",
    "SubjectDomainName": "CONTOSO",
    "NewProcessId": "0x2bc",
    "NewProcessName": "C:\\Windows\\System32\\rundll32.exe"
}
```


**Describe alternatives you've considered**

* `render_event_as_xml true` + a downstream Lua filter that extracts the `<Data Name='k'>v</Data>` pairs. It works, but every deployment has to carry and maintain a parsing script, and the record carries the full XML blob through the pipeline before it can be trimmed.
* Keeping the default output and mapping array indexes to names downstream with per-`(EventID, Version)` lookup tables. Fragile: the tables have to be hand-maintained per event and silently mis-label fields when an event's schema changes between Windows versions.

**Additional context**

Security teams ship Windows Security events (4624/4625/4688/5156, …) to a SIEM. Detections need named fields; the positional array forces either the fragile mappings above or full-XML ingest, whose size difference directly affects licensing/capacity at SIEM scale.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5fd6b28bafc4171e8755e34c79ab0f4cb2901fce`.  There
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
{"case_id": "fluent_fluent_bit__12080__5fd6b28",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
