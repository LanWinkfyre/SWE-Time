#!/usr/bin/env python3
"""Write a digest of the working tree — the audit anchor for "was the repo tampered with?".

Task 1's audit bound four git invariants to the checkout (HEAD == cutoff, one ref, no future
objects, view_digest). Task 2's container carries a plain working tree with NO .git at all, so
none of those apply — and the strongest statement available is simply that the bytes did not
change. This computes a content digest (path + sha256 for every tracked file) and stores it in
the baseline receipt; the verifier recomputes it and reports the match.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from pathlib import Path


def tree_digest(root: Path, cap: int = 400000) -> tuple[str, int]:
    h = hashlib.sha256()
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for name in sorted(filenames):
            p = Path(dirpath) / name
            rel = p.relative_to(root).as_posix()
            h.update(rel.encode())
            h.update(b"\0")
            try:
                st = p.lstat()
                h.update(str(st.st_size).encode())
                if p.is_file() and not p.is_symlink():
                    with p.open("rb") as f:
                        while True:
                            chunk = f.read(1 << 20)
                            if not chunk:
                                break
                            h.update(chunk)
            except OSError:
                h.update(b"<unreadable>")
            h.update(b"\0")
            n += 1
            if n >= cap:
                break
    return h.hexdigest(), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/testbed/repo")
    ap.add_argument("--stage", required=True, choices=["baseline", "preinstall", "verifier"])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    root = Path(a.repo)
    d, n = (tree_digest(root) if root.is_dir() else ("<no-repo>", 0))
    rec = {"stage": a.stage, "repo": str(root), "repo_present": root.is_dir(),
           "tree_digest": d, "n_files": n, "uid": os.getuid()}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rec, indent=2))
    print(f"{a.stage}: {n} files digest={d[:12]}")


if __name__ == "__main__":
    main()
