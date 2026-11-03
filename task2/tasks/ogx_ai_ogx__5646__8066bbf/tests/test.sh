#!/usr/bin/env bash
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p /logs/verifier
echo 0 > /logs/verifier/reward.txt
printf '{"reason": "verifier_crashed", "reward": 0}\n' > /logs/verifier/detail.json
python3 "$HERE/tree_digest.py" --repo /testbed/repo --stage verifier --out /logs/verifier/post_receipt.json >/dev/null 2>&1 || true
python3 "$HERE/verify.py" --repo /testbed/repo --answer /testbed/answer.json --gold "$HERE/gold.json" --reward /logs/verifier/reward.txt --detail /logs/verifier/detail.json --baseline /opt/swe-time/receipt.json --post /logs/verifier/post_receipt.json
