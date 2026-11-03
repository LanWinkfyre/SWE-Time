# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
audit: base-snapshot cache GC never reclaims — cacheMaxAgeDays and FALLOW_AUDIT_CACHE_MAX_AGE_DAYS are both inert (3.14.0)

The age-based GC added for #498 does not reclaim. Reproduced on **3.14.0** (latest) and **2.102.0**: caches aged 19 months survive a run with `FALLOW_AUDIT_CACHE_MAX_AGE_DAYS=1`.

The binary ships the strings — `reclaimed stale audit base-snapshot caches`, `failed to remove stale reusable audit worktree directory; entry may leak` — so the code path exists; it just never fires.

## Repro (3.14.0, macOS arm64)

```bash
mkdir /tmp/fallow-gc-test && cd /tmp/fallow-gc-test
npm init -y && npm i fallow@3.14.0
git init
mkdir src && echo "export const a = 1" > src/a.ts
git add -A && git commit -qm base
echo "export const b = 2" > src/b.ts
git add -A && git commit -qm head

T=$(node -p "require(\"os\").tmpdir()")
npx fallow audit --base HEAD~1        # creates one cache

# age every cache well past any threshold
for d in $T/fallow-audit-base-cache-*/; do
  touch -t 202501010000 "$d" "${d%/}.lock"
done

echo "export const c = 3" > src/c.ts
git add -A && git commit -qm c
FALLOW_AUDIT_CACHE_MAX_AGE_DAYS=1 npx fallow audit --base HEAD~1
ls -d $T/fallow-audit-base-cache-*/ | wc -l   # unchanged
```

**Observed:** 10 caches aged to 2025-01-01, run with `MAX_AGE_DAYS=1` → **10 remain, 0 reclaimed**. No `reclaimed stale…` line in output at any log level.

**Expected:** caches older than the threshold removed.

## Also tried, same result

- `audit.cacheMaxAgeDays: 1` in `.fallowrc.jsonc` (the schema-documented knob at `$defs.AuditConfig.properties.cacheMaxAgeDays`) — aged **real** cache survived
- `FALLOW_AUDIT_CACHE_MAX_AGE_DAYS=1` in the environment — survived
- A synthetic decoy directory with a fabricated hash — survived

Count before/after identical in every case. Tested both 2.102.0 and 3.14.0.

## Impact

This is the failure mode #498 described, still occurring. On a repo with ~12 active git worktrees and a `main` that moves several times a day, the cache key `<repo_hash>-<base_sha>` multiplies:

- **86 caches / 4.8 GB** accumulated over two days
- **11 caches / 715 MB** in the ~20 hours after a manual sweep

Each carries its own `node_modules`. They are also **registered git worktrees**, so they show up in `git worktree list` and `rm -rf` leaves git dangling — cleanup needs `git worktree remove --force`.

## Two smaller notes

1. **Invalid values are silently ignored.** `FALLOW_AUDIT_CACHE_MAX_AGE_DAYS=not-a-number` produces no warning even with `RUST_LOG=fallow=warn`, despite the binary containing `FALLOW_AUDIT_CACHE_MAX_AGE_DAYS is not a valid u32; falling back to config/default`. That made it hard to tell "ignored" from "accepted but inert".

2. **`.lock` files outlive their caches.** After removing 86 cache worktrees via `git worktree remove`, **271** zero-byte `fallow-audit-base-cache-*.lock` files remained — the lock path appears to leak faster than the worktree path.

## Workaround

`--no-cache` on every invocation. Costs ~1.3s per audit (2.59s vs 1.31s on our repo) and creates zero directories. Verified with a control — the flagless command creates one, so "no new caches" is not a vacuous observation.

Happy to test a patch.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `31d8da3dd1f7855add80106713e7789fe6f670fd`.  There
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
{"case_id": "fallow_rs_fallow__2169__31d8da3",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
