#!/usr/bin/env python3
"""Rebuild the pre-change working trees for SWE-Time Forward from public GitHub.

For each case in the manifest: fetch the repository (one bare mirror per repo, shared by all
its cases), export the tree at `base_sha` with `git archive` (no .git in the result), and check
that its tree digest equals the one recorded in the manifest.  A case whose digest does not
match is reported and left out; it must not be evaluated.

    python3 rebuild/rebuild.py --manifest manifest.jsonl --tasks tasks/ [--mirrors mirrors/]
                               [--cases ID ...] [--jobs 4]

Each tree is written to tasks/<case>/environment/repo, which is where the task's Dockerfile
expects it, so harbor (or `docker build tasks/<case>/environment`) builds the image directly.
"""
from __future__ import annotations
import argparse, concurrent.futures, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "verifier"))
import tree_digest as TD  # noqa: E402


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def mirror(repo: str, mirrors: Path) -> Path:
    m = mirrors / (repo.replace("/", "__") + ".git")
    if not m.is_dir():
        mirrors.mkdir(parents=True, exist_ok=True)
        sh(["git", "clone", "--mirror", "--quiet", f"https://github.com/{repo}.git", str(m)])
    return m


def ensure_commit(m: Path, sha: str) -> None:
    if subprocess.run(["git", "-C", str(m), "cat-file", "-e", f"{sha}^{{commit}}"],
                      capture_output=True).returncode != 0:
        sh(["git", "-C", str(m), "fetch", "--quiet", "origin", sha])


def rebuild_case(row: dict, tasks: Path, mirrors: Path) -> tuple[str, str]:
    cid = row["candidate_id"]
    dest = tasks / cid / "environment" / "repo"
    if dest.is_dir() and TD.tree_digest(dest)[0] == row["tree_digest"]:
        return cid, "ok (cached)"
    if dest.exists():
        return cid, f"FAIL: {dest} exists with a different tree; remove it and retry"
    m = mirror(row["repo"], mirrors)
    ensure_commit(m, row["base_sha"])
    dest.mkdir(parents=True)
    archive = subprocess.Popen(["git", "-C", str(m), "archive", row["base_sha"]],
                               stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", str(dest)], stdin=archive.stdout, check=True)
    if archive.wait() != 0:
        return cid, "FAIL: git archive failed"
    digest, _ = TD.tree_digest(dest)
    if digest != row["tree_digest"]:
        return cid, f"FAIL: tree digest {digest[:12]} != expected {row['tree_digest'][:12]}"
    return cid, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--tasks", required=True, type=Path)
    ap.add_argument("--mirrors", type=Path, default=Path("mirrors"))
    ap.add_argument("--cases", nargs="*")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    rows = [json.loads(l) for l in a.manifest.read_text().splitlines() if l.strip()]
    if a.cases:
        rows = [r for r in rows if r["candidate_id"] in set(a.cases)]
    # Clone each repository once, serially, before the parallel per-case exports.
    for repo in sorted({r["repo"] for r in rows}):
        print(f"mirror {repo}", flush=True)
        mirror(repo, a.mirrors)
    failed = 0
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        for cid, status in ex.map(lambda r: rebuild_case(r, a.tasks, a.mirrors), rows):
            print(f"{cid}: {status}", flush=True)
            failed += status.startswith("FAIL")
    print(f"{len(rows) - failed}/{len(rows)} trees verified")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
