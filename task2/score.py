#!/usr/bin/env python3
"""SWE-Time Forward (Task 2) batch scorer.

Scores a directory of predictions against the released tasks and reports WORKFLOW Case-Exact,
the only metric SWE-Time reports for this task.  Per-case scoring is exactly the in-container
verifier (`verifier/verify.py`), so a harbor run and this script agree.

    python3 score.py --tasks tasks/ --predictions preds/ [--manifest manifest.jsonl]
                     [--out results.json]

  --tasks        released task dirs, one per case: <case>/tests/gold.json
  --repos        optional; directory of rebuilt trees <case>/.  Default: the tree rebuild.py
                 wrote to tasks/<case>/environment/repo
  --predictions  one answer per case: <case>.json, same schema as /testbed/answer.json
  --manifest     optional; adds per-repository and Temporal x Spatial breakdowns

Denominator policy: every task in --tasks counts.  A missing prediction is scored as
`no_answer` (0), and an INVALID_ROUTING_STATE answer is 0, so models are compared on the same
fixed denominator.
"""
from __future__ import annotations
import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "verifier"))
import verify as V  # noqa: E402


def score_case(task_dir: Path, repo_dir: Path, pred_path: Path) -> dict:
    gold = json.loads((task_dir / "tests" / "gold.json").read_text())
    if pred_path.exists() and not repo_dir.is_dir():
        raise SystemExit(f"missing rebuilt repository for {task_dir.name}: {repo_dir}")
    return V.score_file(pred_path, set(gold["gold_activated_workflows"]), repo_dir)


def pct(xs):
    return round(100.0 * sum(xs) / len(xs), 1) if xs else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tasks", required=True, type=Path)
    ap.add_argument("--repos", type=Path)
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
        repo = (a.repos / c) if a.repos else (a.tasks / c / "environment" / "repo")
        per_case[c] = score_case(a.tasks / c, repo, a.predictions / f"{c}.json")

    hits = {c: int(r["reward"] == 1.0) for c, r in per_case.items()}
    report = {"metric": "workflow_exact", "n_cases": len(cases),
              "overall_pct": pct(list(hits.values())),
              "reasons": dict(Counter(r["reason"] for r in per_case.values()))}
    if meta:
        by_repo, by_cell = defaultdict(list), defaultdict(list)
        for c, h in hits.items():
            m = meta.get(c, {})
            by_repo[m.get("repo", "?")].append(h)
            by_cell[f"{m.get('temporal', '?')}/{m.get('spatial', '?')}"].append(h)
        report["per_repository_pct"] = {k: pct(v) for k, v in sorted(by_repo.items())}
        report["repo_macro_pct"] = round(sum(pct(v) for v in by_repo.values()) / len(by_repo), 1)
        report["temporal_x_spatial_pct"] = {k: pct(v) for k, v in sorted(by_cell.items())}

    print(json.dumps(report, indent=2))
    if a.out:
        a.out.write_text(json.dumps({"summary": report, "cases": per_case}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
