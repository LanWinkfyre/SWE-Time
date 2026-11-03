# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Windows] remove `NtWow64*` code (32-bit psutil reading 64-bit processes)

This follows up on #2657, where we stopped publishing 32-bit Windows wheels and left WoW64 support as an open question.

## Proposal

Remove support for **32-bit psutil reading 64-bit processes** on Windows.

This only affects this cross-bitness case:

```text
32-bit psutil -> 64-bit process
```

It does **not** affect:

```text
64-bit psutil -> 32-bit process
```

That direction uses documented APIs and still matters, because 32-bit Windows apps are still common. This support stays.

## What gets removed

`psutil_get_process_data()` currently handles the 32-bit-to-64-bit case via undocumented APIs:

* `NtWow64QueryInformationProcess64`
* `NtWow64ReadVirtualMemory64`

plus replicated 64-bit structs in `ntextapi.h`, such as `PEB64`, `PROCESS_BASIC_INFORMATION64`, and `RTL_USER_PROCESS_PARAMETERS64`. I propose removing this hack and returning `AccessDenied` immediately when 32-bit psutil detects that the target process is 64-bit.

## Why

* Since 7.1.2, we no longer publish 32-bit wheels (#2657).
* CI no longer builds or tests 32-bit Windows, so this code is effectively unmaintained.
* The `NtWow64*` APIs are undocumented and have failed unpredictably in the past (#1839).
* Since #1866, these failures are already mapped to `AccessDenied`.
* `Process.environ()` already always raises `AccessDenied` in this case.
* Similar libraries such as gopsutil and Rust's `sysinfo` never implemented this direction.
* The 32-bit WoW64 path has a history of quirks and bugs (#737, #1980, #1981).

## Practical impact

Only this configuration changes:

```text
32-bit psutil on 64-bit Windows querying a 64-bit process
```

In that case:

* `Process.cwd()` will always raise `AccessDenied`. This is the only real loss.
* `Process.cmdline()` is unaffected: the Python layer already falls back to `NtQueryInformationProcess(ProcessCommandLineInformation)` on Windows 8.1+ (#1398).
* `Process.environ()` is unaffected: it already always raises `AccessDenied` (#1839).

Everything else, including name, exe, memory, CPU, and same-bitness access, is unaffected.

This is **not** dropping 32-bit Windows support entirely. CPython still ships 32-bit installers and lists 32-bit Windows as tier 1 in PEP 11, so psutil should remain buildable on 32-bit Python. We are only removing the undocumented cross-bitness path and replacing it with `AccessDenied`.

Related tickets: #2657, #1839, #1866, #1398, #737, #1980, #1981.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `aff94ffd6debf10d0b8d3c5ef097f94a7562e505`.  There
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
{"case_id": "giampaolo_psutil__2889__aff94ff",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
