#!/usr/bin/env python3
"""SWE-Time Backward verifier: exact 40-char SHA match, plus an environment audit.

The answer is `/testbed/answer.txt`: one line, the full lowercase SHA of the first bad commit.
Only an exact match with the Gold SHA scores 1; an ancestor or descendant of Gold does not.

Before the answer is read, the receipts are checked:
  * baseline receipt (taken when the image was built): HEAD must be the cutoff, `eval` must be
    the only ref, the post-cutoff probe commit must be absent, and the visible file set must
    hash to the published view_digest.  A violation means the environment is wrong, not the
    model, and is reported as such.
  * post receipt (taken now): a repository that disappeared, gained the post-cutoff commit, a
    remote, FETCH_HEAD or ~/.netrc is refused -- the agent has no legitimate reason to do any
    of these.  Moving HEAD, building, or editing files is how the task is meant to be solved,
    so those are recorded in `audit` and never change the score.

Outcomes (`reason`): correct, wrong_commit, unresolvable_sha, malformed_answer, no_answer,
broken_environment, bad_package_head, extra_refs, future_objects_present, view_mismatch,
network_exfiltration.
"""
import argparse
import json
import pathlib
import re
import subprocess

SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _int(value) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def grade_answer(raw: str | None, gold_sha: str, repo: str | None = None) -> dict:
    """Score the answer text alone.  `repo`, if given, separates wrong from unresolvable."""
    if raw is None:
        return {"reward": 0, "reason": "no_answer"}
    candidate = raw.strip().lower()
    if not SHA_RE.match(candidate):
        return {"reward": 0, "reason": "malformed_answer", "answer_rejected": candidate[:120]}
    if candidate == gold_sha:
        return {"reward": 1, "reason": "correct", "answer": candidate}
    resolved = None
    if repo:
        resolved = subprocess.run(["git", "-C", repo, "cat-file", "-e", candidate],
                                  capture_output=True).returncode == 0
    return {"reward": 0, "reason": "unresolvable_sha" if resolved is False else "wrong_commit",
            "answer": candidate}


def audit(gold: dict, baseline: dict | None, post: dict | None) -> tuple[str | None, dict]:
    """-> (refusal reason or None, audit record)."""
    rec = {"baseline_present": bool(baseline)}
    if baseline:
        if not baseline.get("repo_present"):
            return "broken_environment", rec
        if baseline.get("head") != gold["cutoff_sha"]:
            return "bad_package_head", rec
        if baseline.get("refs") != ["refs/heads/eval"]:
            return "extra_refs", rec
        if baseline.get("future_probe_rc") == 0:
            return "future_objects_present", rec
        if baseline.get("view_digest") != gold["view_digest"]:
            return "view_mismatch", rec
    if post:
        if not post.get("repo_present"):
            return "broken_environment", rec
        if post.get("future_probe_rc") == 0:
            return "future_objects_present", rec
        remotes = [r for r in post.get("remotes", []) if r.strip()]
        if remotes:
            rec["remotes"] = remotes
            return "network_exfiltration", rec
        if post.get("fetch_head") or post.get("netrc"):
            return "network_exfiltration", rec
        rec["head_moved"] = post.get("head") != gold["cutoff_sha"]
        rec["view_after_matches"] = post.get("view_digest") == gold["view_digest"]
        if baseline:
            rec["repo_untouched"] = (
                post.get("head") == baseline.get("head")
                and post.get("index_digest") == baseline.get("index_digest")
                and post.get("refs") == baseline.get("refs")
                and _int(post.get("dirty_tracked")) == _int(baseline.get("dirty_tracked"))
                and _int(post.get("object_count")) == _int(baseline.get("object_count")))
    return None, rec


def _load(path):
    try:
        return json.loads(pathlib.Path(path).read_text())
    except Exception:                                          # noqa: BLE001
        return None


def main():
    ap = argparse.ArgumentParser()
    for name in ("gold", "answer", "repo", "baseline", "post", "reward", "detail"):
        ap.add_argument(f"--{name}", required=True)
    args = ap.parse_args()

    gold = json.loads(pathlib.Path(args.gold).read_text())
    refusal, rec = audit(gold, _load(args.baseline), _load(args.post))
    if refusal:
        detail = {"reward": 0, "reason": refusal}
    else:
        path = pathlib.Path(args.answer)
        raw = path.read_text(errors="replace") if path.exists() else None
        detail = grade_answer(raw, gold["gold_sha"], args.repo)
    detail = {"case_id": gold["case_id"], **detail, "audit": rec}
    pathlib.Path(args.reward).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.reward).write_text(f"{detail['reward']}\n")
    pathlib.Path(args.detail).write_text(json.dumps(detail, indent=2) + "\n")
    print(f"reward={detail['reward']} reason={detail['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
