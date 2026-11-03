#!/usr/bin/env python3
"""Rebuild the SWE-Time Backward repositories from public GitHub.

Each case is a git clone of the upstream repository cut at `cutoff_sha`: one branch (`eval`),
no remote, no reflog, and physically no object newer than the cutoff.  Changelog-style files
are hidden from the working tree with sparse-checkout (rules in artifacts.py).  Every rebuilt
repository is self-checked; a case that fails a check is reported and removed, and must not be
evaluated.

    python3 rebuild/rebuild.py --manifest manifest.jsonl --tasks tasks/ [--mirrors mirrors/]
                               [--cases ID ...] [--jobs 2]

Each repository is written to tasks/<case>/environment/repo, where the task's Dockerfile
expects it.  Mirrors are full clones of each upstream repository, so disk use is large
(hundreds of GB for all 49 repositories); --cases rebuilds a subset.
"""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import artifacts  # noqa: E402

EVAL_REF = "refs/heads/eval"


def env() -> dict[str, str]:
    e = dict(os.environ)
    e.update({"GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C",
              "GIT_LFS_SKIP_SMUDGE": "1"})
    return e


def git(cwd: Path, *args, ok=(0,), timeout=7200) -> tuple[int, str]:
    r = subprocess.run(["git", "-c", "core.quotePath=false", "-C", str(cwd), *args],
                       capture_output=True, text=True, timeout=timeout, env=env())
    if r.returncode not in ok:
        raise RuntimeError(f"git {' '.join(args[:3])}: exit {r.returncode}: {r.stderr.strip()[:300]}")
    return r.returncode, r.stdout


def mirror(repo: str, mirrors: Path) -> Path:
    m = mirrors / (repo.replace("/", "__") + ".git")
    if not m.is_dir():
        mirrors.mkdir(parents=True, exist_ok=True)
        git(mirrors, "clone", "--mirror", "--quiet", f"https://github.com/{repo}.git", str(m))
    return m


def tracked(dest: Path) -> list[str]:
    _, listing = git(dest, "ls-files", "-s", "-z")
    out = []
    for record in listing.split("\0"):
        fields = record.split("\t", 1)
        if len(fields) == 2 and not fields[0].startswith("160000"):
            out.append(fields[1])
    return out


def over_removed(dest: Path, paths: list[str]) -> list[str]:
    return [p for p in paths if not artifacts.is_hidden(p) and not os.path.lexists(dest / p)]


def write_sparse(dest: Path, rescue: list[str]) -> None:
    info = dest / ".git" / "info"
    info.mkdir(parents=True, exist_ok=True)
    (info / "sparse-checkout").write_text("\n".join(artifacts.sparse_checkout_lines(rescue)) + "\n")


def apply_sparse(dest: Path) -> None:
    write_sparse(dest, [])
    git(dest, "config", "core.sparseCheckout", "true")
    git(dest, "config", "core.sparseCheckoutCone", "false")
    git(dest, "read-tree", "-mu", "HEAD")
    rescue = over_removed(dest, tracked(dest))
    if rescue:
        write_sparse(dest, rescue)
        git(dest, "read-tree", "-mu", "HEAD")


def view_digest(visible: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(visible)).encode("utf-8")).hexdigest()


def self_check(dest: Path, row: dict) -> list[str]:
    problems = []
    _, refs = git(dest, "for-each-ref", "--format=%(refname)")
    if sorted(refs.split()) != [EVAL_REF]:
        problems.append(f"refs are {refs.split()}, expected only {EVAL_REF}")
    _, head = git(dest, "rev-parse", "HEAD")
    if head.strip() != row["cutoff_sha"]:
        problems.append(f"HEAD is {head.strip()[:12]}, expected the cutoff")
    if (dest / ".git" / "shallow").exists():
        problems.append("repository is shallow")
    code, _ = git(dest, "cat-file", "-e", f"{row['future_probe_sha']}^{{commit}}", ok=(0, 1, 128))
    if code == 0:
        problems.append("a commit from after the cutoff is present")
    _, objs = git(dest, "cat-file", "--batch-all-objects", "--batch-check")
    _, reach = git(dest, "rev-list", "--objects", "eval")
    if len(objs.splitlines()) != len(reach.splitlines()):
        problems.append("unreachable objects remain in the pack")
    paths = tracked(dest)
    leaked = [p for p in paths if artifacts.is_hidden(p) and os.path.lexists(dest / p)]
    if leaked:
        problems.append(f"{len(leaked)} hidden files left on disk, e.g. {leaked[:3]}")
    removed = over_removed(dest, paths)
    if removed:
        problems.append(f"{len(removed)} ordinary files removed, e.g. {removed[:3]}")
    if view_digest([p for p in paths if not artifacts.is_hidden(p)]) != row["view_digest"]:
        problems.append("visible file set does not hash to the published view_digest")
    return problems


def rebuild_case(row: dict, tasks: Path, mirrors: Path) -> tuple[str, str]:
    cid = row["candidate_id"]
    dest = (tasks / cid / "environment" / "repo").resolve()
    if dest.exists():
        return cid, f"FAIL: {dest} already exists; remove it and retry"
    m = mirror(row["repo"], mirrors).resolve()
    if git(m, "cat-file", "-e", f"{row['cutoff_sha']}^{{commit}}", ok=(0, 1, 128))[0] != 0:
        git(m, "fetch", "--quiet", "origin", row["cutoff_sha"])
    temp = f"swe_time_{cid}"
    git(m, "update-ref", f"refs/heads/{temp}", row["cutoff_sha"])
    try:
        # --no-local: a local clone would hardlink the whole object store, including every
        # post-cutoff object, while showing one branch.
        git(dest.parent, "clone", "--quiet", "--no-local", "--single-branch",
            "--branch", temp, str(m), str(dest))
    finally:
        git(m, "update-ref", "-d", f"refs/heads/{temp}")
    git(dest, "remote", "remove", "origin")
    git(dest, "branch", "-m", temp, "eval")
    _, refs = git(dest, "for-each-ref", "--format=%(refname)")
    for ref in refs.split():
        if ref != EVAL_REF:
            git(dest, "update-ref", "-d", ref)
    git(dest, "reflog", "expire", "--expire=now", "--all")
    git(dest, "gc", "--quiet", "--prune=now")
    git(dest, "checkout", "--quiet", "--detach", "eval")
    apply_sparse(dest)
    problems = self_check(dest, row)
    if problems:
        shutil.rmtree(dest, ignore_errors=True)
        return cid, "FAIL: " + "; ".join(problems)
    return cid, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--tasks", required=True, type=Path)
    ap.add_argument("--mirrors", type=Path, default=Path("mirrors"))
    ap.add_argument("--cases", nargs="*")
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    rows = [json.loads(l) for l in a.manifest.read_text().splitlines() if l.strip()]
    if a.cases:
        rows = [r for r in rows if r["candidate_id"] in set(a.cases)]
    for repo in sorted({r["repo"] for r in rows}):
        print(f"mirror {repo}", flush=True)
        mirror(repo, a.mirrors)
    failed = 0
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        for cid, status in ex.map(lambda r: rebuild_case(r, a.tasks, a.mirrors), rows):
            print(f"{cid}: {status}", flush=True)
            failed += status.startswith("FAIL")
    print(f"{len(rows) - failed}/{len(rows)} repositories verified")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
