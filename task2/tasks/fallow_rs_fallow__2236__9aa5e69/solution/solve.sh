#!/usr/bin/env bash
# Oracle: write the Gold answer.  Used to check that a task is solvable end to end.
cat > /testbed/answer.json <<'EOF'
{"case_id": "fallow_rs_fallow__2236__9aa5e69", "activated_workflows": [".github/workflows/bench-type-aware.yml", ".github/workflows/ci.yml", ".github/workflows/commitlint.yml", ".github/workflows/coverage.yml", ".github/workflows/dependabot-auto-merge.yml"]}
EOF
