#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "fallow_rs_fallow__2079__52b30f5", "activated_workflows": [".github/workflows/ci.yml", ".github/workflows/commitlint.yml", ".github/workflows/coverage.yml", ".github/workflows/dependabot-auto-merge.yml", ".github/workflows/test-action.yml"]}
EOF
