#!/usr/bin/env python3
"""SWE-Time Forward verifier: score one answer against Gold at the workflow level.

An answer is `/testbed/answer.json` of the form {"case_id": ..., "activated_workflows": [...]}.
The case is correct iff the set of `activated_workflows` equals the Gold set exactly.

Outcomes (`reason` in detail.json; reward is 1.0 only for `correct`):
  correct                the workflow set equals Gold
  wrong                  a valid workflow set that differs from Gold
  no_answer              no answer file
  INVALID_ROUTING_STATE  not valid JSON, not an object, `activated_workflows` missing or not a
                         list of strings, or it names a path that is not a workflow file
                         (`.github/workflows/*.yml|*.yaml`) in the repository

The verifier also compares the repository tree digest recorded before the agent ran with the
digest taken now, so a run that modified the repository is visible in `audit`.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

WF_DIR = ".github/workflows"


def known_workflows(repo: Path) -> set[str]:
    d = repo / WF_DIR
    if not d.is_dir():
        return set()
    return {f"{WF_DIR}/{p.name}" for p in d.iterdir()
            if p.is_file() and p.name.endswith((".yml", ".yaml"))}


def score_answer(raw, gold_wf: set[str], known_wf: set[str]) -> dict:
    if not isinstance(raw, dict):
        return {"reason": "INVALID_ROUTING_STATE", "error": "answer is not a JSON object",
                "reward": 0.0}
    wfs = raw.get("activated_workflows")
    if not isinstance(wfs, list) or not all(isinstance(x, str) for x in wfs):
        return {"reason": "INVALID_ROUTING_STATE",
                "error": "activated_workflows missing or not a list of strings", "reward": 0.0}
    unknown = sorted({w for w in wfs if w not in known_wf})
    if unknown:
        return {"reason": "INVALID_ROUTING_STATE",
                "error": f"unknown workflow path(s): {unknown[:5]}", "reward": 0.0}
    pred = set(wfs)
    exact = pred == gold_wf
    return {"reason": "correct" if exact else "wrong", "reward": 1.0 if exact else 0.0,
            "exact": exact, "n_pred": len(pred), "n_gold": len(gold_wf),
            "missing": sorted(gold_wf - pred), "extra": sorted(pred - gold_wf),
            "activated_workflows": sorted(pred)}


def score_file(answer: Path, gold_wf: set[str], repo: Path) -> dict:
    try:
        raw = json.loads(answer.read_text())
    except FileNotFoundError:
        return {"reason": "no_answer", "reward": 0.0}
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"reason": "INVALID_ROUTING_STATE", "error": "answer is not valid JSON",
                "reward": 0.0}
    return score_answer(raw, gold_wf, known_workflows(repo))


def _audit(baseline: str | None, post: str | None) -> dict:
    if not baseline or not Path(baseline).exists():
        return {"baseline_present": False}
    try:
        b = json.loads(Path(baseline).read_text())
        p = json.loads(Path(post).read_text()) if post and Path(post).exists() else {}
    except Exception as e:                                     # noqa: BLE001
        return {"baseline_present": False, "audit_error": type(e).__name__}
    return {"baseline_present": True,
            "tree_digest_match": b.get("tree_digest") == p.get("tree_digest"),
            "baseline_tree_digest": b.get("tree_digest"), "post_tree_digest": p.get("tree_digest")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/testbed/repo")
    ap.add_argument("--answer", default="/testbed/answer.json")
    ap.add_argument("--gold", required=True)
    ap.add_argument("--reward", default="/logs/verifier/reward.txt")
    ap.add_argument("--detail", default="/logs/verifier/detail.json")
    ap.add_argument("--baseline", default=None)
    ap.add_argument("--post", default=None)
    a = ap.parse_args()

    gold = json.loads(Path(a.gold).read_text())
    detail = {"case_id": gold.get("case_id"), "metric": "workflow_exact"}
    detail.update(score_file(Path(a.answer), set(gold["gold_activated_workflows"]), Path(a.repo)))
    detail["audit"] = _audit(a.baseline, a.post)

    Path(a.reward).parent.mkdir(parents=True, exist_ok=True)
    Path(a.reward).write_text(f"{detail['reward']}\n")
    Path(a.detail).write_text(json.dumps(detail, ensure_ascii=False, indent=2))
    print(f"reward={detail['reward']} reason={detail['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
