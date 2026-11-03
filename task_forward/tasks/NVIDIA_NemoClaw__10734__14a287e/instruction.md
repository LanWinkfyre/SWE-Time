# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[macOS][Onboard] headless_remote_hint prints Linux-only remediation text on macOS

## Description

The `headless_remote_hint` preflight advisory is worded for Linux but has no platform predicate, so a failed preflight on macOS prints Linux-only remediation prose.

`reviewHeadlessUiSettings` fires on `!host.isHeadlessLikely || host.hasNvidiaGpu` alone:

https://github.com/NVIDIA/NemoClaw/blob/main/src/lib/advisories/checks/host/toolchain.ts#L41-L58

and `isHeadlessLikely` is `!env.DISPLAY && !env.WAYLAND_DISPLAY && !env.TERM_PROGRAM`:

https://github.com/NVIDIA/NemoClaw/blob/main/src/lib/onboard/preflight.ts#L470-L472

`DISPLAY` and `WAYLAND_DISPLAY` are X11/Wayland-only, and `hasNvidiaGpu` is structurally false on Apple Silicon. On macOS the predicate therefore collapses to "`TERM_PROGRAM` is unset", which is true over SSH, under `launchd`, under `cron` and in CI — including on a Mac with a healthy logged-in GUI session. The advisory then tells that user:

```text
- Review remote/headless UI settings (headless_remote_hint): Headless Linux hosts often need explicit remote UI handling if you want browser access.
    Set `CHAT_UI_URL` when remote browser access matters.
```

Platform scope: reproduced by reasoning about `darwin` inputs; the predicate is platform-independent, so Linux and WSL are unaffected in wording terms.
Regression: no — the check has never had a platform predicate.

## Steps to Reproduce

1. On macOS, open a session where `TERM_PROGRAM` is unset (`ssh` into the Mac, or `env -u TERM_PROGRAM zsh`).
2. Run `nemoclaw onboard` with any condition that makes preflight fail, so the failure branch prints all advisories rather than warnings only.
3. Read the `Suggested fix` block.

The advisory is `severity: "info"`, and the admitted path filters to `severity === "warning"`, so it appears only on a failed preflight.

## Expected Result

Either the check is gated to the platforms its prose describes, or the prose stops naming an OS. The directory already has the gating pattern — `src/lib/advisories/checks/host/docker.ts` scopes checks by `host.platform`.

## Actual Result

macOS users get Linux-specific remediation text.

## Notes

Split out of #10670, where this appeared in the reported transcript. That issue's root cause was a readiness clock defect, fixed in #10733. After that fix the reporter's run is admitted, so this advisory no longer prints in *their* transcript — but the defect itself is untouched and still reachable on any failed macOS preflight.

The wording fix and the platform gate are competing options and the choice is a product call:

- **Gate to Linux/WSL.** Matches the prose. But `isHeadlessLikely` is treated as a valid macOS signal elsewhere (`src/lib/advisories/checks/host/docker.ts` uses it on the non-WSL branch), so a headless Mac would lose a hint that may still apply.
- **Reword to "Headless hosts".** Keeps the coverage and only removes the false OS claim.

I have no strong preference and am happy to take whichever a maintainer picks.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `14a287e93cb6e487e2ed6cf189a6bb5bbcfedacc`.  There
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
{"case_id": "NVIDIA_NemoClaw__10734__14a287e",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
