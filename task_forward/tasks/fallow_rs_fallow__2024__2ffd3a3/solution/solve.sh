#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "fallow_rs_fallow__2024__2ffd3a3", "activated_workflows": [".github/workflows/bench.yml", ".github/workflows/ci.yml", ".github/workflows/commitlint.yml", ".github/workflows/coverage.yml", ".github/workflows/dependabot-auto-merge.yml"]}
EOF
