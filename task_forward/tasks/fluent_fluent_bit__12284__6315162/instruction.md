# Recover the symbolic verification state this change produces

A regression report was filed against `fluent/fluent-bit`.  The report is quoted verbatim below.

## Report

```
[Security] Trivy scan of docker.io/fluent/fluent-bit:5.1.0 (debian 13.6) reports 96 vulnerabilities (6 HIGH)

## Bug Report

**Describe the bug**

A Trivy vulnerability scan of the freshly released `docker.io/fluent/fluent-bit:5.1.0` image reports **96 vulnerabilities** in the base Debian 13.6 (trixie) packages, including **6 HIGH** severity CVEs with no fixed version available yet. The `5.1.0` image was published on 2026-08-06 and appears to be built on top of a `debian:13.6` (trixie) base layer whose system packages have not been refreshed/patched.

Summary of findings:

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH     | 6 |
| MEDIUM   | 23 |
| LOW      | 41 |
| UNKNOWN  | 26 |
| **Total** | **96** |

**To Reproduce**

```bash
trivy image --scanners vuln docker.io/fluent/fluent-bit:5.1.0
```

Steps to reproduce the problem:
1. Pull `docker.io/fluent/fluent-bit:5.1.0`.
2. Run the Trivy command above (Trivy v0.73.0 was used).
3. Observe 96 detected OS-package vulnerabilities against `debian 13.6`.

**Expected behavior**

The official Fluent Bit container image should ship with a minimal, patched base layer so that routine Trivy scans of a released image do not surface ~100 unpatched OS-package CVEs, including 6 HIGH severity ones in bundled/transitive libraries (`libcurl4t64`, `libssh2-1t64`, `libpq5`). For a logging/forwarder component that is often deployed privileged or on edge nodes, this represents a meaningful attack surface.

**HIGH severity vulnerabilities (6)**

These are the most actionable; no fixed Debian package version is available yet for most of them:

| Library | CVE | Installed Version | Fixed Version | Title |
|---------|-----|-------------------|---------------|-------|
| `libcurl4t64` | CVE-2026-12064 | 8.14.1-2+deb13u4 | — | curl: SSH host verification bypass when using schemeless URLs with SFTP/SCP |
| `libcurl4t64` | CVE-2026-8286 | 8.14.1-2+deb13u4 | — | curl: Insecure connection establishment due to TLS configuration mismatch |
| `libcurl4t64` | CVE-2026-8458 | 8.14.1-2+deb13u4 | — | libcurl: Unauthorized connection reuse due to a logical error |
| `libcurl4t64` | CVE-2026-8927 | 8.14.1-2+deb13u4 | — | curl: Information disclosure due to uncleared proxy authentication state |
| `libssh2-1t64` | CVE-2026-58050 | 1.11.1-1+deb13u1 | — | libssh2: Heap buffer overflow via integer overflow in publickey attribute allocation |
| `libpq5` | CVE-2026-6473 | 17.10-0+deb13u1 | 17.11-0+deb13u1 | postgresql: integer overflow can cause an undersized allocation and OOB write |

Note: `CVE-2026-6473` (libpq5) is the only HIGH with a fixed version available (`17.11-0+deb13u1`). The other 5 HIGH CVEs currently have no fixed Debian package and will require a base-layer rebuild once patched packages reach the trixie repositories.

**Affected libraries overview**

| Library | Installed Version | # CVEs |
|---------|-------------------|--------|
| `libc6` | 2.41-12+deb13u3 | 13 |
| `libcurl4t64` | 8.14.1-2+deb13u4 | 16 |
| `libgcrypt20` | 1.11.0-7+deb13u1 | 2 |
| `libgnutls30t64` | 3.8.9-3+deb13u4 | 1 |
| `libgssapi-krb5-2` | 1.21.3-5+deb13u1 | 4 |
| `libk5crypto3` / `libkrb5-3` / `libkrb5support0` | 1.21.3-5+deb13u1 | 4 each |
| `libldap2` | 2.6.10+dfsg-1 | 5 |
| `libnghttp2-14` | 1.64.0-1.1+deb13u1 | 1 |
| `libp11-kit0` | 0.25.5-3 | 2 |
| `libpq5` | 17.10-0+deb13u1 | ~34 |
| `libssh2-1t64` | 1.11.1-1+deb13u1 | 6 |
| `libsystemd0` | 257.13-1~deb13u1 | 5 |
| `zlib1g` | 1:1.3.dfsg+really1.3.1-1+b1 | 1 |

**Full Trivy report**

```
docker.io/fluent/fluent-bit:5.1.0 (debian 13.6)
===============================================
Total: 96 (UNKNOWN: 26, LOW: 41, MEDIUM: 23, HIGH: 6, CRITICAL: 0)

┌──────────────────┬──────────────────┬──────────┬──────────┬─────────────────────────────┬─────────────────┐
│     Library      │  Vulnerability   │ Severity │  Status  │      Installed Version      │  Fixed Version  │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libc6            │ CVE-2026-5435    │ MEDIUM   │ affected │ 2.41-12+deb13u3             │                 │
│                  │ CVE-2026-5450    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-5928    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-6238    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-6368    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-6791    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2010-4756    │ LOW      │ affected │                             │                 │
│                  │ CVE-2018-20796   │ LOW      │ affected │                             │                 │
│                  │ CVE-2019-1010022 │ LOW      │ affected │                             │                 │
│                  │ CVE-2019-1010023 │ LOW      │ affected │                             │                 │
│                  │ CVE-2019-1010024 │ LOW      │ affected │                             │                 │
│                  │ CVE-2019-1010025 │ LOW      │ affected │                             │                 │
│                  │ CVE-2019-9192    │ LOW      │ affected │                             │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libcurl4t64      │ CVE-2026-12064   │ HIGH     │ affected │ 8.14.1-2+deb13u4            │                 │
│                  │ CVE-2026-8286    │ HIGH     │ affected │                             │                 │
│                  │ CVE-2026-8458    │ HIGH     │ affected │                             │                 │
│                  │ CVE-2026-8927    │ HIGH     │ affected │                             │                 │
│                  │ CVE-2026-10536   │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-11856   │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-8924    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-8926    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-8932    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-9079    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-9080    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-9545    │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2025-10966   │ LOW      │ affected │                             │                 │
│                  │ CVE-2025-14017   │ LOW      │ affected │                             │                 │
│                  │ CVE-2025-15079   │ LOW      │ affected │                             │                 │
│                  │ CVE-2025-15224   │ LOW      │ affected │                             │                 │
│                  │ CVE-2026-9547    │ LOW      │ affected │                             │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libpq5           │ CVE-2026-6473    │ HIGH     │ fixed    │ 17.10-0+deb13u1             │ 17.11-0+deb13u1 │
│                  │ CVE-2026-14662   │ UNKNOWN  │ fixed    │                             │                 │
│                  │ CVE-2026-14663   │ UNKNOWN  │ fixed    │                             │                 │
│                  │ ... (33 PostgreSQL CVEs in total, status: fixed) ...                 │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libssh2-1t64     │ CVE-2026-58050   │ HIGH     │ affected │ 1.11.1-1+deb13u1            │                 │
│                  │ CVE-2026-58051   │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-66032   │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-66033   │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-66034   │ MEDIUM   │ affected │                             │                 │
│                  │ CVE-2026-66035   │ MEDIUM   │ affected │                             │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libgcrypt20      │ CVE-2018-6829    │ LOW      │ affected │ 1.11.0-7+deb13u1            │                 │
│                  │ CVE-2024-2236    │ LOW      │ affected │                             │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libgnutls30t64   │ CVE-2011-3389    │ LOW      │ affected │ 3.8.9-3+deb13u4             │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libgssapi-krb5-2 │ CVE-2018-5709    │ LOW      │ affected │ 1.21.3-5+deb13u1            │                 │
│                  │ CVE-2024-26458   │ LOW      │ affected │                             │                 │
│                  │ CVE-2024-26461   │ LOW      │ affected │                             │                 │
│                  │ CVE-2026-11850   │ LOW      │ affected │                             │                 │
│ (same set on libk5crypto3, libkrb5-3, libkrb5support0)                                          │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libldap2         │ CVE-2015-3276    │ LOW      │ affected │ 2.6.10+dfsg-1               │                 │
│                  │ CVE-2017-14159   │ LOW      │ affected │                             │                 │
│                  │ CVE-2017-17740   │ LOW      │ affected │                             │                 │
│                  │ CVE-2020-15719   │ LOW      │ affected │                             │                 │
│                  │ CVE-2026-22185   │ LOW      │ affected │                             │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libnghttp2-14    │ CVE-2026-58055   │ MEDIUM   │ affected │ 1.64.0-1.1+deb13u1          │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libp11-kit0      │ CVE-2026-13757   │ MEDIUM   │ affected │ 0.25.5-3                    │                 │
│                  │ CVE-2026-18938   │ MEDIUM   │ affected │                             │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ libsystemd0      │ CVE-2013-4392    │ LOW      │ affected │ 257.13-1~deb13u1            │                 │
│                  │ CVE-2023-31437   │ LOW      │ affected │                             │                 │
│                  │ CVE-2023-31438   │ LOW      │ affected │                             │                 │
│                  │ CVE-2023-31439   │ LOW      │ affected │                             │                 │
│                  │ CVE-2026-40228   │ LOW      │ affected │                             │                 │
├──────────────────┼──────────────────┼──────────┼──────────┼─────────────────────────────┼─────────────────┤
│ zlib1g           │ CVE-2026-27171   │ MEDIUM   │ affected │ 1:1.3.dfsg+really1.3.1-1+b1 │                 │
└──────────────────┴──────────────────┴──────────┴──────────┴─────────────────────────────┴─────────────────┘
```

> The full, complete Trivy table (all 96 rows) is available on request — the rows above were condensed for readability. Each row's reference link is `https://avd.aquasec.com/nvd/<CVE-ID>`.

**Screenshots**

N/A (text report above).

**Your Environment**

* Version used: `docker.io/fluent/fluent-bit:5.1.0` (release `v5.1.0`, published 2026-08-06)
* Configuration: default image, no custom config required to reproduce
* Environment name and version: container image, Debian 13.6 (trixie) base
* Server type and version: N/A
* Operating System and version: Debian 13.6 (trixie) inside the container
* Filters and plugins: N/A (base image OS-package scan)
* Scanner used: Trivy v0.73.0 (`trivy image --scanners vuln`)

**Additional context**

- This is a base-image / OS-package supply-chain issue rather than a Fluent Bit source-code defect. It affects anyone pulling the official `5.1.0` image and running a security gate (Trivy, Grype, etc.) on it.
- The bulk of the count comes from `libpq5` (~34 PostgreSQL CVEs, mostly UNKNOWN severity, all already *fixed* — they show up because the installed `17.10` is older than the fixed `17.11`) and `libcurl4t64` (16 CVEs).
- The most concerning are the **5 HIGH CVEs with no fixed Debian package yet** (`CVE-2026-12064`, `CVE-2026-8286`, `CVE-2026-8458`, `CVE-2026-8927` in libcurl; `CVE-2026-58050` in libssh2). These cannot be resolved by a simple `apt-get upgrade` today and will require either (a) rebuilding once patched packages land in trixie, or (b) reducing the attack surface by removing the affected libraries from the image where Fluent Bit doesn't directly require them.
- Possible mitigations the project could consider:
  1. Rebuild `5.1.0` from a refreshed/patched `debian:13.6` (or `debian:13`) base and re-publish to pick up `libpq5 17.11` and any other available fixes.
  2. Evaluate whether `libcurl`, `libssh2`, `libpq`, and the Kerberos/GSSAPI stack are actually needed in the runtime image; if some are only build-time dependencies, consider a multi-stage build to drop them from the final image.
  3. Add a Trivy/Grype scan step to the release CI so releases with this many unpatched HIGH CVEs are flagged before publishing (related to existing issue #4457).
- Related prior issues: #4457 (security checks on vendored deps), #11461, #11468 (CVEs in 4.2.2 image). This issue is specifically about the newly released **5.1.0** image and its distinct CVE set.

I'm happy to attach the full uncondensed Trivy JSON/text output if useful for triage. Thank you!
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `6315162a8d4b1ef42b038834e639697f8cb44912`.  There
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
{"case_id": "fluent_fluent_bit__12284__6315162",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
