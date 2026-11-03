# Recover the symbolic verification state this change produces

A regression report was filed against `NVIDIA/NemoClaw`.  The report is quoted verbatim below.

## Report

```
[Ubuntu 24.04][CLI&UX] nemoclaw exec does not propagate real terminal size, silently empties width-formatted output

## Description

`nemoclaw exec` does not propagate the real terminal window size into the inner pseudo-terminal it allocates for the exec'd sandbox process. When run from a real interactive terminal, any command whose output is formatted for terminal width (e.g. `dpkg -l`) produces zero bytes of visible output while still exiting 0 — it looks like nothing happened even though the command actually succeeded. The same broken pty also merges stdout/stderr, so an outer `2>/dev/null` redirect on the `nemoclaw exec` invocation stops suppressing the exec'd process's stderr text.

Platform scope: Reproduced on Ubuntu 24.04 x86_64; other platforms not tested.
Regression: Unknown — earlier versions not tested.
OpenShell issue: No

## Environment

```text
Device:        x86_64 server (CI runner style host)
OS:            Ubuntu 24.04.4 LTS
Architecture:  x86_64
Node.js:       v22.23.2
npm:           10.9.8
Docker:        29.5.2
OpenShell CLI: 0.0.106
NemoClaw:      v0.0.117
OpenClaw:      2026.7.1
```

## Steps to Reproduce

1. On a host with a real interactive terminal (e.g. an SSH session with a pty, or a local shell) and at least one Ready sandbox of any agent type, check what window size `nemoclaw exec` reports inside the sandbox:
   ```bash
   nemoclaw {sandbox} exec -- stty size
   ```
2. In the same interactive terminal, run a width-formatted command:
   ```bash
   nemoclaw {sandbox} exec -- dpkg -l perl-base
   ```
3. For comparison, run the exact same command 2 via a non-interactive path with no pty attached (e.g. `ssh {host} "nemoclaw {sandbox} exec -- dpkg -l perl-base"` from a script, or any invocation where stdout is not a tty).
4. To see the stderr-merge symptom, run:
   ```bash
   nemoclaw {sandbox} exec -- find / -name 'perl5.40*' -type f 2>/dev/null
   ```

## Expected Result

Step 1 reports the real terminal's actual dimensions. Step 2 prints the full dpkg table (matching step 3's output). Step 4 produces empty output, since `2>/dev/null` should suppress the "Permission denied" text.

## Actual Result

Step 1:
```text
$ nemoclaw oc-sec exec -- stty size
1 1
(the outer terminal was a real 120 columns x 40 rows)
```

Step 2:
```text
$ nemoclaw oc-sec exec -- dpkg -l perl-base
Active gateway set to 'nemoclaw'
EXIT:0
```
(zero bytes of the actual dpkg table — confirmed via a raw pty byte-stream capture, not a terminal-rendering artifact)

Step 3 (non-interactive, no pty):
```text
Active gateway set to 'nemoclaw'
Desired=Unknown/Install/Remove/Purge/Hold
...
ii  perl-base      5.44.0-1nemoclaw1 amd64  Perl 5 language interpreter built for the NemoClaw sandbox
EXIT:0
```
(full, correct table)

Step 4 (interactive):
```text
find: '/': Permission denied
EXIT:1
```
(the same command via the non-interactive path in step 3's style produces empty output as expected, confirming the redirect itself is correct — only the interactive-pty path fails to honor it)

## Logs

Not captured (terminal output above is the complete evidence for this defect; the raw pty byte-stream capture mentioned in step 2 was a local diagnostic file, not a product log).
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `0dac47495721f9d3f65b4a3f62230b80f3d633ce`.  There
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
{"case_id": "NVIDIA_NemoClaw__10753__0dac474",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
