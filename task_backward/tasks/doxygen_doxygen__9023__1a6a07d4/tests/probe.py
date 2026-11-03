#!/usr/bin/env python3
"""Record the invariants of one SWE-Time Backward repository.

Run once when the image is built (`--stage baseline`, written to /opt/swe-time/receipt.json)
and again by the verifier after the agent has finished (`--stage verifier`).  The verifier
compares the two.  Nothing here reads the Gold.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys


def run(cmd, timeout=300):
    try:
        done = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except FileNotFoundError:
        return {"rc": 127, "out": "not found"}
    except subprocess.TimeoutExpired:
        return {"rc": 124, "out": "timeout"}
    text = (done.stdout + done.stderr).decode("utf-8", "replace")[:400]
    return {"rc": done.returncode, "out": text.strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--future-probe", required=True,
                    help="a commit written after the cutoff; it must be absent from the repo")
    ap.add_argument("--stage", required=True, choices=["baseline", "verifier"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = args.repo
    git = ["git", "-C", repo]
    here = pathlib.Path(__file__).resolve().parent
    receipt = {
        "stage": args.stage,
        "repo_present": os.path.isdir(os.path.join(repo, ".git")),
        "head": run(git + ["rev-parse", "HEAD"])["out"],
        "refs": run(git + ["for-each-ref", "--format=%(refname)"])["out"].split(),
        # rc != 0 means the object is absent, which is the invariant.
        "future_probe_rc": run(git + ["cat-file", "-e", args.future_probe])["rc"],
        "remotes": run(git + ["remote", "-v"])["out"].split("\n"),
        "fetch_head": os.path.exists(os.path.join(repo, ".git", "FETCH_HEAD")),
        "netrc": os.path.exists(os.path.expanduser("~/.netrc")),
        # view_digest hashes the visible tracked path list (the shipped view);
        # index_digest and dirty_tracked record whether tracked content was modified.
        "view_digest": run([sys.executable, str(here / "view_digest.py"), repo])["out"],
        "index_digest": run(["bash", "-c",
                             f"git -C {repo} ls-files -s -z | sha256sum | cut -d' ' -f1"])["out"],
        "dirty_tracked": run(["bash", "-c",
                              f"git -C {repo} status --porcelain --untracked-files=no | wc -l"],
                             timeout=600)["out"],
        "object_count": run(["bash", "-c",
                             f"git -C {repo} cat-file --batch-all-objects --batch-check | wc -l"],
                            timeout=900)["out"],
    }
    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.out).write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"{args.stage}: head={receipt['head'][:12]} view={receipt['view_digest'][:12]}")


if __name__ == "__main__":
    main()
