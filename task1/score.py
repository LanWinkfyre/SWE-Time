#!/usr/bin/env python3
"""SWE-Time Backward (Task 1) batch scorer.

Scores a directory of answers against the released tasks and reports Exact (first-bad-commit
SHA match).  Per-case scoring is the answer check of the in-container verifier
(`verifier/grade.py::grade_answer`); the environment audit needs the receipts taken inside the
container and is therefore only applied when the task is run through its own test.sh.

    python3 score.py --tasks tasks/ --predictions preds/ [--manifest manifest.jsonl] [--out results.json]

  --tasks        released task dirs, one per case: <case>/tests/gold.json
  --predictions  one answer per case: <case>.txt, same content as /testbed/answer.txt
  --manifest     optional; adds per-repository, Repo-Macro and S1-S4 breakdowns

Every task in --tasks counts; a missing answer is `no_answer` (0).
"""
from __future__ import annotations
import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "verifier"))
import grade as V  # noqa: E402


def pct(xs):
    return round(100.0 * sum(xs) / len(xs), 1) if xs else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tasks", required=True, type=Path)
    ap.add_argument("--predictions", required=True, type=Path)
    ap.add_argument("--manifest", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()

    cases = sorted(d.name for d in a.tasks.iterdir() if (d / "tests" / "gold.json").exists())
    if not cases:
        raise SystemExit(f"no tasks found under {a.tasks}")
    meta = {}
    if a.manifest:
        for line in a.manifest.read_text().splitlines():
            if line.strip():
                r = json.loads(line); meta[r["candidate_id"]] = r

    per_case = {}
    for c in cases:
        gold = json.loads((a.tasks / c / "tests" / "gold.json").read_text())
        p = a.predictions / f"{c}.txt"
        repo = a.tasks / c / "environment" / "repo"
        per_case[c] = V.grade_answer(p.read_text(errors="replace") if p.exists() else None,
                                     gold["gold_sha"], str(repo) if repo.is_dir() else None)

    hits = {c: int(r["reward"] == 1) for c, r in per_case.items()}
    report = {"metric": "exact", "n_cases": len(cases), "overall_pct": pct(list(hits.values())),
              "reasons": dict(Counter(r["reason"] for r in per_case.values()))}
    if meta:
        by_repo, by_subset = defaultdict(list), defaultdict(list)
        for c, h in hits.items():
            m = meta.get(c, {})
            by_repo[m.get("repo", "?")].append(h)
            by_subset[m.get("subset", "?")].append(h)
        report["per_repository_pct"] = {k: pct(v) for k, v in sorted(by_repo.items())}
        report["repo_macro_pct"] = round(sum(pct(v) for v in by_repo.values()) / len(by_repo), 1)
        report["subset_pct"] = {k: pct(v) for k, v in sorted(by_subset.items())}

    print(json.dumps(report, indent=2))
    if a.out:
        a.out.write_text(json.dumps({"summary": report, "cases": per_case}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
