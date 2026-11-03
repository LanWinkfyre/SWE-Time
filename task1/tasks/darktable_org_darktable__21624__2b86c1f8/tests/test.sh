#!/usr/bin/env bash
# SWE-Time Backward verifier entry point.  tests/ is uploaded only after the agent finishes.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p /logs/verifier
echo 0 > /logs/verifier/reward.txt
printf '{"reason": "verifier_crashed", "reward": 0}\n' > /logs/verifier/detail.json
FUTURE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["future_probe_sha"])' "$HERE/gold.json")"
python3 "$HERE/probe.py" --repo /testbed/repo --future-probe "$FUTURE" --stage verifier \
    --out /logs/verifier/post_receipt.json > /dev/null 2>&1
python3 "$HERE/grade.py" --gold "$HERE/gold.json" --answer /testbed/answer.txt \
    --repo /testbed/repo --baseline /opt/swe-time/receipt.json \
    --post /logs/verifier/post_receipt.json \
    --reward /logs/verifier/reward.txt --detail /logs/verifier/detail.json
